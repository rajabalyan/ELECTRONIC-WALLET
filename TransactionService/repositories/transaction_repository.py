from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select

from TransactionService.db.session import get_session
from TransactionService.models.outbox_event import OutboxEvent
from TransactionService.models.transaction import Transaction


class TransactionRepository:
    async def lookup_receiver(self, receiver_mobile_number: str) -> dict | None:
        async with get_session() as session:
            result = await session.execute(select(Transaction).where(Transaction.receiver_mobile_number == receiver_mobile_number))
            txn = result.scalar_one_or_none()
            return None if txn is None else {"transaction_id": txn.transaction_id, "receiver_mobile_number": txn.receiver_mobile_number}

    async def create_initiated_transaction(self, sender_user_id: int, receiver_mobile_number: str, amount: Decimal, purpose: str) -> dict:
        async with get_session() as session:
            txn_id = f"txn-{uuid4().hex[:12]}"
            txn = Transaction(transaction_id=txn_id, sender_user_id=sender_user_id, receiver_mobile_number=receiver_mobile_number, amount=amount, purpose=purpose, status="INITIATED")
            session.add(txn)
            await session.commit()
            await session.refresh(txn)
            return {"transaction_id": txn.transaction_id, "status": txn.status}

    async def create_outbox_event(self, event_id: str, topic: str, payload: str) -> None:
        async with get_session() as session:
            event = OutboxEvent(event_id=event_id, topic=topic, payload=payload)
            session.add(event)
            await session.commit()

    async def history_for_user(self, user_id: int) -> list[dict]:
        async with get_session() as session:
            result = await session.execute(select(Transaction).where((Transaction.sender_user_id == user_id)))
            rows = result.scalars().all()
            return [{"transaction_id": row.transaction_id, "amount": str(row.amount), "purpose": row.purpose, "sender": row.sender_user_id, "receiver": row.receiver_mobile_number, "status": row.status, "status_message": row.status_message, "created_at": row.created_at.isoformat(), "direction": "DEBIT" if row.sender_user_id == user_id else "CREDIT"} for row in rows]

    async def update_status(self, transaction_id: str, status: str, message: str) -> None:
        async with get_session() as session:
            result = await session.execute(select(Transaction).where(Transaction.transaction_id == transaction_id))
            txn = result.scalar_one_or_none()
            if txn is not None:
                txn.status = status
                txn.status_message = message
                await session.commit()
