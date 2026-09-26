from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.core.permissions import RoleChecker
from src.db.main import get_session
from src.models.user import User

from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.student_repository import StudentRepository
from src.repositories.subject_repository import SubjectRepository

from src.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
)

from src.services.enrollment_service import EnrollmentService


router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"],
)


def get_enrollment_service(
    session: AsyncSession = Depends(get_session),
) -> EnrollmentService:

    return EnrollmentService(
        EnrollmentRepository(session),
        StudentRepository(session),
        SubjectRepository(session),
    )


@router.post(
    "",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleChecker(["admin", "teacher"]))],
)
async def create_enrollment(
    data: EnrollmentCreate,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return await service.create_enrollment(data)


@router.get(
    "/student/{student_id}",
    response_model=list[EnrollmentResponse],
)
async def get_student_enrollments(
    student_id: UUID,
    service: EnrollmentService = Depends(get_enrollment_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_student_enrollments(student_id)


@router.delete(
    "/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(["admin", "teacher"]))],
)
async def delete_enrollment(
    enrollment_id: UUID,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    await service.delete_enrollment(enrollment_id)