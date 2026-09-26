from datetime import date
from uuid import UUID

from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    student_id: str
    subject_id: str
    date: date
    is_present: bool = False


class AttendanceResponse(BaseModel):
    uid: UUID
    student_id: UUID
    subject_id: UUID
    date: date
    is_present: bool