from __future__ import annotations

import json

from aiokafka import AIOKafkaProducer

from CommonService.kafka.events import EventEnvelope


class KafkaProducerClient:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        if self.producer is None:
            self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await self.producer.start()

    async def stop(self) -> None:
        if self.producer is not None:
            await self.producer.stop()
            self.producer = None

    async def send_event(self, topic: str, event: EventEnvelope, key: str | None = None) -> None:
        if self.producer is None:
            await self.start()
        payload = json.dumps(event.model_dump(mode="json")).encode("utf-8")
        await self.producer.send_and_wait(topic, value=payload, key=(key.encode("utf-8") if key else None))
