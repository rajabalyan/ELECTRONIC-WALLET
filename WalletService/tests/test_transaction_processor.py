from __future__ import annotations

from decimal import Decimal

from WalletService.services.transaction_processor import TransactionProcessor


async def test_transaction_processor_rejects_insufficient_funds() -> None:
    processor = TransactionProcessor()
    event = __import__("types").SimpleNamespace(
        event_id="event-1",
        event_type="transaction.initiated",
        payload={"amount": "500.00", "sender_mobile_number": "111", "receiver_mobile_number": "222", "transaction_id": "t-1"},
    )
    try:
        await processor.process_event(event)
    except ValueError:
        return
    raise AssertionError("ValueError not raised")
