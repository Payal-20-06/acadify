from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    user_id: str
    enrollment_number: str = Field(
        min_length=3,
        max_length=30,
    )
    course: str = Field(
        min_length=2,
        max_length=100,
    )
    semester: int = Field(
        ge=1,
        le=8,
    )


class StudentResponse(BaseModel):
    uid: str
    user_id: str
    enrollment_number: str
    course: str
    semester: int