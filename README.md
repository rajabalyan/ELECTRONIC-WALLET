# E-Wallet Python

This repository contains four independent backend services that mirror the core flows of a Java e-wallet system using FastAPI, SQLAlchemy, Redis, Kafka, JWT, and SMTP. The project is intentionally beginner-friendly, runs as separate local Python processes, and is now set up with a safer startup flow for local execution.

## Services

- OnboardingService: user registration, OTP validation, login, and JWT-authenticated user lookup.
- WalletService: wallet creation on user creation, balance lookup, and transfer processing.
- TransactionService: transaction initiation, history, and Kafka-backed status tracking.
- NotificationService: OTP generation, email dispatch, and welcome email handling.
- CommonService: shared models, security helpers, Kafka event schemas, and utility logic.

## Recommended setup

This project expects Python 3.12+. The repository includes a `.venv` and a service-safe demo startup script, but you can also recreate the environment from scratch.

Windows PowerShell:

```powershell
cd "C:\path\to\E-Wallet-Python"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cd /path/to/E-Wallet-Python
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

The demo runner now validates the environment automatically and creates `.env` from `.env.example` if it is missing.

## Run the local demo

```bash
python run_demo.py
```

This starts all four backend services and exposes the frontend at:

```text
http://localhost:8001
```

The startup runner verifies each service health check before reporting the stack as ready.

If you want to start them manually, use separate terminals:

```bash
python -m OnboardingService.main
python -m WalletService.main
python -m TransactionService.main
python -m NotificationService.main
```

Then open the frontend in your browser at http://localhost:8001.

The UI lets you:
- register a user
- validate the OTP
- log in with the generated JWT
- check the wallet balance
- initiate a wallet transfer

In local development, the OTP is returned in the registration response and filled into the OTP form automatically. Wallets are provisioned on login. Transfers are processed synchronously by the wallet service, so local testing does not require Kafka. Production environments continue to use the configured Kafka producer path.

## Configuration

Use `.env` to override default service settings. The project is configured to work with SQLite and a shared SQLite-backed expiring cache in local development, so Redis is not required for the demo. For deployment, configure Redis URLs and real database, Kafka, SMTP, and secret values. Development OTP codes are returned to the local UI only while the environment and email mode are set to development.

## Kafka topics

- `user-creation-topic`
- `txn-initiation-topic`
- `txn-update-topic`

## Testing

```bash
pytest -q
```

Use mocks for SMTP and Kafka in tests. No real SMTP or live Kafka broker is needed.

## Production-readiness note

This repository is now closer to a runnable local reference implementation, but it is still not a fully hardened production payment platform. For real production use, you would add:

- secure secret management
- real database migrations and transactional controls
- Redis/Kafka resiliency and retry policies
- observability and audit logging
- stronger identity and authorization policies
- deployment and infrastructure automation

The included code is structured for learning and local validation while remaining extensible toward a real system.
