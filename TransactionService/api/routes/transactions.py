from __future__ import annotations

from decimal import Decimal

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from CommonService.kafka.events import EventEnvelope
from CommonService.kafka.producer import KafkaProducerClient
from CommonService.security.jwt import create_access_token
from TransactionService.api.dependencies import get_current_user
from TransactionService.config import settings
from TransactionService.repositories.transaction_repository import TransactionRepository
from TransactionService.schemas.transaction import InitiateTransactionRequest, TransactionResponse

router = APIRouter(tags=["transactions"])


async def get_repository() -> TransactionRepository:
    return TransactionRepository()


@router.post("/initiate/transaction", response_model=TransactionResponse)
async def initiate_transaction(payload: InitiateTransactionRequest, current_user: dict = Depends(get_current_user), repo: TransactionRepository = Depends(get_repository)) -> TransactionResponse:
    sender_user_id = int(current_user["sub"])
    receiver_mobile = payload.receiver_mobile_number
    if not receiver_mobile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": "validation_error", "message": "Receiver mobile is required"})
    txn = await repo.create_initiated_transaction(sender_user_id, receiver_mobile, payload.amount, payload.purpose)
    event = EventEnvelope.create(
        "transaction.initiated",
        {
            "transaction_id": txn["transaction_id"],
            "sender_mobile_number": str(current_user.get("mobile_number", "")),
            "receiver_mobile_number": receiver_mobile,
            "amount": str(payload.amount),
            "purpose": payload.purpose,
        },
        event_id=f"txn-init-{txn['transaction_id']}",
    )
    if settings.environment.lower() in {"development", "local", "test"}:
        service_token = create_access_token(
            str(sender_user_id),
            settings.jwt_secret,
            5,
            extra_claims={"mobile_number": current_user.get("mobile_number")},
            algorithm=settings.jwt_algorithm,
        )
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"{settings.wallet_service_url.rstrip('/')}/wallet-service/transfer",
                    json={
                        "transaction_id": txn["transaction_id"],
                        "receiver_mobile_number": receiver_mobile,
                        "amount": str(payload.amount),
                        "purpose": payload.purpose,
                    },
                    headers={"Authorization": f"Bearer {service_token}"},
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            reason = exc.response.text or "Wallet service rejected the transfer"
            await repo.update_status(txn["transaction_id"], "FAILED", reason)
            error_status = status.HTTP_400_BAD_REQUEST if exc.response.status_code < 500 else status.HTTP_502_BAD_GATEWAY
            raise HTTPException(status_code=error_status, detail={"code": "transfer_failed", "message": reason}) from exc
        except httpx.RequestError as exc:
            await repo.update_status(txn["transaction_id"], "FAILED", "Wallet service is unavailable")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail={"code": "wallet_service_unavailable", "message": "Wallet service is unavailable"}) from exc
        await repo.update_status(txn["transaction_id"], "COMPLETED", "Transfer processed successfully")
        return TransactionResponse(transaction_id=txn["transaction_id"], status="COMPLETED")

    producer = KafkaProducerClient(settings.kafka_bootstrap_servers)
    await producer.send_event(settings.txn_initiation_topic, event, key=txn["transaction_id"])
    return TransactionResponse(transaction_id=txn["transaction_id"], status="INITIATED")


@router.get("/get/transaction/history")
async def transaction_history(current_user: dict = Depends(get_current_user), repo: TransactionRepository = Depends(get_repository)) -> dict:
    records = await repo.history_for_user(int(current_user["sub"]))
    return {"items": records}
