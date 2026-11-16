from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select

from CommonService.kafka.events import EventEnvelope
from WalletService.db.session import get_session
from WalletService.models.wallet import Wallet
from WalletService.repositories.wallet_repository import WalletRepository


class TransactionProcessor:
    def __init__(self, repo: WalletRepository | None = None):
        self.repo = repo or WalletRepository()

    async def process_event(self, event: EventEnvelope) -> dict:
        payload = event.payload
        if await self.repo.is_event_processed(event.event_id):
            return {"status": "duplicate", "message": "Event already processed"}
        amount = Decimal(str(payload["amount"]))
        sender_mobile = payload["sender_mobile_number"]
        receiver_mobile = payload["receiver_mobile_number"]
        async with get_session() as session:
            sender_wallet = (await session.execute(select(Wallet).where(Wallet.mobile_number == sender_mobile).with_for_update())).scalar_one_or_none()
            receiver_wallet = (await session.execute(select(Wallet).where(Wallet.mobile_number == receiver_mobile).with_for_update())).scalar_one_or_none()
            if sender_wallet is None or receiver_wallet is None:
                raise ValueError("Sender or receiver wallet not found")
            if amount <= 0:
                raise ValueError("Transfer amount must be positive")
            if sender_wallet.balance < amount:
                raise ValueError("Insufficient funds")
            sender_wallet.balance -= amount
            receiver_wallet.balance += amount
            session.add(sender_wallet)
            session.add(receiver_wallet)
            await session.commit()
        await self.repo.mark_event_processed(event.event_id, event.event_type)
        return {"status": "success", "transaction_id": payload["transaction_id"], "message": "Transfer processed successfully"}
