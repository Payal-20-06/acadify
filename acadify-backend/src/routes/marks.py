from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.core.permissions import RoleChecker
from src.db.main import get_session
from src.models.user import User

from src.repositories.marks_repository import MarksRepository
from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.student_repository import StudentRepository
from src.repositories.subject_repository import SubjectRepository

from src.schemas.marks import MarksCreate, MarksResponse

from src.services.marks_service import MarksService


router = APIRouter(
    prefix="/marks",
    tags=["Marks"],
)


def get_marks_service(
    session: AsyncSession = Depends(get_session),
) -> MarksService:

    return MarksService(
        MarksRepository(session),
        EnrollmentRepository(session),
        StudentRepository(session),
        SubjectRepository(session),
    )


@router.post(
    "",
    response_model=MarksResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleChecker(["teacher", "admin"]))],
)
async def create_marks(
    data: MarksCreate,
    service: MarksService = Depends(get_marks_service),
):
    return await service.create_marks(data)


@router.get(
    "/student/{student_id}",
    response_model=list[MarksResponse],
)
async def get_student_marks(
    student_id: UUID,
    service: MarksService = Depends(get_marks_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_student_marks(student_id)


@router.get(
    "/{marks_id}",
    response_model=MarksResponse,
)
async def get_marks(
    marks_id: UUID,
    service: MarksService = Depends(get_marks_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_marks(marks_id)