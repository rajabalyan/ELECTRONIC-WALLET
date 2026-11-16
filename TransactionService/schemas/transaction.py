from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InitiateTransactionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    receiver_mobile_number: str = Field(..., min_length=8, max_length=25)
    amount: Decimal = Field(..., gt=0)
    purpose: str = Field(..., min_length=2, max_length=200)


class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
