from datetime import time
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class ClassSchedule(SQLModel, table=True):
    __tablename__ = "class_schedules"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    subject_id: UUID = Field(
        foreign_key="subjects.uid",
        index=True,
    )

    teacher_id: UUID = Field(
        foreign_key="teachers.uid",
        index=True,
    )

    day_of_week: str

    start_time: time

    end_time: time

    room: str | None = None

    subject: "Subject" = Relationship(
        back_populates="class_schedules"
    )

    teacher: "Teacher" = Relationship(
        back_populates="class_schedules"
    )