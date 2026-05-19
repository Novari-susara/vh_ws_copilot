"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.models.schemas import LoginRequest, TokenResponse
from src.services.auth_service import AuthService

router = APIRouter()


def get_auth_service() -> AuthService:
    return AuthService()


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Authenticate user and return JWT token."""
    token = await service.authenticate(credentials.email, credentials.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    """Logout (client-side token removal)."""
    pass


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    service: AuthService = Depends(get_auth_service),
):
    """Refresh an access token."""
    # Implementation would validate refresh token from header
    raise HTTPException(status_code=501, detail="Not implemented in demo")
