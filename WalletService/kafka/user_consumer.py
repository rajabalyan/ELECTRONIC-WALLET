from __future__ import annotations

from decimal import Decimal

from CommonService.kafka.events import EventEnvelope
from WalletService.services.wallet_service import WalletService


async def handle_user_created(msg: dict) -> None:
    event = EventEnvelope.model_validate(msg)
    payload = event.payload
    service = WalletService()
    await service.create_wallet(int(payload["user_id"]), payload["mobile_number"], Decimal("100.00"))
