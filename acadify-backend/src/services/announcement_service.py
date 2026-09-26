from uuid import UUID

from src.models.announcement import Announcement

from src.repositories.announcement_repository import (
    AnnouncementRepository,
)

from src.schemas.announcement import AnnouncementCreate

from src.core.exceptions import AnnouncementNotFound


class AnnouncementService:

    def __init__(
        self,
        announcement_repository: AnnouncementRepository,
    ):
        self.announcement_repository = announcement_repository

    async def create_announcement(
        self,
        data: AnnouncementCreate,
        creator_id: UUID,
    ) -> Announcement:

        announcement = Announcement(
            title=data.title,
            content=data.content,
            created_by=creator_id,
        )

        return await self.announcement_repository.create(
            announcement
        )

    async def get_announcement(
        self,
        announcement_id: UUID,
    ) -> Announcement:

        announcement = (
            await self.announcement_repository.get_by_uid(
                announcement_id
            )
        )

        if not announcement:
            raise AnnouncementNotFound()

        return announcement

    async def get_all_announcements(
        self,
    ) -> list[Announcement]:

        return await self.announcement_repository.get_all()

    async def get_my_announcements(
        self,
        creator_id: UUID,
    ) -> list[Announcement]:

        return await self.announcement_repository.get_by_creator(
            creator_id
        )

    async def delete_announcement(
        self,
        announcement_id: UUID,
    ) -> None:

        announcement = (
            await self.announcement_repository.get_by_uid(
                announcement_id
            )
        )

        if not announcement:
            raise AnnouncementNotFound()

        await self.announcement_repository.delete(
            announcement
        )