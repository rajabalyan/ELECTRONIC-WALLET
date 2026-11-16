from __future__ import annotations

import time
from pathlib import Path
from typing import Protocol

import aiosqlite
from redis.asyncio import Redis
from sqlalchemy.engine import make_url


class CacheStore(Protocol):
    async def get(self, key: str) -> str | None: ...

    async def setex(self, key: str, seconds: int, value: str | int) -> object: ...

    async def delete(self, *keys: str) -> int: ...


class SQLiteCache:
    def __init__(self, database_path: Path):
        self.database_path = database_path

    async def _ensure_table(self, connection: aiosqlite.Connection) -> None:
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS cache_entries (
                cache_key TEXT PRIMARY KEY,
                cache_value TEXT NOT NULL,
                expires_at REAL NOT NULL
            )
            """
        )

    async def get(self, key: str) -> str | None:
        async with aiosqlite.connect(self.database_path) as connection:
            await self._ensure_table(connection)
            cursor = await connection.execute(
                "SELECT cache_value, expires_at FROM cache_entries WHERE cache_key = ?",
                (key,),
            )
            row = await cursor.fetchone()
            await cursor.close()
            if row is None:
                return None

            value, expires_at = row
            if expires_at <= time.time():
                await connection.execute("DELETE FROM cache_entries WHERE cache_key = ?", (key,))
                await connection.commit()
                return None
            return str(value)

    async def setex(self, key: str, seconds: int, value: str | int) -> None:
        if seconds <= 0:
            raise ValueError("Cache expiration must be greater than zero")
        expires_at = time.time() + seconds
        async with aiosqlite.connect(self.database_path) as connection:
            await self._ensure_table(connection)
            await connection.execute(
                """
                INSERT INTO cache_entries (cache_key, cache_value, expires_at)
                VALUES (?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    cache_value = excluded.cache_value,
                    expires_at = excluded.expires_at
                """,
                (key, str(value), expires_at),
            )
            await connection.commit()

    async def delete(self, *keys: str) -> int:
        if not keys:
            return 0
        placeholders = ", ".join("?" for _ in keys)
        async with aiosqlite.connect(self.database_path) as connection:
            await self._ensure_table(connection)
            cursor = await connection.execute(
                f"DELETE FROM cache_entries WHERE cache_key IN ({placeholders})",
                keys,
            )
            await connection.commit()
            deleted = cursor.rowcount
            await cursor.close()
            return deleted


def create_cache(url: str) -> CacheStore:
    if url.startswith("redis://") or url.startswith("rediss://"):
        return Redis.from_url(url, decode_responses=True)
    if url.startswith("sqlite+aiosqlite://") or url.startswith("sqlite://"):
        database = make_url(url).database
        if not database or database == ":memory:":
            raise ValueError("SQLite cache must use a file database shared by the services")
        return SQLiteCache(Path(database).resolve())
    raise ValueError("Cache URL must use redis://, rediss://, sqlite://, or sqlite+aiosqlite://")
