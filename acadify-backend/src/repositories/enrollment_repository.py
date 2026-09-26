from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.enrollment import Enrollment


class EnrollmentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uid(
        self,
        uid: UUID,
    ) -> Enrollment | None:

        statement = select(Enrollment).where(
            Enrollment.uid == uid
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_student_and_subject(
        self,
        student_id: UUID,
        subject_id: UUID,
    ) -> Enrollment | None:

        statement = select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.subject_id == subject_id,
        )

        result = await self.session.execute(statement)

        return result.scalars().first()

    async def get_by_student_id(
        self,
        student_id: UUID,
    ) -> list[Enrollment]:

        statement = select(Enrollment).where(
            Enrollment.student_id == student_id
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def get_by_subject_id(
        self,
        subject_id: UUID,
    ) -> list[Enrollment]:

        statement = select(Enrollment).where(
            Enrollment.subject_id == subject_id
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def create(
        self,
        enrollment: Enrollment,
    ) -> Enrollment:

        self.session.add(enrollment)

        await self.session.commit()

        await self.session.refresh(enrollment)

        return enrollment

    async def delete(
        self,
        enrollment: Enrollment,
    ) -> None:

        await self.session.delete(enrollment)

        await self.session.commit()