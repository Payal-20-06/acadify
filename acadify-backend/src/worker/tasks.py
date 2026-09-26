from src.worker.celery_app import celery_app


@celery_app.task
def test_background_task(message: str) -> str:

    print(f"Background task received: {message}")

    return f"Processed: {message}"