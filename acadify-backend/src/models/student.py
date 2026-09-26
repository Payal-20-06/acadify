from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:

    from src.models.enrollment import Enrollment
    from src.models.attendance import Attendance
    from src.models.marks import Marks

class Student(SQLModel, table=True):
    __tablename__ = "students"

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

    enrollment_number: str = Field(
        unique=True,
        index=True,
    )

    course: str

    semester: int


    enrollments: list["Enrollment"] = Relationship(
        back_populates="student"
    )

    attendance_records: list["Attendance"] = Relationship(
        back_populates="student"
    )

    marks: list["Marks"] = Relationship(
        back_populates="student"
    )
