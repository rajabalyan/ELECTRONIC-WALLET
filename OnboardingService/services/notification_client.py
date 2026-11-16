from __future__ import annotations

import httpx


class NotificationClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def send_otp(self, email: str) -> dict:
        url = f"{self.base_url}/otp/send/otp/{email}"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url)
            response.raise_for_status()
            return response.json()

    async def validate_otp(self, email: str, otp: str) -> dict:
        url = f"{self.base_url}/otp/validate"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json={"email": email, "otp": otp})
            return response.json()
