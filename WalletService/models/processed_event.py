from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from CommonService.database.base import Base


class ProcessedEvent(Base):
    __tablename__ = "processed_events"

    id: Mapped[str] = mapped_column(String(240), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
