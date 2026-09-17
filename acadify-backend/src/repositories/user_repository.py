from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models import user
from src.models.user import User


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = select(User).where(
            User.email == email
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_phone(
        self,
        phone: str,
    ) -> User | None:

        statement = select(User).where(
            User.phone == phone
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:

        statement = select(User).where(
            User.username == username
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> User | None:

        statement = select(User).where(
            User.uid == uid
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def create(
        self,
        user: User,
    ) -> User:

        self.session.add(user)

        await self.session.commit()

        await self.session.refresh(user)

        return user

    async def update(
    self,
    user: User,
    ) -> User:

       self.session.add(user)

       await self.session.commit()

       await self.session.refresh(user)

       return user