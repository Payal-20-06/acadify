from pydantic import BaseModel, Field
from uuid import UUID


class MarksCreate(BaseModel):
    student_id: str
    subject_id: str

    assessment_type: str = Field(
        min_length=2,
        max_length=50,
    )

    marks_obtained: float = Field(
        ge=0,
    )

    max_marks: float = Field(
        gt=0,
    )


class MarksResponse(BaseModel):
    uid: UUID
    student_id: UUID
    subject_id: UUID
    assessment_type: str
    marks_obtained: float
    max_marks: float