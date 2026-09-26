from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.subject import Subject
    from src.models.class_schedule import ClassSchedule


class Teacher(SQLModel, table=True):
    __tablename__ = "teachers"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    user_id: UUID = Field(
        foreign_key="users.uid",
        unique=True,
        index=True,
    )

    employee_id: str = Field(
        unique=True,
        index=True,
    )

    department: str

    designation: str



    subjects: list["Subject"] = Relationship(
        back_populates="teacher"
    )

    class_schedules: list["ClassSchedule"] = Relationship(
        back_populates="teacher"
    )
