from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.exceptions import AcadifyException


async def acadify_exception_handler(
    request: Request,
    exc: AcadifyException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
        },
    )