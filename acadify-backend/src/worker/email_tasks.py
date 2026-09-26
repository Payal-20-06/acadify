import asyncio

from src.worker.celery_app import celery_app

from src.services.email_service import (
    send_verification_email,
    send_password_reset_email,
)


@celery_app.task
def send_verification_email_task(
    email: str,
    verification_token: str,
):
    asyncio.run(
        send_verification_email(
            email,
            verification_token,
        )
    )


@celery_app.task
def send_password_reset_email_task(
    email: str,
    reset_token: str,
):
    asyncio.run(
        send_password_reset_email(
            email,
            reset_token,
        )
    )