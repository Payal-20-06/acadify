from fastapi import status


class AcadifyException(Exception):
    """Base exception for Acadify."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class InvalidCredentials(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class EmailAlreadyRegistered(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Email already registered",
            status_code=status.HTTP_409_CONFLICT,
        )


class PhoneAlreadyRegistered(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Phone number already registered",
            status_code=status.HTTP_409_CONFLICT,
        )


class UsernameAlreadyExists(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Username already exists",
            status_code=status.HTTP_409_CONFLICT,
        )


class InvalidVerificationToken(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired verification token",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

class InvalidToken(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AccessTokenRequired(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Access token required",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class TokenRevoked(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Token has been revoked",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class UserNotFound(AcadifyException):
    def __init__(self):
        super().__init__(
            message="User not found",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class EmailNotVerified(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Please verify your email before accessing this resource",
            status_code=status.HTTP_403_FORBIDDEN,
        )
class InvalidRefreshToken(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired refresh token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class InvalidPasswordResetToken(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired password reset token",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class StudentAlreadyExists(AcadifyException):
    def __init__(self):
        super().__init__("Student profile already exists", status.HTTP_409_CONFLICT)


class StudentNotFound(AcadifyException):
    def __init__(self):
        super().__init__("Student not found", status.HTTP_404_NOT_FOUND)


class TeacherAlreadyExists(AcadifyException):
    def __init__(self):
        super().__init__("Teacher profile already exists", status.HTTP_409_CONFLICT)


class TeacherNotFound(AcadifyException):
    def __init__(self):
        super().__init__("Teacher not found", status.HTTP_404_NOT_FOUND)


class SubjectAlreadyExists(AcadifyException):
    def __init__(self):
        super().__init__("Subject already exists", status.HTTP_409_CONFLICT)


class SubjectNotFound(AcadifyException):
    def __init__(self):
        super().__init__("Subject not found", status.HTTP_404_NOT_FOUND)


class EnrollmentAlreadyExists(AcadifyException):
    def __init__(self):
        super().__init__("Student is already enrolled in this subject", status.HTTP_409_CONFLICT)


class EnrollmentNotFound(AcadifyException):
    def __init__(self):
        super().__init__("Enrollment not found", status.HTTP_404_NOT_FOUND)


class StudentNotEnrolled(AcadifyException):
    def __init__(self):
        super().__init__("Student is not enrolled in this subject", status.HTTP_400_BAD_REQUEST)


class AttendanceAlreadyExists(AcadifyException):
    def __init__(self):
        super().__init__("Attendance already recorded for this date", status.HTTP_409_CONFLICT)


class AttendanceNotFound(AcadifyException):
    def __init__(self):
        super().__init__("Attendance record not found", status.HTTP_404_NOT_FOUND)


class MarksNotFound(AcadifyException):
    def __init__(self):
        super().__init__("Marks record not found", status.HTTP_404_NOT_FOUND)


class InvalidMarks(AcadifyException):
    def __init__(self):
        super().__init__(
            "Marks obtained cannot be greater than maximum marks",
            status.HTTP_400_BAD_REQUEST,
        )


class ScheduleNotFound(AcadifyException):
    def __init__(self):
        super().__init__("Schedule not found", status.HTTP_404_NOT_FOUND)


class ScheduleConflict(AcadifyException):
    def __init__(self):
        super().__init__(
            "Schedule conflicts with an existing class",
            status.HTTP_409_CONFLICT,
        )


class AnnouncementNotFound(AcadifyException):
    def __init__(self):
        super().__init__("Announcement not found", status.HTTP_404_NOT_FOUND)


