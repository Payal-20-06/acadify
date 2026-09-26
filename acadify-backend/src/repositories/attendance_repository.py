from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.attendance import Attendance


class AttendanceRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> Attendance | None:

        statement = select(Attendance).where(
            Attendance.uid == uid
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_student_subject_date(
        self,
        student_id: UUID,
        subject_id: UUID,
        attendance_date: date,
    ) -> Attendance | None:

        statement = select(Attendance).where(
            Attendance.student_id == student_id,
            Attendance.subject_id == subject_id,
            Attendance.date == attendance_date,
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_student_id(
        self,
        student_id: UUID,
    ) -> list[Attendance]:

        statement = select(Attendance).where(
            Attendance.student_id == student_id
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def get_by_subject_id(
        self,
        subject_id: UUID,
    ) -> list[Attendance]:

        statement = select(Attendance).where(
            Attendance.subject_id == subject_id
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def create(
        self,
        attendance: Attendance,
    ) -> Attendance:

        self.session.add(attendance)

        await self.session.commit()

        await self.session.refresh(attendance)

        return attendance

    async def update(
        self,
        attendance: Attendance,
    ) -> Attendance:

        self.session.add(attendance)

        await self.session.commit()

        await self.session.refresh(attendance)

        return attendance

    async def delete(
        self,
        attendance: Attendance,
    ) -> None:

        await self.session.delete(attendance)

        await self.session.commit()