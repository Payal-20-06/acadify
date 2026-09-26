import pytest

from src.core.security import create_email_verification_token


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Acadify API is running"


@pytest.mark.asyncio
async def test_signup(client):
    payload = {
        "full_name": "Test Student",
        "email": "teststudent@example.com",
        "phone": "9876543210",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == (
        "Account created successfully. "
        "Please check your email to verify your account."
    )

    assert data["user"]["email"] == payload["email"]
    assert data["user"]["role"] == "student"
    assert data["user"]["is_verified"] is False


@pytest.mark.asyncio
async def test_login(client):
    payload = {
        "full_name": "Login Student",
        "email": "loginstudent@example.com",
        "phone": "9876543211",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Create the user
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    # Login
    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client):
    payload = {
        "full_name": "Invalid Login Student",
        "email": "invalidlogin@example.com",
        "phone": "9876543212",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Create the user
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    # Try login with wrong password
    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": payload["email"],
            "password": "WrongPassword123",
        },
    )

    assert login_response.status_code == 401

    data = login_response.json()

    assert data["message"] == "Invalid email or password"


@pytest.mark.asyncio
async def test_refresh_token(client):
    payload = {
        "full_name": "Refresh Student",
        "email": "refreshstudent@example.com",
        "phone": "9876543213",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Create user
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    # Login
    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    refresh_token = login_data["refresh_token"]

    # Refresh access token
    refresh_response = await client.post(
        "/api/v1/auths/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert refresh_response.status_code == 200

    refresh_data = refresh_response.json()

    assert "access_token" in refresh_data
    assert refresh_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_me(client):
    payload = {
        "full_name": "Me Student",
        "email": "mstudent@example.com",
        "phone": "9876543214",
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
    assert verify_response.json()["is_verified"] is True

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

    # Access protected endpoint
    me_response = await client.get(
        "/api/v1/auths/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert me_response.status_code == 200

    data = me_response.json()

    assert data["email"] == payload["email"]
    assert data["role"] == "student"
    assert data["is_verified"] is True

@pytest.mark.asyncio
async def test_logout_revokes_session(client):
    payload = {
        "full_name": "Logout Student",
        "email": "logoutstudent@example.com",
        "phone": "9876543215",
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

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    # Token should work before logout
    me_response = await client.get(
        "/api/v1/auths/me",
        headers=headers,
    )

    assert me_response.status_code == 200

    # Logout
    logout_response = await client.post(
        "/api/v1/auths/logout",
        headers=headers,
    )

    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Logged out successfully."

    # Same token should no longer work
    me_after_logout = await client.get(
        "/api/v1/auths/me",
        headers=headers,
    )

    assert me_after_logout.status_code == 401

@pytest.mark.asyncio
async def test_invalid_refresh_token(client):
    response = await client.post(
        "/api/v1/auths/refresh",
        json={
            "refresh_token": "invalid-refresh-token",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["message"] == "Invalid or expired refresh token"

@pytest.mark.asyncio
async def test_student_role_access(client):
    payload = {
        "full_name": "RBAC Student",
        "email": "rbacstudent@example.com",
        "phone": "9876543216",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={
            "token": verification_token,
        },
    )

    assert verify_response.status_code == 200

    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auths/student-test",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Student access granted"

@pytest.mark.asyncio
async def test_teacher_cannot_access_student_endpoint(client):
    payload = {
        "full_name": "RBAC Teacher",
        "email": "rbacteacher@example.com",
        "phone": "9876543217",
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

    # Try to access student-only endpoint
    response = await client.get(
        "/api/v1/auths/student-test",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert "detail" in data
    assert data["detail"] == "You do not have permission to access this resource"
