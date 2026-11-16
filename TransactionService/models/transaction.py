from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from CommonService.database.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    sender_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    receiver_mobile_number: Mapped[str] = mapped_column(String(35), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)
    purpose: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="INITIATED", nullable=False)
    status_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
