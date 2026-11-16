from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict


class UserCreatedPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: str
    name: str
    email: str
    mobile_number: str
    identification_type: str
    identification_value: str


class TransactionInitiationPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    transaction_id: str
    sender_mobile_number: str
    receiver_mobile_number: str
    amount: str
    purpose: str


class TransactionUpdatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    transaction_id: str
    status: str
    status_message: str


class EventEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str
    event_type: str
    schema_version: str = "1.0"
    timestamp: datetime
    payload: dict[str, Any]

    @classmethod
    def create(cls, event_type: str, payload: dict[str, Any], event_id: str | None = None) -> "EventEnvelope":
        return cls(
            event_id=event_id or f"{event_type}-{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            payload=payload,
        )

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_none=True)

    @classmethod
    def from_json(cls, raw: str | bytes) -> "EventEnvelope":
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        data = json.loads(raw)
        return cls.model_validate(data)
