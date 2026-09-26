from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.student import Student


class StudentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> Student | None:

        statement = select(Student).where(
            Student.uid == uid
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> Student | None:

        statement = select(Student).where(
            Student.user_id == user_id
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_enrollment_number(
        self,
        enrollment_number: str,
    ) -> Student | None:

        statement = select(Student).where(
            Student.enrollment_number
            == enrollment_number
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def create(
        self,
        student: Student,
    ) -> Student:

        self.session.add(student)

        await self.session.commit()

        await self.session.refresh(student)

        return student

    async def update(
        self,
        student: Student,
    ) -> Student:

        self.session.add(student)

        await self.session.commit()

        await self.session.refresh(student)

        return student

    async def delete(
        self,
        student: Student,
    ) -> None:

        await self.session.delete(student)

        await self.session.commit()