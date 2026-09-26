from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.core.permissions import RoleChecker
from src.db.main import get_session
from src.models.user import User

from src.repositories.schedule_repository import ScheduleRepository
from src.repositories.subject_repository import SubjectRepository
from src.repositories.teacher_repository import TeacherRepository

from src.schemas.schedule import ScheduleCreate, ScheduleResponse

from src.services.schedule_service import ScheduleService


router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"],
)


def get_schedule_service(
    session: AsyncSession = Depends(get_session),
) -> ScheduleService:

    return ScheduleService(
        ScheduleRepository(session),
        SubjectRepository(session),
        TeacherRepository(session),
    )


@router.post(
    "",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleChecker(["teacher", "admin"]))],
)
async def create_schedule(
    data: ScheduleCreate,
    service: ScheduleService = Depends(get_schedule_service),
):
    return await service.create_schedule(data)


@router.get(
    "",
    response_model=list[ScheduleResponse],
)
async def get_schedules(
    service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_all_schedules()


@router.get(
    "/teacher/{teacher_id}",
    response_model=list[ScheduleResponse],
)
async def get_teacher_schedule(
    teacher_id: UUID,
    service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_teacher_schedule(teacher_id)


@router.get(
    "/subject/{subject_id}",
    response_model=list[ScheduleResponse],
)
async def get_subject_schedule(
    subject_id: UUID,
    service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_subject_schedule(subject_id)


@router.get(
    "/{schedule_id}",
    response_model=ScheduleResponse,
)
async def get_schedule(
    schedule_id: UUID,
    service: ScheduleService = Depends(get_schedule_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_schedule(schedule_id)


@router.delete(
    "/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(["teacher", "admin"]))],
)
async def delete_schedule(
    schedule_id: UUID,
    service: ScheduleService = Depends(get_schedule_service),
):
    await service.delete_schedule(schedule_id)