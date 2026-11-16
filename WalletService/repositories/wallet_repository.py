from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select

from WalletService.db.session import get_session
from WalletService.models.processed_event import ProcessedEvent
from WalletService.models.wallet import Wallet


class WalletRepository:
    async def get_wallet_for_user(self, user_id: int) -> dict | None:
        async with get_session() as session:
            result = await session.execute(select(Wallet).where(Wallet.user_id == user_id))
            wallet = result.scalar_one_or_none()
            return None if wallet is None else {"id": wallet.id, "user_id": wallet.user_id, "mobile_number": wallet.mobile_number, "balance": wallet.balance, "status": wallet.status}

    async def get_wallet_by_mobile(self, mobile_number: str) -> dict | None:
        async with get_session() as session:
            result = await session.execute(select(Wallet).where(Wallet.mobile_number == mobile_number))
            wallet = result.scalar_one_or_none()
            return None if wallet is None else {"id": wallet.id, "user_id": wallet.user_id, "mobile_number": wallet.mobile_number, "balance": wallet.balance, "status": wallet.status}

    async def create_wallet(self, user_id: int, mobile_number: str, initial_balance: Decimal) -> dict:
        async with get_session() as session:
            existing = await session.execute(select(Wallet).where(Wallet.user_id == user_id))
            wallet = existing.scalar_one_or_none()
            if wallet is None:
                wallet = Wallet(user_id=user_id, mobile_number=mobile_number, balance=initial_balance)
                session.add(wallet)
                await session.commit()
                await session.refresh(wallet)
            return {"id": wallet.id, "user_id": wallet.user_id, "mobile_number": wallet.mobile_number, "balance": wallet.balance, "status": wallet.status}

    async def mark_event_processed(self, event_id: str, event_type: str) -> None:
        async with get_session() as session:
            processed = ProcessedEvent(id=event_id, event_type=event_type)
            session.add(processed)
            await session.commit()

    async def is_event_processed(self, event_id: str) -> bool:
        async with get_session() as session:
            result = await session.execute(select(ProcessedEvent).where(ProcessedEvent.id == event_id))
            return result.scalar_one_or_none() is not None

    async def locking_update(self, user_id: int, delta: Decimal) -> dict | None:
        async with get_session() as session:
            result = await session.execute(select(Wallet).where(Wallet.user_id == user_id).with_for_update())
            wallet = result.scalar_one_or_none()
            if wallet is None:
                return None
            wallet.balance += delta
            await session.commit()
            return {"id": wallet.id, "user_id": wallet.user_id, "mobile_number": wallet.mobile_number, "balance": wallet.balance, "status": wallet.status}
