from __future__ import annotations

from OnboardingService.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository | None = None):
        self.repo = repo or UserRepository()
