from uuid import UUID

from src.models.subject import Subject
from src.repositories.subject_repository import SubjectRepository
from src.repositories.teacher_repository import TeacherRepository
from src.schemas.subject import SubjectCreate

from src.core.exceptions import (
    SubjectAlreadyExists,
    SubjectNotFound,
    TeacherNotFound,
)


class SubjectService:

    def __init__(
        self,
        subject_repository: SubjectRepository,
        teacher_repository: TeacherRepository,
    ):
        self.subject_repository = subject_repository
        self.teacher_repository = teacher_repository

    async def create_subject(self, data: SubjectCreate) -> Subject:

        teacher_id = data.teacher_id

        teacher = await self.teacher_repository.get_by_uid(teacher_id)

        if not teacher:
            raise TeacherNotFound()

        existing_subject = await self.subject_repository.get_by_code(
            data.code
        )

        if existing_subject:
            raise SubjectAlreadyExists()

        subject = Subject(
            name=data.name,
            code=data.code,
            description=data.description,
            teacher_id=teacher_id,
        )

        return await self.subject_repository.create(subject)

    async def get_subject(self, subject_id: UUID) -> Subject:

        subject = await self.subject_repository.get_by_uid(subject_id)

        if not subject:
            raise SubjectNotFound()

        return subject

    async def get_all_subjects(self) -> list[Subject]:

        return await self.subject_repository.get_all()

    async def get_teacher_subjects(
        self,
        teacher_id: UUID,
    ) -> list[Subject]:

        return await self.subject_repository.get_by_teacher_id(
            teacher_id
        )