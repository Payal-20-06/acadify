from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    username: str = Field(
        index=True,
        unique=True,
    )

    email: str = Field(
        index=True,
        unique=True,
    )

    phone: str = Field(
        index=True,
        unique=True,
    )

    first_name: str
    last_name: str

    role: str = Field(
        default="student",
        index=True,
    )

    is_verified: bool = Field(
        default=False,
    )

    password_hash: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )