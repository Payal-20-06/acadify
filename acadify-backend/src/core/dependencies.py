from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import decode_token
from src.db.main import get_session
from src.db.redis import is_session_revoked
from src.repositories.user_repository import UserRepository

from src.core.exceptions import (
    InvalidToken,
    AccessTokenRequired,
    TokenRevoked,
    UserNotFound,
    EmailNotVerified,
)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials

    # 1. Decode JWT
    try:
        payload = decode_token(token)

    except Exception:
        raise InvalidToken()

    # 2. Make sure this is an access token
    if payload.get("type") != "access":
        raise AccessTokenRequired()

    # 3. Get session ID
    session_id = payload.get("sid")

    if not session_id:
        raise InvalidToken()

    # 4. Check Redis
    if await is_session_revoked(session_id):
        raise TokenRevoked()

    # 5. Get user ID
    user_id = payload.get("sub")

    if not user_id:
        raise InvalidToken()

    # 6. Find user
    repository = UserRepository(session)

    try:
        user = await repository.get_by_uid(
            UUID(user_id)
        )
    except ValueError:
        raise InvalidToken()

    if not user:
        raise UserNotFound()

    # 7. Check email verification
    if not user.is_verified:
        raise EmailNotVerified()

    return user