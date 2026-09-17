from fastapi import APIRouter, Depends

from src.core.permissions import RoleChecker


router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"],
)


student_only = RoleChecker(["student"])


@router.get(
    "/dashboard",
    dependencies=[Depends(student_only)],
)
async def student_dashboard():
    return {
        "message": "Student dashboard access granted"
    }