from uuid import UUID

from src.models.marks import Marks

from src.repositories.marks_repository import MarksRepository
from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.student_repository import StudentRepository
from src.repositories.subject_repository import SubjectRepository

from src.schemas.marks import MarksCreate

from src.core.exceptions import (
    InvalidMarks,
    StudentNotEnrolled,
    StudentNotFound,
    SubjectNotFound,
    MarksNotFound,
)


class MarksService:

    def __init__(
        self,
        marks_repository: MarksRepository,
        enrollment_repository: EnrollmentRepository,
        student_repository: StudentRepository,
        subject_repository: SubjectRepository,
    ):
        self.marks_repository = marks_repository
        self.enrollment_repository = enrollment_repository
        self.student_repository = student_repository
        self.subject_repository = subject_repository

    async def create_marks(
        self,
        data: MarksCreate,
    ) -> Marks:

        student_id = UUID(data.student_id)
        subject_id = UUID(data.subject_id)

        if data.marks_obtained > data.max_marks:
            raise InvalidMarks()

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

        marks = Marks(
            student_id=student_id,
            subject_id=subject_id,
            assessment_type=data.assessment_type,
            marks_obtained=data.marks_obtained,
            max_marks=data.max_marks,
        )

        return await self.marks_repository.create(marks)

    async def get_student_marks(
        self,
        student_id: UUID,
    ) -> list[Marks]:

        student = await self.student_repository.get_by_uid(student_id)

        if not student:
            raise StudentNotFound()

        return await self.marks_repository.get_by_student_id(
            student_id
        )

    async def get_marks(
        self,
        marks_id: UUID,
    ) -> Marks:

        marks = await self.marks_repository.get_by_uid(marks_id)

        if not marks:
            raise MarksNotFound()

        return marks