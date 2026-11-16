from __future__ import annotations

from CommonService.kafka.events import EventEnvelope
from CommonService.kafka.producer import KafkaProducerClient
from WalletService.config import settings


class StatusProducer:
    def __init__(self, bootstrap_servers: str | None = None):
        self.bootstrap_servers = bootstrap_servers or settings.kafka_bootstrap_servers
        self.producer = KafkaProducerClient(self.bootstrap_servers)

    async def publish(self, transaction_id: str, status: str, status_message: str) -> None:
        event = EventEnvelope.create(
            "transaction.status.updated",
            {"transaction_id": transaction_id, "status": status, "status_message": status_message},
            event_id=f"txn-update-{transaction_id}",
        )
        await self.producer.send_event(settings.txn_update_topic, event, key=transaction_id)
