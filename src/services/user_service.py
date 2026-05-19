"""User management service."""

import logging
import uuid
from datetime import UTC, datetime

from src.models.schemas import UserCreate, UserResponse

logger = logging.getLogger(__name__)

_users: dict[str, dict] = {}
_users_by_email: dict[str, str] = {}


class UserService:
    """Handles user CRUD operations."""

    async def list_users(self) -> list[UserResponse]:
        return [UserResponse(**u) for u in _users.values()]

    async def get_user(self, user_id: str) -> UserResponse | None:
        user = _users.get(user_id)
        return UserResponse(**user) if user else None

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        user_id = _users_by_email.get(email)
        if not user_id:
            return None
        return await self.get_user(user_id)

    async def create_user(self, user: UserCreate) -> UserResponse:
        user_id = str(uuid.uuid4())
        user_dict = {
            "id": user_id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": datetime.now(UTC),
            # NOTE: In production, hash the password! Never store plaintext.
            "_password_hash": f"hashed_{user.password}",
        }
        _users[user_id] = user_dict
        _users_by_email[user.email] = user_id
        logger.info("User created: %s", user_id)
        return UserResponse(**user_dict)
