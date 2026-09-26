from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.marks import Marks


class MarksRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> Marks | None:
        statement = select(Marks).where(
            Marks.uid == uid
        )

        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_by_student_id(
        self,
        student_id: UUID,
    ) -> list[Marks]:
        statement = select(Marks).where(
            Marks.student_id == student_id
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_subject_id(
        self,
        subject_id: UUID,
    ) -> list[Marks]:
        statement = select(Marks).where(
            Marks.subject_id == subject_id
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_student_subject(
        self,
        student_id: UUID,
        subject_id: UUID,
    ) -> list[Marks]:
        statement = select(Marks).where(
            Marks.student_id == student_id,
            Marks.subject_id == subject_id,
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(
        self,
        marks: Marks,
    ) -> Marks:
        self.session.add(marks)
        await self.session.commit()
        await self.session.refresh(marks)
        return marks

    async def update(
        self,
        marks: Marks,
    ) -> Marks:
        self.session.add(marks)
        await self.session.commit()
        await self.session.refresh(marks)
        return marks

    async def delete(
        self,
        marks: Marks,
    ) -> None:
        await self.session.delete(marks)
        await self.session.commit()