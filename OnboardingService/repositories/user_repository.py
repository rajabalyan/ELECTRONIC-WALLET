from __future__ import annotations

from typing import Any

from sqlalchemy import select

from OnboardingService.db.session import get_session
from OnboardingService.models.user import User


class UserRepository:
    async def get_by_email_or_mobile_or_id(self, email: str, mobile_number: str, identification_value: str) -> dict | None:
        async with get_session() as session:
            result = await session.execute(
                select(User).where((User.email == email) | (User.mobile_number == mobile_number) | (User.identification_value == identification_value))
            )
            user = result.scalar_one_or_none()
            return None if user is None else {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "mobile_number": user.mobile_number,
                "password_hash": user.password_hash,
                "identification_type": user.identification_type,
                "identification_value": user.identification_value,
                "status": user.status,
            }

    async def get_by_id(self, user_id: str | int) -> dict | None:
        async with get_session() as session:
            result = await session.execute(select(User).where(User.id == int(user_id)))
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return {"id": user.id, "email": user.email, "name": user.name, "mobile_number": user.mobile_number, "password_hash": user.password_hash, "identification_type": user.identification_type, "identification_value": user.identification_value, "status": user.status}

    async def get_by_mobile_or_username(self, mobile_number: str) -> dict | None:
        async with get_session() as session:
            result = await session.execute(select(User).where(User.mobile_number == mobile_number))
            user = result.scalar_one_or_none()
            return None if user is None else {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "mobile_number": user.mobile_number,
                "password_hash": user.password_hash,
                "status": user.status,
            }

    async def user_exists(self, username: str) -> bool:
        async with get_session() as session:
            result = await session.execute(select(User.id).where((User.email == username) | (User.mobile_number == username)))
            return result.scalar_one_or_none() is not None

    async def create_user(self, **kwargs: Any) -> dict:
        async with get_session() as session:
            user = User(**kwargs)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return {"id": user.id, "email": user.email, "name": user.name, "mobile_number": user.mobile_number, "status": user.status}
