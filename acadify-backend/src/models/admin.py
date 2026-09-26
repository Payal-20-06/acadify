from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Admin(SQLModel, table=True):
    __tablename__ = "admins"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )

    user_id: UUID = Field(
        foreign_key="users.uid",
        unique=True,
        index=True,
    )

    employee_id: str = Field(
        unique=True,
        index=True,
    )

    department: str | None = None