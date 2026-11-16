from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from CommonService.database.base import Base


class IdentificationType(str, Enum):
    NATIONAL_ID = "NATIONAL_ID"
    PASSPORT = "PASSPORT"
    DRIVER_LICENSE = "DRIVER_LICENSE"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    INACTIVE = "INACTIVE"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(35), unique=True, index=True, nullable=False)
    date_of_birth: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    identification_type: Mapped[str] = mapped_column(String(40), nullable=False)
    identification_value: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=UserStatus.PENDING.value, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
