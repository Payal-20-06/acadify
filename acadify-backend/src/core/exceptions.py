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


class InvalidRefreshToken(AcadifyException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired refresh token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


                