from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from CommonService.logging_config import configure_logging
from NotificationService.api.routes.otp import router as otp_router
from NotificationService.config import settings

configure_logging(settings.log_level)
app = FastAPI(title="NotificationService", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(otp_router, prefix="")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "NotificationService"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("NotificationService.main:app", host=settings.host, port=settings.port, reload=False)
