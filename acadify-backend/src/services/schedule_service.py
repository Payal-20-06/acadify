from uuid import UUID

from src.models.class_schedule import ClassSchedule

from src.repositories.schedule_repository import ScheduleRepository
from src.repositories.subject_repository import SubjectRepository
from src.repositories.teacher_repository import TeacherRepository

from src.schemas.schedule import ScheduleCreate

from src.core.exceptions import (
    ScheduleConflict,
    ScheduleNotFound,
    SubjectNotFound,
    TeacherNotFound,
)


class ScheduleService:

    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        subject_repository: SubjectRepository,
        teacher_repository: TeacherRepository,
    ):
        self.schedule_repository = schedule_repository
        self.subject_repository = subject_repository
        self.teacher_repository = teacher_repository

    async def create_schedule(
        self,
        data: ScheduleCreate,
    ) -> ClassSchedule:

        subject_id = UUID(data.subject_id)
        teacher_id = UUID(data.teacher_id)

        # Validate subject
        subject = await self.subject_repository.get_by_uid(subject_id)

        if not subject:
            raise SubjectNotFound()

        # Validate teacher
        teacher = await self.teacher_repository.get_by_uid(teacher_id)

        if not teacher:
            raise TeacherNotFound()

        # Validate time
        if data.start_time >= data.end_time:
            raise ScheduleConflict()

        # Get teacher's existing schedules
        existing_schedules = (
            await self.schedule_repository.get_by_teacher_id(
                teacher_id
            )
        )

        # Check for time conflict
        for schedule in existing_schedules:

            if schedule.day_of_week != data.day_of_week:
                continue

            if (
                data.start_time < schedule.end_time
                and data.end_time > schedule.start_time
            ):
                raise ScheduleConflict()

        schedule = ClassSchedule(
            subject_id=subject_id,
            teacher_id=teacher_id,
            day_of_week=data.day_of_week,
            start_time=data.start_time,
            end_time=data.end_time,
            room=data.room,
        )

        return await self.schedule_repository.create(schedule)

    async def get_schedule(
        self,
        schedule_id: UUID,
    ) -> ClassSchedule:

        schedule = await self.schedule_repository.get_by_uid(
            schedule_id
        )

        if not schedule:
            raise ScheduleNotFound()

        return schedule

    async def get_all_schedules(
        self,
    ) -> list[ClassSchedule]:

        return await self.schedule_repository.get_all()

    async def get_teacher_schedule(
        self,
        teacher_id: UUID,
    ) -> list[ClassSchedule]:

        return await self.schedule_repository.get_by_teacher_id(
            teacher_id
        )

    async def get_subject_schedule(
        self,
        subject_id: UUID,
    ) -> list[ClassSchedule]:

        return await self.schedule_repository.get_by_subject_id(
            subject_id
        )

    async def update_schedule(
         self,
         schedule_id: UUID,
         data: ScheduleCreate,
        ) -> ClassSchedule:

        schedule = await self.schedule_repository.get_by_uid(
          schedule_id
        )

        if not schedule:
            raise ScheduleNotFound()

        subject_id = UUID(data.subject_id)
        teacher_id = UUID(data.teacher_id)

        subject = await self.subject_repository.get_by_uid(
           subject_id
         )

        if not subject:
            raise SubjectNotFound()

        teacher = await self.teacher_repository.get_by_uid(
            teacher_id
        )

        if not teacher:
           raise TeacherNotFound()

        if data.start_time >= data.end_time:
           raise ScheduleConflict()

        existing_schedules = (
          await self.schedule_repository.get_by_teacher_id(
            teacher_id
        )
       )

        for existing in existing_schedules:

           if existing.uid == schedule.uid:
            continue

           if existing.day_of_week != data.day_of_week:
             continue

        if (
            data.start_time < existing.end_time
            and data.end_time > existing.start_time
        ):
            raise ScheduleConflict()

        schedule.subject_id = subject_id
        schedule.teacher_id = teacher_id
        schedule.day_of_week = data.day_of_week
        schedule.start_time = data.start_time
        schedule.end_time = data.end_time
        schedule.room = data.room

        return await self.schedule_repository.update(schedule)

    async def delete_schedule(
        self,
        schedule_id: UUID,
    ) -> None:

        schedule = await self.schedule_repository.get_by_uid(
            schedule_id
        )

        if not schedule:
            raise ScheduleNotFound()

        await self.schedule_repository.delete(schedule)