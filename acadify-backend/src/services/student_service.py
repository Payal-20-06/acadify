from uuid import UUID

from src.models.student import Student
from src.repositories.student_repository import StudentRepository
from src.repositories.user_repository import UserRepository
from src.schemas.student import StudentCreate

from src.core.exceptions import (
    StudentAlreadyExists,
    StudentNotFound,
)


class StudentService:

    def __init__(
        self,
        student_repository: StudentRepository,
        user_repository: UserRepository,
    ):
        self.student_repository = student_repository
        self.user_repository = user_repository

    async def create_student(self, data: StudentCreate) -> Student:

        user_id = UUID(data.user_id)

        user = await self.user_repository.get_by_uid(user_id)

        if not user:
            raise StudentNotFound()

        existing_student = await self.student_repository.get_by_user_id(user_id)

        if existing_student:
            raise StudentAlreadyExists()

        existing_enrollment = (
            await self.student_repository.get_by_enrollment_number(
                data.enrollment_number
            )
        )

        if existing_enrollment:
            raise StudentAlreadyExists()

        student = Student(
            user_id=user_id,
            enrollment_number=data.enrollment_number,
            course=data.course,
            semester=data.semester,
        )

        return await self.student_repository.create(student)

    async def get_student(self, student_id: UUID) -> Student:

        student = await self.student_repository.get_by_uid(student_id)

        if not student:
            raise StudentNotFound()

        return student

    async def get_student_by_user(self, user_id: UUID) -> Student:

        student = await self.student_repository.get_by_user_id(user_id)

        if not student:
            raise StudentNotFound()

        return student