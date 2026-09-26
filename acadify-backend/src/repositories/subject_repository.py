from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.subject import Subject


class SubjectRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> Subject | None:

        statement = select(Subject).where(
            Subject.uid == uid
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_code(
        self,
        code: str,
    ) -> Subject | None:

        statement = select(Subject).where(
            Subject.code == code
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_teacher_id(
        self,
        teacher_id: UUID,
    ) -> list[Subject]:

        statement = select(Subject).where(
            Subject.teacher_id == teacher_id
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def get_all(self) -> list[Subject]:

        statement = select(Subject)

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def create(
        self,
        subject: Subject,
    ) -> Subject:

        self.session.add(subject)

        await self.session.commit()

        await self.session.refresh(subject)

        return subject

    async def update(
        self,
        subject: Subject,
    ) -> Subject:

        self.session.add(subject)

        await self.session.commit()

        await self.session.refresh(subject)

        return subject

    async def delete(
        self,
        subject: Subject,
    ) -> None:

        await self.session.delete(subject)

        await self.session.commit()