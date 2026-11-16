from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from CommonService.logging_config import configure_logging
from TransactionService.api.routes.transactions import router as transactions_router
from TransactionService.config import settings

configure_logging(settings.log_level)
app = FastAPI(title="TransactionService", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(transactions_router, prefix="/txn-service")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "TransactionService"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("TransactionService.main:app", host=settings.host, port=settings.port, reload=False)
