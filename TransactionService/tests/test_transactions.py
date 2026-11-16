from __future__ import annotations

from decimal import Decimal

from TransactionService.schemas.transaction import InitiateTransactionRequest


def test_initiate_transaction_request_valid() -> None:
    payload = InitiateTransactionRequest(receiver_mobile_number="5551234567", amount=Decimal("42.50"), purpose="Lunch")
    assert payload.amount == Decimal("42.50")
    assert payload.purpose == "Lunch"
