from uuid import UUID

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    create_email_verification_token,
)
from src.schemas.auth import SignupRequest, LoginRequest


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def signup(self, data: SignupRequest) -> tuple[User, str]:

        existing_email = await self.user_repository.get_by_email(
            data.email
        )

        if existing_email:
            raise ValueError("Email already registered")

        existing_phone = await self.user_repository.get_by_phone(
            data.phone
        )

        if existing_phone:
            raise ValueError("Phone number already registered")

        name_parts = data.full_name.strip().split()

        first_name = name_parts[0]
        last_name = (
            " ".join(name_parts[1:])
            if len(name_parts) > 1
            else ""
        )

        username = data.email.split("@")[0]

        existing_username = await self.user_repository.get_by_username(
            username
        )

        if existing_username:
            raise ValueError("Username already exists")

        hashed_password = hash_password(data.password)

        user = User(
            username=username,
            email=data.email,
            phone=data.phone,
            first_name=first_name,
            last_name=last_name,
            role=data.role,
            is_verified=False,
            password_hash=hashed_password,
        )

        user = await self.user_repository.create(user)

        verification_token = create_email_verification_token(
            str(user.uid)
        )

        return user, verification_token

    async def login(
        self,
        data: LoginRequest,
    ) -> dict:

        # 1. Find user by email
        user = await self.user_repository.get_by_email(
            data.email
        )

        # 2. Check user exists
        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        # 3. Verify password
        password_valid = verify_password(
            data.password,
            user.password_hash,
        )

        if not password_valid:
            raise ValueError(
                "Invalid email or password"
            )

        # 4. Create access token
        access_token = create_access_token(
            str(user.uid)
        )

        # 5. Create refresh token
        refresh_token = create_refresh_token(
            str(user.uid)
        )

        # 6. Return tokens
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> dict:

        # 1. Decode refresh token
        payload = decode_token(refresh_token)

        # 2. Make sure it is actually a refresh token
        if payload.get("type") != "refresh":
            raise ValueError(
                "Invalid refresh token"
            )

        # 3. Get user ID
        user_id = payload.get("sub")

        if not user_id:
            raise ValueError(
                "Invalid refresh token"
            )

        # 4. Create a new access token
        access_token = create_access_token(
            user_id
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    async def verify_email(
        self,
        token: str,
    ) -> User:

        try:
            payload = decode_token(token)

        except Exception:
            raise ValueError(
                "Invalid or expired verification token"
            )

        # Check token type
        if payload.get("type") != "email_verification":
            raise ValueError(
                "Invalid verification token"
            )

        # Get user ID
        user_id = payload.get("sub")

        if not user_id:
            raise ValueError(
                "Invalid verification token"
            )

        # Find user
        user = await self.user_repository.get_by_uid(
            UUID(user_id)
        )

        if not user:
            raise ValueError(
                "User not found"
            )

        # Already verified
        if user.is_verified:
            return user

        # Verify user
        user.is_verified = True

        # Save changes
        await self.user_repository.update(user)

        return user
