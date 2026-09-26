from uuid import UUID, uuid4

from src.models.user import User
from src.repositories.user_repository import UserRepository

from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    create_email_verification_token,
    create_password_reset_token,
)

from src.schemas.auth import (
    SignupRequest,
    LoginRequest,
)

from src.core.exceptions import (
    InvalidCredentials,
    EmailAlreadyRegistered,
    PhoneAlreadyRegistered,
    UsernameAlreadyExists,
    InvalidVerificationToken,
    InvalidRefreshToken,
    InvalidPasswordResetToken,
)

from src.db.redis import is_session_revoked

from src.worker.email_tasks import (
    send_verification_email_task,
    send_password_reset_email_task,
)


class AuthService:

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def signup(
        self,
        data: SignupRequest,
    ) -> tuple[User, str]:

        existing_email = await self.user_repository.get_by_email(
            data.email
        )

        if existing_email:
            raise EmailAlreadyRegistered()

        existing_phone = await self.user_repository.get_by_phone(
            data.phone
        )

        if existing_phone:
            raise PhoneAlreadyRegistered()

        name_parts = data.full_name.strip().split()

        first_name = name_parts[0]

        last_name = (
            " ".join(name_parts[1:])
            if len(name_parts) > 1
            else ""
        )

        username = data.email.split("@")[0]

        existing_username = (
            await self.user_repository.get_by_username(
                username
            )
        )

        if existing_username:
            raise UsernameAlreadyExists()

        hashed_password = hash_password(
            data.password
        )

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

        # Create verification token
        verification_token = create_email_verification_token(
            str(user.uid)
        )

        # Send token to Celery.
        # The email service will build the verification URL.
        send_verification_email_task.delay(
            user.email,
            verification_token,
        )

        return user, verification_token

    async def login(
        self,
        data: LoginRequest,
    ) -> dict:

        user = await self.user_repository.get_by_email(
            data.email
        )

        if not user:
            raise InvalidCredentials()

        password_valid = verify_password(
            data.password,
            user.password_hash,
        )

        if not password_valid:
            raise InvalidCredentials()

        # One session ID for the access + refresh token pair
        session_id = str(uuid4())

        access_token = create_access_token(
            str(user.uid),
            session_id,
        )

        refresh_token = create_refresh_token(
            str(user.uid),
            session_id,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> dict:

        try:
            payload = decode_token(refresh_token)

        except Exception:
            raise InvalidRefreshToken()

        if payload.get("type") != "refresh":
            raise InvalidRefreshToken()

        user_id = payload.get("sub")
        session_id = payload.get("sid")

        if not user_id or not session_id:
            raise InvalidRefreshToken()

        # Check whether the session has been revoked
        if await is_session_revoked(session_id):
            raise InvalidRefreshToken()

        try:
            user = await self.user_repository.get_by_uid(
                UUID(user_id)
            )

        except ValueError:
            raise InvalidRefreshToken()

        if not user:
            raise InvalidRefreshToken()

        access_token = create_access_token(
            user_id,
            session_id,
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
            raise InvalidVerificationToken()

        if payload.get("type") != "email_verification":
            raise InvalidVerificationToken()

        user_id = payload.get("sub")

        if not user_id:
            raise InvalidVerificationToken()

        try:
            user = await self.user_repository.get_by_uid(
                UUID(user_id)
            )

        except ValueError:
            raise InvalidVerificationToken()

        if not user:
            raise InvalidVerificationToken()

        # Already verified
        if user.is_verified:
            return user

        user.is_verified = True

        await self.user_repository.update(user)

        return user

    async def forgot_password(
        self,
        email: str,
    ) -> str | None:

        user = await self.user_repository.get_by_email(
            email
        )

        if not user:
            return None

        # Create password reset token
        reset_token = create_password_reset_token(
            str(user.uid)
        )

        # Send token to Celery.
        # The email service will build the reset URL.
        send_password_reset_email_task.delay(
            user.email,
            reset_token,
        )

        return reset_token

    async def reset_password(
        self,
        token: str,
        new_password: str,
    ) -> None:

        try:
            payload = decode_token(token)

        except Exception:
            raise InvalidPasswordResetToken()

        if payload.get("type") != "password_reset":
            raise InvalidPasswordResetToken()

        user_id = payload.get("sub")

        if not user_id:
            raise InvalidPasswordResetToken()

        try:
            user = await self.user_repository.get_by_uid(
                UUID(user_id)
            )

        except ValueError:
            raise InvalidPasswordResetToken()

        if not user:
            raise InvalidPasswordResetToken()

        user.password_hash = hash_password(
            new_password
        )

        await self.user_repository.update(user)