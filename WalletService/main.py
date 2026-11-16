from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from CommonService.logging_config import configure_logging
from WalletService.api.routes.wallets import router as wallets_router
from WalletService.config import settings

configure_logging(settings.log_level)
app = FastAPI(title="WalletService", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(wallets_router, prefix="/wallet-service")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "WalletService"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("WalletService.main:app", host=settings.host, port=settings.port, reload=False)
