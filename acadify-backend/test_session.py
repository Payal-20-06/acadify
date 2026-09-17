import asyncio

from sqlalchemy import text

from src.db.main import async_session


async def test_session():
    async with async_session() as session:

        result = await session.execute(
            text("SELECT current_database()")
        )

        database_name = result.scalar_one()

        print(
            f"Connected to database: {database_name}"
        )


asyncio.run(test_session())