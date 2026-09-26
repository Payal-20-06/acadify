from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Announcement(SQLModel, table=True):
    __tablename__ = "announcements"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    title: str

    content: str

    created_by: UUID = Field(
        foreign_key="users.uid",
        index=True,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )