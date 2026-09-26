from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.core.permissions import RoleChecker
from src.db.main import get_session
from src.models.user import User

from src.repositories.announcement_repository import (
    AnnouncementRepository,
)

from src.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
)

from src.services.announcement_service import AnnouncementService


router = APIRouter(
    prefix="/announcements",
    tags=["Announcements"],
)


def get_announcement_service(
    session: AsyncSession = Depends(get_session),
) -> AnnouncementService:

    return AnnouncementService(
        AnnouncementRepository(session)
    )


@router.post(
    "",
    response_model=AnnouncementResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleChecker(["teacher", "admin"]))],
)
async def create_announcement(
    data: AnnouncementCreate,
    current_user: User = Depends(get_current_user),
    service: AnnouncementService = Depends(
        get_announcement_service
    ),
):
    return await service.create_announcement(
        data,
        current_user.uid,
    )


@router.get(
    "",
    response_model=list[AnnouncementResponse],
)
async def get_announcements(
    service: AnnouncementService = Depends(
        get_announcement_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await service.get_all_announcements()


@router.get(
    "/{announcement_id}",
    response_model=AnnouncementResponse,
)
async def get_announcement(
    announcement_id: UUID,
    service: AnnouncementService = Depends(
        get_announcement_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await service.get_announcement(announcement_id)


@router.delete(
    "/{announcement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(["teacher", "admin"]))],
)
async def delete_announcement(
    announcement_id: UUID,
    service: AnnouncementService = Depends(
        get_announcement_service
    ),
):
    await service.delete_announcement(announcement_id)