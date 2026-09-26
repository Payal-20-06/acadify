from datetime import time
from uuid import UUID

from pydantic import BaseModel, Field


class ScheduleCreate(BaseModel):
    subject_id: str
    teacher_id: str

    day_of_week: str = Field(
        min_length=3,
        max_length=15,
    )

    start_time: time
    end_time: time

    room: str | None = Field(
        default=None,
        max_length=50,
    )


class ScheduleResponse(BaseModel):
    uid: UUID
    subject_id: UUID
    teacher_id: UUID
    day_of_week: str
    start_time: time
    end_time: time
    room: str | None