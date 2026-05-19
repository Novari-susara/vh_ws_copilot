"""User management service."""

from typing import List, Optional, Dict
from datetime import datetime
import uuid
import logging

from src.models.schemas import UserCreate, UserResponse

logger = logging.getLogger(__name__)

_users: Dict[str, dict] = {}
_users_by_email: Dict[str, str] = {}


class UserService:
    """Handles user CRUD operations."""

    async def list_users(self) -> List[UserResponse]:
        return [UserResponse(**u) for u in _users.values()]

    async def get_user(self, user_id: str) -> Optional[UserResponse]:
        user = _users.get(user_id)
        return UserResponse(**user) if user else None

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
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
            "created_at": datetime.utcnow(),
            # NOTE: In production, hash the password! Never store plaintext.
            "_password_hash": f"hashed_{user.password}",
        }
        _users[user_id] = user_dict
        _users_by_email[user.email] = user_id
        logger.info("User created: %s", user_id)
        return UserResponse(**user_dict)
