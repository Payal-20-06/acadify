from pydantic import BaseModel, Field


class TeacherCreate(BaseModel):
    user_id: str

    employee_id: str = Field(
        min_length=3,
        max_length=30,
    )

    department: str = Field(
        min_length=2,
        max_length=100,
    )

    designation: str = Field(
        min_length=2,
        max_length=100,
    )


class TeacherResponse(BaseModel):
    uid: str
    user_id: str
    employee_id: str
    department: str
    designation: str