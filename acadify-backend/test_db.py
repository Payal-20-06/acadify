import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings


async def test_connection():
    engine = create_async_engine(settings.DATABASE_URL)

    try:
        async with engine.connect():
            print("DATABASE CONNECTED SUCCESSFULLY")
    finally:
        await engine.dispose()


asyncio.run(test_connection())