import pytest

from src.core.security import create_email_verification_token,hash_password
from src.models.user import User


@pytest.mark.asyncio
async def test_admin_dashboard(
    client,
    db_session,
):
    admin = User(
        username="admin_test",
        email="admin_test@example.com",
        phone="9876543290",
        first_name="Admin",
        last_name="User",
        role="admin",
        is_verified=True,
        password_hash=hash_password("TestPassword123"),
    )

    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)

    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": "admin_test@example.com",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/admin/dashboard",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Admin dashboard access granted"