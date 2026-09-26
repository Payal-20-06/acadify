from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.student import Student
    from src.models.subject import Subject


class Marks(SQLModel, table=True):
    __tablename__ = "marks"

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

    assessment_type: str

    marks_obtained: float

    max_marks: float

    student: "Student" = Relationship(
        back_populates="marks"
    )

    subject: "Subject" = Relationship(
        back_populates="marks"
    )
