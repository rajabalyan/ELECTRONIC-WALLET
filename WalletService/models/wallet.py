from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from CommonService.database.base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(35), unique=True, index=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), default=Decimal("0.00"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
