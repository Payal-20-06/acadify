from pydantic import BaseModel
from uuid import UUID


class EnrollmentCreate(BaseModel):
    student_id: str
    subject_id: str


class EnrollmentResponse(BaseModel):
    uid: UUID
    student_id: UUID
    subject_id: UUID