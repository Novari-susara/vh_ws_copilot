"""Users API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.models.schemas import UserCreate, UserResponse
from src.services.user_service import UserService
from src.utils.auth import get_current_user

router = APIRouter()


def get_user_service() -> UserService:
    return UserService()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Get the current authenticated user's profile."""
    user = await service.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[UserResponse])
async def list_users(
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """List all users (admin only in production)."""
    return await service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Get a specific user by ID."""
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """Register a new user."""
    existing = await service.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    return await service.create_user(user)
