from uuid import UUID

from pydantic import BaseModel, Field


class SubjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=20)
    description: str | None = None
    teacher_id: UUID


class SubjectResponse(BaseModel):
    uid: UUID
    name: str
    code: str
    description: str | None
    teacher_id: UUID