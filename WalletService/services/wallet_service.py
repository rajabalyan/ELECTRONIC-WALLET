from __future__ import annotations

from decimal import Decimal

from WalletService.repositories.wallet_repository import WalletRepository


class WalletService:
    def __init__(self, repo: WalletRepository | None = None):
        self.repo = repo or WalletRepository()

    async def create_wallet(self, user_id: int, mobile_number: str, initial_balance: Decimal = Decimal("100.00")) -> dict:
        return await self.repo.create_wallet(user_id, mobile_number, initial_balance)
