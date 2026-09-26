from uuid import UUID

from src.models.enrollment import Enrollment

from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.student_repository import StudentRepository
from src.repositories.subject_repository import SubjectRepository

from src.schemas.enrollment import EnrollmentCreate

from src.core.exceptions import (
    EnrollmentAlreadyExists,
    EnrollmentNotFound,
    StudentNotFound,
    SubjectNotFound,
)


class EnrollmentService:

    def __init__(
        self,
        enrollment_repository: EnrollmentRepository,
        student_repository: StudentRepository,
        subject_repository: SubjectRepository,
    ):
        self.enrollment_repository = enrollment_repository
        self.student_repository = student_repository
        self.subject_repository = subject_repository

    async def create_enrollment(
        self,
        data: EnrollmentCreate,
    ) -> Enrollment:

        student_id = UUID(data.student_id)
        subject_id = UUID(data.subject_id)

        student = await self.student_repository.get_by_uid(student_id)

        if not student:
            raise StudentNotFound()

        subject = await self.subject_repository.get_by_uid(subject_id)

        if not subject:
            raise SubjectNotFound()

        existing = (
            await self.enrollment_repository
            .get_by_student_and_subject(
                student_id,
                subject_id,
            )
        )

        if existing:
            raise EnrollmentAlreadyExists()

        enrollment = Enrollment(
            student_id=student_id,
            subject_id=subject_id,
        )

        return await self.enrollment_repository.create(enrollment)

    async def get_student_enrollments(
        self,
        student_id: UUID,
    ) -> list[Enrollment]:

        student = await self.student_repository.get_by_uid(student_id)

        if not student:
            raise StudentNotFound()

        return await self.enrollment_repository.get_by_student_id(
            student_id
        )

    async def delete_enrollment(
        self,
        enrollment_id: UUID,
    ) -> None:

        enrollment = await self.enrollment_repository.get_by_uid(
            enrollment_id
        )

        if not enrollment:
            raise EnrollmentNotFound()

        await self.enrollment_repository.delete(enrollment)