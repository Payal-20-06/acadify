import redis.asyncio as redis

from src.core.config import settings


def get_redis_client():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )


async def revoke_session(session_id: str, expires_in: int):
    client = get_redis_client()

    try:
        await client.setex(
            f"revoked_session:{session_id}",
            expires_in,
            "true",
        )
    finally:
        await client.aclose()


async def is_session_revoked(session_id: str) -> bool:
    client = get_redis_client()

    try:
        result = await client.get(
            f"revoked_session:{session_id}"
        )
        return result is not None
    finally:
        await client.aclose()