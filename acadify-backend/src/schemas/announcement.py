from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class AnnouncementCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    content: str = Field(
        min_length=1,
    )


class AnnouncementResponse(BaseModel):
    uid: UUID
    title: str
    content: str
    created_by: UUID
    created_at: datetime