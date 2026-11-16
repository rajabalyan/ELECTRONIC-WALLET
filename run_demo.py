from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable
from urllib import error, request

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE_FILE = PROJECT_ROOT / ".env.example"

SERVICES = [
    ("OnboardingService", 8001, "/health"),
    ("WalletService", 8002, "/health"),
    ("TransactionService", 8003, "/health"),
    ("NotificationService", 8004, "/health"),
]


def ensure_project_ready() -> None:
    if sys.version_info[:2] < (3, 12):
        raise RuntimeError("This project requires Python 3.12 or newer. Use the included .venv or install Python 3.12.")

    if not ENV_FILE.exists() and ENV_EXAMPLE_FILE.exists():
        shutil.copy2(ENV_EXAMPLE_FILE, ENV_FILE)
        print(f"Created default environment file at {ENV_FILE}")

    if not ENV_FILE.exists():
        raise RuntimeError("Missing .env file. Create one from .env.example before starting the demo.")

    env_contents = ENV_FILE.read_text(encoding="utf-8")
    if "mysql+aiomysql://root:root@localhost" in env_contents:
        ENV_FILE.write_text(ENV_EXAMPLE_FILE.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Reset local development defaults in {ENV_FILE} to the SQLite demo configuration.")

    if not shutil.which(sys.executable):
        raise RuntimeError("Python interpreter not found in the current environment.")


def wait_for_service(service_name: str, port: int, path: str, timeout_seconds: int = 30) -> None:
    url = f"http://localhost:{port}{path}"
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None

    while time.time() < deadline:
        try:
            with request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    print(f"{service_name} is ready at {url}")
                    return
        except (error.URLError, TimeoutError, ConnectionError) as exc:  # pragma: no cover - startup timing only
            last_error = exc
            time.sleep(0.5)

    detail = last_error or RuntimeError(f"Health check for {service_name} timed out")
    raise RuntimeError(f"{service_name} did not become healthy at {url}: {detail}")


def start_service(service_name: str) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONPATH"] = str(PROJECT_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.Popen(
        [sys.executable, "-m", f"{service_name}.main"],
        cwd=str(PROJECT_ROOT),
        env=env,
        stdout=None,
        stderr=None,
        text=True,
    )


def stop_services(processes: Iterable[subprocess.Popen[str]]) -> None:
    for process in processes:
        if process.poll() is None:
            process.terminate()
    for process in processes:
        if process.poll() is None:
            process.wait(timeout=10)


if __name__ == "__main__":
    try:
        ensure_project_ready()
    except RuntimeError as exc:
        print(f"Startup validation failed: {exc}")
        raise SystemExit(1)

    print("Starting E-Wallet demo services...")
    processes: list[subprocess.Popen[str]] = []
    try:
        for module_name, _, _ in SERVICES:
            processes.append(start_service(module_name))
            time.sleep(0.75)

        for module_name, port, path in SERVICES:
            wait_for_service(module_name, port, path)

        print("\nDemo services are running:")
        for module_name, port, _ in SERVICES:
            print(f"- {module_name}: http://localhost:{port}")
        print("\nFrontend: http://localhost:8001")
        print("Press Ctrl+C to stop all services.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping demo services...")
            stop_services(processes)
            print("Stopped.")
    except KeyboardInterrupt:
        print("\nStopping demo services...")
        stop_services(processes)
        print("Stopped.")
    except Exception as exc:  # pragma: no cover - CLI wrapper only
        print(f"Failed to start the demo stack: {exc}")
        stop_services(processes)
        raise SystemExit(1)
