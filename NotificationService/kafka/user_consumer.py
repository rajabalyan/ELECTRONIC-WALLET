from __future__ import annotations

from CommonService.kafka.events import EventEnvelope
from NotificationService.services.email_service import EmailService


async def handle_user_created(msg: dict) -> None:
    event = EventEnvelope.model_validate(msg)
    payload = event.payload
    email_service = EmailService()
    await email_service.send_welcome_email(payload["email"], payload["name"])
