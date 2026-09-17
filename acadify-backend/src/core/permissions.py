from typing import Any

from fastapi import Depends, HTTPException, status

from src.core.dependencies import get_current_user


class RoleChecker:

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        current_user=Depends(get_current_user),
    ) -> Any:

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user