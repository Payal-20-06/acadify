from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.class_schedule import ClassSchedule


class ScheduleRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> ClassSchedule | None:
        statement = select(ClassSchedule).where(
            ClassSchedule.uid == uid
        )

        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_by_teacher_id(
        self,
        teacher_id: UUID,
    ) -> list[ClassSchedule]:
        statement = select(ClassSchedule).where(
            ClassSchedule.teacher_id == teacher_id
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_subject_id(
        self,
        subject_id: UUID,
    ) -> list[ClassSchedule]:
        statement = select(ClassSchedule).where(
            ClassSchedule.subject_id == subject_id
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_all(
        self,
    ) -> list[ClassSchedule]:
        statement = select(ClassSchedule)

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(
        self,
        schedule: ClassSchedule,
    ) -> ClassSchedule:
        self.session.add(schedule)
        await self.session.commit()
        await self.session.refresh(schedule)
        return schedule

    async def update(
        self,
        schedule: ClassSchedule,
    ) -> ClassSchedule:
        self.session.add(schedule)
        await self.session.commit()
        await self.session.refresh(schedule)
        return schedule

    async def delete(
        self,
        schedule: ClassSchedule,
    ) -> None:
        await self.session.delete(schedule)
        await self.session.commit()