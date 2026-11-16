from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from CommonService.logging_config import configure_logging
from OnboardingService.api.routes.auth import router as auth_router
from OnboardingService.api.routes.users import router as users_router
from OnboardingService.config import settings

configure_logging(settings.log_level)
app = FastAPI(title="OnboardingService", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/onboarding-service")
app.include_router(users_router, prefix="/onboarding-service")

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="frontend_static")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(str(frontend_dir / "index.html"))


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "OnboardingService"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("OnboardingService.main:app", host=settings.host, port=settings.port, reload=False)
