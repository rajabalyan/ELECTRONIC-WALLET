from __future__ import annotations

from fastapi import HTTPException


class DomainError(Exception):
    """Base application error."""


class NotFoundError(DomainError):
    pass


class DuplicateResourceError(DomainError):
    pass


class InvalidCredentialsError(DomainError):
    pass


class InvalidOperationError(DomainError):
    pass


def raise_http_error(status_code: int, code: str, message: str):
    raise HTTPException(status_code=status_code, detail={"code": code, "message": message})
