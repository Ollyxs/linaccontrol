from typing import Any, Union
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from uuid import uuid4
import bcrypt
import logging
import jwt


def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash.decode("utf-8")


def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now(timezone.utc) + (
        expiry
        if expiry is not None
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload["jti"] = str(uuid4())
    payload["refresh"] = refresh
    token = jwt.encode(
        payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return token_data
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None
