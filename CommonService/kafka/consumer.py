from __future__ import annotations

import json
from typing import Callable

from aiokafka import AIOKafkaConsumer


class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: list[str]):
        self.consumer = AIOKafkaConsumer(*topics, bootstrap_servers=bootstrap_servers, group_id=group_id, enable_auto_commit=False)

    async def start(self) -> None:
        await self.consumer.start()

    async def stop(self) -> None:
        await self.consumer.stop()

    async def consume(self, callback: Callable[[dict], None]) -> None:
        async for msg in self.consumer:
            payload = json.loads(msg.value.decode("utf-8"))
            await callback(payload)
            await self.consumer.commit()
