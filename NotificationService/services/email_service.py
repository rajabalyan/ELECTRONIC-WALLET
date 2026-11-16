from __future__ import annotations

import logging

import aiosmtplib
from email.message import EmailMessage

from NotificationService.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    async def send_otp(self, email: str, otp: str) -> None:
        if settings.email_mode.lower() == "development":
            logger.info("Development-only email mode active; OTP was not disclosed in logs for %s", email)
            return
        msg = EmailMessage()
        msg["Subject"] = "Your OTP code"
        msg["From"] = settings.smtp_from
        msg["To"] = email
        msg.set_content(f"Your OTP is {otp}. It is valid for 5 minutes.")
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_username or None,
            password=settings.smtp_password or None,
            use_tls=settings.smtp_use_tls,
        )

    async def send_welcome_email(self, email: str, name: str) -> None:
        if settings.email_mode.lower() == "development":
            logger.info("Development-only email mode active; welcome email stubbed for %s", email)
            return
        msg = EmailMessage()
        msg["Subject"] = "Welcome to E-Wallet"
        msg["From"] = settings.smtp_from
        msg["To"] = email
        msg.set_content(f"Welcome {name}! Your wallet has been created.")
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_username or None,
            password=settings.smtp_password or None,
            use_tls=settings.smtp_use_tls,
        )
