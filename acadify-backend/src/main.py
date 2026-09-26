from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth import router as auth_router
from src.routes.student import router as student_router
from src.routes.teacher import router as teacher_router
from src.routes.admin import router as admin_router

from src.core.exceptions import AcadifyException
from src.core.exception_handlers import acadify_exception_handler

from src.routes.subject import router as subject_router
from src.routes.enrollment import router as enrollment_router
from src.routes.attendance import router as attendance_router
from src.routes.marks import router as marks_router
from src.routes.schedule import router as schedule_router
from src.routes.announcement import router as announcement_router


app = FastAPI(
    title="Acadify API",
    description="""
## Acadify Academic Management API

Backend API for managing:

- Authentication and authorization
- Students and teachers
- Subjects and enrollments
- Attendance
- Marks
- Class schedules
- Announcements

Authentication uses JWT Bearer tokens.
""",
    version="1.0.0",
    contact={
        "name": "Acadify Development Team",
    },
    license_info={
        "name": "MIT",
    },
)
app.add_exception_handler(
    AcadifyException,
    acadify_exception_handler,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(admin_router)
app.include_router(subject_router, prefix="/api/v1")
app.include_router(enrollment_router, prefix="/api/v1")
app.include_router(attendance_router, prefix="/api/v1")
app.include_router(marks_router, prefix="/api/v1")
app.include_router(schedule_router, prefix="/api/v1")
app.include_router(announcement_router, prefix="/api/v1")


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