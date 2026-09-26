from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.announcement import Announcement


class AnnouncementRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> Announcement | None:
        statement = select(Announcement).where(
            Announcement.uid == uid
        )

        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_all(
        self,
    ) -> list[Announcement]:
        statement = select(Announcement).order_by(
            Announcement.created_at.desc()
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_creator(
        self,
        user_id: UUID,
    ) -> list[Announcement]:
        statement = select(Announcement).where(
            Announcement.created_by == user_id
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(
        self,
        announcement: Announcement,
    ) -> Announcement:
        self.session.add(announcement)
        await self.session.commit()
        await self.session.refresh(announcement)
        return announcement

    async def delete(
        self,
        announcement: Announcement,
    ) -> None:
        await self.session.delete(announcement)
        await self.session.commit()