from __future__ import annotations

from OnboardingService.schemas.auth import OtpValidationRequest


def test_otp_validation_request() -> None:
    payload = OtpValidationRequest(email="alice@example.com", otp="123456")
    assert payload.otp == "123456"
