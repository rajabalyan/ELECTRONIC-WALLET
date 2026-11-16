from __future__ import annotations

from NotificationService.services.otp_service import OtpService


def test_generate_otp_length() -> None:
    otp = OtpService.generate_otp()
    assert len(otp) == 6
    assert otp.isdigit()
