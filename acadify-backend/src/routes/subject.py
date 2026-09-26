from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.core.permissions import RoleChecker
from src.db.main import get_session
from src.models.user import User

from src.repositories.subject_repository import SubjectRepository
from src.repositories.teacher_repository import TeacherRepository

from src.schemas.subject import SubjectCreate, SubjectResponse

from src.services.subject_service import SubjectService


router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


def get_subject_service(
    session: AsyncSession = Depends(get_session),
) -> SubjectService:

    return SubjectService(
        SubjectRepository(session),
        TeacherRepository(session),
    )


@router.post(
    "",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleChecker(["admin", "teacher"]))],
)
async def create_subject(
    data: SubjectCreate,
    service: SubjectService = Depends(get_subject_service),
):
    return await service.create_subject(data)


@router.get(
    "",
    response_model=list[SubjectResponse],
)
async def get_subjects(
    service: SubjectService = Depends(get_subject_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_all_subjects()


@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
)
async def get_subject(
    subject_id: UUID,
    service: SubjectService = Depends(get_subject_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_subject(subject_id)