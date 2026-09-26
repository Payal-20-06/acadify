from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.teacher import Teacher


class TeacherRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> Teacher | None:

        statement = select(Teacher).where(
            Teacher.uid == uid
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> Teacher | None:

        statement = select(Teacher).where(
            Teacher.user_id == user_id
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_employee_id(
        self,
        employee_id: str,
    ) -> Teacher | None:

        statement = select(Teacher).where(
            Teacher.employee_id == employee_id
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def create(
        self,
        teacher: Teacher,
    ) -> Teacher:

        self.session.add(teacher)

        await self.session.commit()

        await self.session.refresh(teacher)

        return teacher

    async def update(
        self,
        teacher: Teacher,
    ) -> Teacher:

        self.session.add(teacher)

        await self.session.commit()

        await self.session.refresh(teacher)

        return teacher

    async def delete(
        self,
        teacher: Teacher,
    ) -> None:

        await self.session.delete(teacher)

        await self.session.commit()