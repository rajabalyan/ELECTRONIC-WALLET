from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status

from CommonService.kafka.events import EventEnvelope
from WalletService.api.dependencies import get_current_user
from WalletService.config import settings
from WalletService.repositories.wallet_repository import WalletRepository
from WalletService.schemas.wallet import WalletTransferRequest
from WalletService.services.transaction_processor import TransactionProcessor

router = APIRouter(tags=["wallets"])


async def get_repository() -> WalletRepository:
    return WalletRepository()


@router.post("/create")
async def create_wallet(current_user: dict = Depends(get_current_user), repo: WalletRepository = Depends(get_repository)) -> dict:
    mobile_number = current_user.get("mobile_number")
    if not mobile_number:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "invalid_token", "message": "Token is missing the user's mobile number"})
    wallet = await repo.create_wallet(int(current_user["sub"]), mobile_number, Decimal(settings.initial_balance))
    return {"user_id": wallet["user_id"], "balance": str(wallet["balance"]), "status": wallet["status"]}


@router.post("/transfer")
async def transfer(payload: WalletTransferRequest, current_user: dict = Depends(get_current_user), repo: WalletRepository = Depends(get_repository)) -> dict:
    sender_mobile = current_user.get("mobile_number")
    if not sender_mobile:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "invalid_token", "message": "Token is missing the user's mobile number"})
    event = EventEnvelope.create(
        "transaction.initiated",
        {
            "transaction_id": payload.transaction_id,
            "sender_mobile_number": sender_mobile,
            "receiver_mobile_number": payload.receiver_mobile_number,
            "amount": str(payload.amount),
            "purpose": payload.purpose,
        },
        event_id=f"txn-init-{payload.transaction_id}",
    )
    try:
        return await TransactionProcessor(repo).process_event(event)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": "transfer_rejected", "message": str(exc)}) from exc


@router.get("/get/balance")
async def get_balance(current_user: dict = Depends(get_current_user), repo: WalletRepository = Depends(get_repository)) -> dict:
    wallet = await repo.get_wallet_for_user(int(current_user["sub"]))
    if wallet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "wallet_not_found", "message": "Wallet not found"})
    return {"user_id": current_user["sub"], "balance": str(wallet["balance"])}
