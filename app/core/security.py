from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
import jwt
from pwdlib import PasswordHash
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status

password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(data: dict) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def generate_refresh_token() -> str:
    """
    Generates a cryptographically secure random refresh token.
    """

    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    """
    Creates an HMAC-SHA256 digest of the refresh token.
    """

    return hmac.new(
        settings.secret_key.encode(),
        token.encode(),
        hashlib.sha256,
    ).hexdigest()


def generate_password_reset_token() -> str:
    return secrets.token_urlsafe(32)


def hash_password_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
