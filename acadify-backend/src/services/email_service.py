from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
    MessageType,
)

from src.core.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)


async def send_verification_email(
    email: str,
    verification_token: str,
):
    print("MAIL SENDER:")
    print(settings.MAIL_USERNAME)

    print("MAIL RECIPIENT:")
    print(email)

    verification_url = (
        f"{settings.FRONTEND_URL}/verify-email"
        f"?token={verification_token}"
    )

    print("VERIFICATION URL:")
    print(verification_url)

    message = MessageSchema(
        subject="Verify your Acadify account",
        recipients=[email],
        body=f"""
        <html>
            <body>
                <h2>Welcome to Acadify!</h2>

                <p>
                    Thank you for creating your account.
                </p>

                <p>
                    Please click the button below to verify your email:
                </p>

                <p>
                    <a href="{verification_url}">
                        Verify Email
                    </a>
                </p>

                <p>
                    This verification link will expire in 30 minutes.
                </p>

                <p>
                    If you did not create this account,
                    you can ignore this email.
                </p>
            </body>
        </html>
        """,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)

    await fm.send_message(message)


async def send_password_reset_email(
    email: str,
    reset_token: str,
):
    print("MAIL SENDER:")
    print(settings.MAIL_USERNAME)

    print("MAIL RECIPIENT:")
    print(email)

    reset_url = (
        f"{settings.FRONTEND_URL}/reset-password"
        f"?token={reset_token}"
    )

    print("RESET URL:")
    print(reset_url)

    message = MessageSchema(
        subject="Reset your Acadify password",
        recipients=[email],
        body=f"""
        <html>
            <body>
                <h2>Reset Your Password</h2>

                <p>
                    We received a request to reset your
                    Acadify password.
                </p>

                <p>
                    <a href="{reset_url}">
                        Reset Password
                    </a>
                </p>

                <p>
                    This link will expire in 15 minutes.
                </p>

                <p>
                    If you did not request this,
                    you can safely ignore this email.
                </p>
            </body>
        </html>
        """,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)

    await fm.send_message(message)