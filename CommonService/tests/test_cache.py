from __future__ import annotations

import asyncio

from CommonService.cache import SQLiteCache


def test_sqlite_cache_shares_values_and_expires(tmp_path) -> None:
    async def run() -> None:
        cache_path = tmp_path / "cache.db"
        writer = SQLiteCache(cache_path)
        reader = SQLiteCache(cache_path)

        await writer.setex("pending_signup:user@example.com", 30, "signup-data")
        assert await reader.get("pending_signup:user@example.com") == "signup-data"

        await reader.delete("pending_signup:user@example.com")
        assert await writer.get("pending_signup:user@example.com") is None

        await writer.setex("otp:user@example.com", 1, "123456")
        await asyncio.sleep(1.05)
        assert await reader.get("otp:user@example.com") is None

    asyncio.run(run())
