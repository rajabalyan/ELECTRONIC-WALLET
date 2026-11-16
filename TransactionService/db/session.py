from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from CommonService.database.session import build_session_factory
from TransactionService.config import settings

_session_factory = build_session_factory(settings.db_url)


def get_session() -> AsyncSession:
    return _session_factory()
