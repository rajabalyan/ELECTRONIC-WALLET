from __future__ import annotations

from CommonService.kafka.events import EventEnvelope
from WalletService.services.transaction_processor import TransactionProcessor


async def handle_transaction_initiated(msg: dict) -> None:
    event = EventEnvelope.model_validate(msg)
    processor = TransactionProcessor()
    return await processor.process_event(event)
