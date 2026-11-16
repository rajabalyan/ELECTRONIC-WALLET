from __future__ import annotations

from CommonService.kafka.producer import KafkaProducerClient


async def publish_pending_outbox_events(topic: str, bootstrap_servers: str) -> None:
    producer = KafkaProducerClient(bootstrap_servers)
    await producer.start()
    await producer.stop()
