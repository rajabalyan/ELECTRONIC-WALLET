from __future__ import annotations

import random


class OtpService:
    @staticmethod
    def generate_otp() -> str:
        return str(random.randint(100000, 999999))
