from datetime import date
from uuid import UUID

from src.models.attendance import Attendance

from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.student_repository import StudentRepository
from src.repositories.subject_repository import SubjectRepository

from src.schemas.attendance import AttendanceCreate

from src.core.exceptions import (
    AttendanceAlreadyExists,
    AttendanceNotFound,
    StudentNotEnrolled,
    StudentNotFound,
    SubjectNotFound,
)


class AttendanceService:

    def __init__(
        self,
        attendance_repository: AttendanceRepository,
        enrollment_repository: EnrollmentRepository,
        student_repository: StudentRepository,
        subject_repository: SubjectRepository,
    ):
        self.attendance_repository = attendance_repository
        self.enrollment_repository = enrollment_repository
        self.student_repository = student_repository
        self.subject_repository = subject_repository

    async def create_attendance(
        self,
        data: AttendanceCreate,
    ) -> Attendance:

        student_id = UUID(data.student_id)
        subject_id = UUID(data.subject_id)

        student = await self.student_repository.get_by_uid(student_id)

        if not student:
            raise StudentNotFound()

        subject = await self.subject_repository.get_by_uid(subject_id)

        if not subject:
            raise SubjectNotFound()

        enrollment = (
            await self.enrollment_repository
            .get_by_student_and_subject(
                student_id,
                subject_id,
            )
        )

        if not enrollment:
            raise StudentNotEnrolled()

        existing = (
            await self.attendance_repository
            .get_by_student_subject_date(
                student_id,
                subject_id,
                data.date,
            )
        )

        if existing:
            raise AttendanceAlreadyExists()

        attendance = Attendance(
            student_id=student_id,
            subject_id=subject_id,
            date=data.date,
            is_present=data.is_present,
        )

        return await self.attendance_repository.create(attendance)

    async def get_student_attendance(
        self,
        student_id: UUID,
    ) -> list[Attendance]:

        student = await self.student_repository.get_by_uid(student_id)

        if not student:
            raise StudentNotFound()

        return await self.attendance_repository.get_by_student_id(
            student_id
        )

    async def update_attendance(
        self,
        attendance_id: UUID,
        is_present: bool,
    ) -> Attendance:

        attendance = await self.attendance_repository.get_by_uid(
            attendance_id
        )

        if not attendance:
            raise AttendanceNotFound()

        attendance.is_present = is_present

        return await self.attendance_repository.update(attendance)