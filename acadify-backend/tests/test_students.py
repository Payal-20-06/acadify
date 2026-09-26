import pytest

from src.core.security import create_email_verification_token


@pytest.mark.asyncio
async def test_student_dashboard(client):
    payload = {
        "full_name": "Dashboard Student",
        "email": "dashboardstudent@example.com",
        "phone": "9876543218",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Signup
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    # Verify email
    user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={
            "token": verification_token,
        },
    )

    assert verify_response.status_code == 200

    # Login
    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Student dashboard
    dashboard_response = await client.get(
        "/api/v1/students/dashboard",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert dashboard_response.status_code == 200

    data = dashboard_response.json()

    assert data["message"] == "Student dashboard access granted"

@pytest.mark.asyncio
async def test_teacher_cannot_access_student_dashboard(client):
    payload = {
        "full_name": "Dashboard Teacher",
        "email": "dashboardteacher@example.com",
        "phone": "9876543219",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Signup
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    # Verify email
    user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={
            "token": verification_token,
        },
    )

    assert verify_response.status_code == 200

    # Login
    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Try to access student dashboard
    dashboard_response = await client.get(
        "/api/v1/students/dashboard",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert dashboard_response.status_code == 403

    data = dashboard_response.json()

    assert data["detail"] == "You do not have permission to access this resource"
