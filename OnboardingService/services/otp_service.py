from __future__ import annotations

import random

from redis.asyncio import Redis


class OtpService:
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def generate_otp() -> str:
        return str(random.randint(100000, 999999))

    async def store_otp(self, email: str, otp: str, ttl_seconds: int = 300) -> None:
        await self.redis.setex(f"otp:{email}", ttl_seconds, otp)
