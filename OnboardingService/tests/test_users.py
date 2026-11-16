from __future__ import annotations

from datetime import date

from OnboardingService.schemas.user import CreateUserRequest


def test_create_user_request_valid() -> None:
    payload = CreateUserRequest(
        name="Alice",
        email="alice@example.com",
        mobile_number="1234567890",
        date_of_birth=date(2000, 1, 1),
        password="strong-password",
        identification_type="NATIONAL_ID",
        identification_value="AB123456",
    )
    assert payload.email == "alice@example.com"
    assert payload.mobile_number == "1234567890"
