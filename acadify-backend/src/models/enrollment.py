from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"

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

    student: "Student" = Relationship(
        back_populates="enrollments"
    )

    subject: "Subject" = Relationship(
        back_populates="enrollments"
    )