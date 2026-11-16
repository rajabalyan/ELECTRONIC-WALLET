from __future__ import annotations

from CommonService.kafka.events import EventEnvelope
from TransactionService.repositories.transaction_repository import TransactionRepository


async def handle_transaction_status_update(msg: dict) -> None:
    event = EventEnvelope.model_validate(msg)
    repo = TransactionRepository()
    await repo.update_status(event.payload["transaction_id"], event.payload["status"], event.payload["status_message"])
