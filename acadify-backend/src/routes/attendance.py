from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.core.permissions import RoleChecker
from src.db.main import get_session
from src.models.user import User

from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.student_repository import StudentRepository
from src.repositories.subject_repository import SubjectRepository

from src.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
)

from src.services.attendance_service import AttendanceService


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


def get_attendance_service(
    session: AsyncSession = Depends(get_session),
) -> AttendanceService:

    return AttendanceService(
        AttendanceRepository(session),
        EnrollmentRepository(session),
        StudentRepository(session),
        SubjectRepository(session),
    )


@router.post(
    "",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleChecker(["teacher", "admin"]))],
)
async def create_attendance(
    data: AttendanceCreate,
    service: AttendanceService = Depends(get_attendance_service),
):
    return await service.create_attendance(data)


@router.get(
    "/student/{student_id}",
    response_model=list[AttendanceResponse],
)
async def get_student_attendance(
    student_id: UUID,
    service: AttendanceService = Depends(get_attendance_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_student_attendance(student_id)