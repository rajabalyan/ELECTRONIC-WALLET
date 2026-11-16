from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class WalletBalanceResponse(BaseModel):
    user_id: str
    balance: Decimal


class WalletCreationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: int
    mobile_number: str
    initial_balance: Decimal = Field(default=Decimal("100.00"))


class WalletTransferRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    transaction_id: str = Field(..., min_length=1, max_length=80)
    receiver_mobile_number: str = Field(..., min_length=8, max_length=25)
    amount: Decimal = Field(..., gt=0)
    purpose: str = Field(..., min_length=2, max_length=200)
