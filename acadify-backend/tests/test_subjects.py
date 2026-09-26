import pytest

from src.core.security import create_email_verification_token
from src.models.teacher import Teacher


@pytest.mark.asyncio
async def test_create_subject(client, db_session):
    payload = {
        "full_name": "Subject Teacher",
        "email": "subjectteacher@example.com",
        "phone": "9876543222",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Create teacher user
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    user_id = signup_response.json()["user"]["uid"]

    # Verify email
    verification_token = create_email_verification_token(user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={
            "token": verification_token,
        },
    )

    assert verify_response.status_code == 200

    # Create Teacher record directly in test database
    teacher = Teacher(
        user_id=user_id,
        employee_id="EMP001",
        department="Computer Science",
        designation="Assistant Professor",
    )

    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)

    # Login as teacher
    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Data Structures",
            "code": "CS301",
            "description": "Data Structures and Algorithms",
            "teacher_id": str(teacher.uid),
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert subject_response.status_code == 201

    data = subject_response.json()

    assert data["name"] == "Data Structures"
    assert data["code"] == "CS301"
    assert data["description"] == "Data Structures and Algorithms"
    assert data["teacher_id"] == str(teacher.uid)

@pytest.mark.asyncio
async def test_create_subject_duplicate_code(client, db_session):
    payload = {
        "full_name": "Duplicate Subject Teacher",
        "email": "duplicatesubjectteacher@example.com",
        "phone": "9876543223",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Create teacher user
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    user_id = signup_response.json()["user"]["uid"]

    # Verify email
    verification_token = create_email_verification_token(user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={
            "token": verification_token,
        },
    )

    assert verify_response.status_code == 200

    # Create Teacher record
    teacher = Teacher(
        user_id=user_id,
        employee_id="EMP002",
        department="Computer Science",
        designation="Assistant Professor",
    )

    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)

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

    subject_payload = {
        "name": "Operating Systems",
        "code": "CS302",
        "description": "Operating Systems fundamentals",
        "teacher_id": str(teacher.uid),
    }

    # Create first subject
    first_response = await client.post(
        "/api/v1/subjects",
        json=subject_payload,
        headers=headers,
    )

    assert first_response.status_code == 201

    # Try creating another subject with same code
    duplicate_response = await client.post(
        "/api/v1/subjects",
        json={
            **subject_payload,
            "name": "Advanced Operating Systems",
        },
        headers=headers,
    )

    assert duplicate_response.status_code == 409

    data = duplicate_response.json()


    assert data["message"] == "Subject already exists"

@pytest.mark.asyncio
async def test_get_subjects(client, db_session):
    payload = {
        "full_name": "Get Subjects Teacher",
        "email": "getsubjects@example.com",
        "phone": "9876543224",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Create teacher user
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    user_id = signup_response.json()["user"]["uid"]

    # Verify email
    verification_token = create_email_verification_token(user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    # Create Teacher record
    teacher = Teacher(
        user_id=user_id,
        employee_id="EMP003",
        department="Computer Science",
        designation="Assistant Professor",
    )

    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)

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

    # Create a subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Database Management",
            "code": "CS303",
            "description": "Database fundamentals",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
    )

    assert subject_response.status_code == 201

    # Get all subjects
    response = await client.get(
        "/api/v1/subjects",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Database Management"
    assert data[0]["code"] == "CS303"


@pytest.mark.asyncio
async def test_get_subject(client, db_session):
    payload = {
        "full_name": "Get Subject Teacher",
        "email": "getsubject@example.com",
        "phone": "9876543225",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Create teacher user
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    user_id = signup_response.json()["user"]["uid"]

    # Verify email
    verification_token = create_email_verification_token(user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    # Create Teacher record
    teacher = Teacher(
        user_id=user_id,
        employee_id="EMP004",
        department="Computer Science",
        designation="Assistant Professor",
    )

    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)

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

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Computer Networks",
            "code": "CS304",
            "description": "Computer Networks fundamentals",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Get subject by ID
    response = await client.get(
        f"/api/v1/subjects/{subject_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["uid"] == subject_id
    assert data["name"] == "Computer Networks"
    assert data["code"] == "CS304"
    assert data["description"] == "Computer Networks fundamentals"
    assert data["teacher_id"] == str(teacher.uid)


@pytest.mark.asyncio
async def test_student_cannot_create_subject(client):
    payload = {
        "full_name": "Subject Student",
        "email": "subjectstudent@example.com",
        "phone": "9876543226",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    # Create student
    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=payload,
    )

    assert signup_response.status_code == 201

    user_id = signup_response.json()["user"]["uid"]

    # Verify email
    verification_token = create_email_verification_token(user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
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

    # Student tries to create subject
    response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Operating Systems",
            "code": "CS305",
            "description": "Operating Systems",
            "teacher_id": "00000000-0000-0000-0000-000000000000",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "You do not have permission to access this resource"

@pytest.mark.asyncio
async def test_get_subjects_unauthorized(client):
    response = await client.get("/api/v1/subjects")

    assert response.status_code in (401, 403)
