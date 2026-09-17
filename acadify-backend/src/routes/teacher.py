from fastapi import APIRouter, Depends

from src.core.permissions import RoleChecker


router = APIRouter(
    prefix="/api/v1/teachers",
    tags=["Teachers"],
)


teacher_only = RoleChecker(["teacher"])


@router.get(
    "/dashboard",
    dependencies=[Depends(teacher_only)],
)
async def teacher_dashboard():
    return {
        "message": "Teacher dashboard access granted"
    }