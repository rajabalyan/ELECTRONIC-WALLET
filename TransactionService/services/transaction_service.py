from __future__ import annotations

from TransactionService.repositories.transaction_repository import TransactionRepository


class TransactionService:
    def __init__(self, repo: TransactionRepository | None = None):
        self.repo = repo or TransactionRepository()
