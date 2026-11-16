from __future__ import annotations

from decimal import Decimal

from WalletService.repositories.wallet_repository import WalletRepository


async def test_wallet_repository_create() -> None:
    repo = WalletRepository()
    wallet = await repo.create_wallet(1001, "2223334444", Decimal("100.00"))
    assert wallet["user_id"] == 1001
    assert str(wallet["balance"]) == "100.00"
