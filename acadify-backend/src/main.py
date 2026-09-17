from fastapi import FastAPI

from src.routes.auth import router as auth_router
from src.routes.student import router as student_router
from src.routes.teacher import router as teacher_router
from src.routes.admin import router as admin_router


app = FastAPI(
    title="Acadify API",
    description="Academic Management Platform API",
    version="1.0.0",
)


app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "message": "Acadify API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(admin_router)