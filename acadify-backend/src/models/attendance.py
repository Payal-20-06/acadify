from datetime import date
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Attendance(SQLModel, table=True):
    __tablename__ = "attendance"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    student_id: UUID = Field(
        foreign_key="students.uid",
        index=True,
    )

    subject_id: UUID = Field(
        foreign_key="subjects.uid",
        index=True,
    )

    date: date

    is_present: bool = Field(default=False)

    student: "Student" = Relationship(
        back_populates="attendance_records"
    )

    subject: "Subject" = Relationship(
        back_populates="attendance_records"
    )