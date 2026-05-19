"""Authentication service — JWT token generation and validation."""

import logging
import os
from datetime import UTC, datetime, timedelta

import jwt

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "demo-secret-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 1


class AuthService:
    """Handles JWT-based authentication."""

    async def authenticate(self, email: str, password: str) -> str | None:
        """Validate credentials and return JWT token."""
        # Demo: accept any email with password 'Demo1234!'
        if password != "Demo1234!":  # noqa: S105  # TODO: Replace with real implementation
            logger.warning("Failed login attempt for %s", email)
            return None

        payload = {
            "sub": email,
            "exp": datetime.now(UTC) + timedelta(hours=TOKEN_EXPIRE_HOURS),
            "iat": datetime.now(UTC),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("Login successful for %s", email)
        return token

    def decode_token(self, token: str) -> dict | None:
        """Decode and validate a JWT token."""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token presented")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token presented")
            return None
