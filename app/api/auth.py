from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import (
    get_auth_service,
    get_current_user,
)
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.register(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.login(
        email=request.email,
        password=request.password,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post(
    "/token",
    response_model=TokenResponse,
)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    OAuth2 compatible endpoint used by Swagger UI.

    OAuth2 uses the field name 'username' even when
    you're actually logging in with an email address.
    """

    return auth_service.login(
        email=form_data.username,
        password=form_data.password,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):

    return auth_service.refresh(request.refresh_token)
