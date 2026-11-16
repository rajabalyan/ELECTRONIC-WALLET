from __future__ import annotations

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from CommonService.database.base import Base

# Import all declarative models so the metadata contains every table we may use.
from OnboardingService.models.user import User  # noqa: F401
from TransactionService.models.outbox_event import OutboxEvent  # noqa: F401
from TransactionService.models.transaction import Transaction  # noqa: F401
from WalletService.models.processed_event import ProcessedEvent  # noqa: F401
from WalletService.models.wallet import Wallet  # noqa: F401


def build_session_factory(db_url: str, echo: bool = False):
    engine = create_async_engine(db_url, echo=echo, future=True)

    async def create_schema() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(create_schema())

    return async_sessionmaker(engine, expire_on_commit=False, autocommit=False, autoflush=False)
