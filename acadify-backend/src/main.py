from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth import router as auth_router
from src.routes.student import router as student_router
from src.routes.teacher import router as teacher_router
from src.routes.admin import router as admin_router

from src.core.exceptions import AcadifyException
from src.core.exception_handlers import acadify_exception_handler


app = FastAPI(
    title="Acadify API",
    description="Academic Management Platform API",
    version="1.0.0",
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