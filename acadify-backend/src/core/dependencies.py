from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import decode_token
from src.db.main import get_session
from src.repositories.user_repository import UserRepository
from uuid import UUID


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials

    try:
        payload = decode_token(token)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # Make sure this is an access token
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    repository = UserRepository(session)

    user = await repository.get_by_uid(
        UUID(user_id)
    )

    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
    )

    if not user.is_verified:
       raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Please verify your email before accessing this resource",
    )

    return user 