from fastapi import APIRouter, Depends

from src.core.permissions import RoleChecker


router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
)


admin_only = RoleChecker(["admin"])


@router.get(
    "/dashboard",
    dependencies=[Depends(admin_only)],
)
async def admin_dashboard():
    return {
        "message": "Admin dashboard access granted"
    }