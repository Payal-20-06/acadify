from uuid import UUID

from src.models.teacher import Teacher
from src.repositories.teacher_repository import TeacherRepository
from src.repositories.user_repository import UserRepository
from src.schemas.teacher import TeacherCreate

from src.core.exceptions import (
    TeacherAlreadyExists,
    TeacherNotFound,
)


class TeacherService:

    def __init__(
        self,
        teacher_repository: TeacherRepository,
        user_repository: UserRepository,
    ):
        self.teacher_repository = teacher_repository
        self.user_repository = user_repository

    async def create_teacher(self, data: TeacherCreate) -> Teacher:

        user_id = UUID(data.user_id)

        user = await self.user_repository.get_by_uid(user_id)

        if not user:
            raise TeacherNotFound()

        existing_teacher = await self.teacher_repository.get_by_user_id(user_id)

        if existing_teacher:
            raise TeacherAlreadyExists()

        existing_employee = (
            await self.teacher_repository.get_by_employee_id(
                data.employee_id
            )
        )

        if existing_employee:
            raise TeacherAlreadyExists()

        teacher = Teacher(
            user_id=user_id,
            employee_id=data.employee_id,
            department=data.department,
            designation=data.designation,
        )

        return await self.teacher_repository.create(teacher)

    async def get_teacher(self, teacher_id: UUID) -> Teacher:

        teacher = await self.teacher_repository.get_by_uid(teacher_id)

        if not teacher:
            raise TeacherNotFound()

        return teacher

    async def get_teacher_by_user(self, user_id: UUID) -> Teacher:

        teacher = await self.teacher_repository.get_by_user_id(user_id)

        if not teacher:
            raise TeacherNotFound()

        return teacher