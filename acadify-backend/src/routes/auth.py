from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_current_user
from src.core.permissions import RoleChecker

from src.db.main import get_session
from src.repositories.user_repository import UserRepository


from src.services.auth_service import AuthService
from src.schemas.auth import (
    SignupRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
)
from src.services.email_service import send_verification_email

router = APIRouter(
    prefix="/api/v1/auths",
    tags=["Authentication"],
)

@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED
)
async def signup(
    data: SignupRequest,
    session: AsyncSession = Depends(get_session),
):
    user_repository = UserRepository(session)
    auth_service = AuthService(user_repository)

    user, verification_token = await auth_service.signup(data)
    print("USER EMAIL:", user.email)
    print("SENDING VERIFICATION EMAIL TO:", user.email)

    await send_verification_email(
        user.email,
        verification_token,
    )

    return {
        "message": "Account created successfully. Please check your email to verify your account.",
        "user": {
            "uid": str(user.uid),
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_verified": user.is_verified,
        },
    }
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    user_repository = UserRepository(session)

    auth_service = AuthService(
        user_repository
    )

    tokens = await auth_service.login(data)

    return TokenResponse(**tokens)

@router.post(
    "/refresh",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
):
    user_repository = UserRepository(session)

    auth_service = AuthService(
        user_repository
    )

    result = await auth_service.refresh_access_token(
        data.refresh_token
    )

    return result
@router.get("/me")
async def get_me(
    current_user = Depends(get_current_user),
):
    return {
        "uid": str(current_user.uid),
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_verified": current_user.is_verified,
    }

@router.get(
    "/student-test",
    dependencies=[
        Depends(RoleChecker(["student"]))
    ],
)
async def student_test():
    return {
        "message": "Student access granted"
    }

@router.get(
    "/verify-email",
    response_model=UserResponse,
)
async def verify_email(
    token: str = Query(...),
    session: AsyncSession = Depends(get_session),
):
    user_repository = UserRepository(session)

    auth_service = AuthService(
        user_repository
    )

    user = await auth_service.verify_email(token)

    return UserResponse(
        uid=str(user.uid),
        username=user.username,
        email=user.email,
        phone=user.phone,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        is_verified=user.is_verified,
    )
