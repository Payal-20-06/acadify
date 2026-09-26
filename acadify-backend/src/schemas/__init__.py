from src.schemas.auth import (
    SignupRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from src.schemas.student import (
    StudentCreate,
    StudentResponse,
)

from src.schemas.teacher import (
    TeacherCreate,
    TeacherResponse,
)

from src.schemas.subject import (
    SubjectCreate,
    SubjectResponse,
)

from src.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
)

from src.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
)

from src.schemas.marks import (
    MarksCreate,
    MarksResponse,
)

from src.schemas.schedule import (
    ScheduleCreate,
    ScheduleResponse,
)

from src.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
)