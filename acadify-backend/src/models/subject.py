from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Subject(SQLModel, table=True):
    __tablename__ = "subjects"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    name: str = Field(index=True)

    code: str = Field(
        unique=True,
        index=True,
    )

    description: str | None = None

    teacher_id: UUID = Field(
        foreign_key="teachers.uid",
        index=True,
    )

    teacher: "Teacher" = Relationship(
        back_populates="subjects"
    )

    enrollments: list["Enrollment"] = Relationship(
        back_populates="subject"
    )

    attendance_records: list["Attendance"] = Relationship(
        back_populates="subject"
    )

    marks: list["Marks"] = Relationship(
        back_populates="subject"
    )

    class_schedules: list["ClassSchedule"] = Relationship(
        back_populates="subject"
    )