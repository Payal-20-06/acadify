import pytest
from uuid import uuid4

from src.core.security import create_email_verification_token
from src.models.student import Student
from src.models.teacher import Teacher


@pytest.mark.asyncio
async def test_create_schedule(
    client,
    db_session,
):
    # Create teacher
    teacher_payload = {
        "full_name": "Schedule Test Teacher",
        "email": "schedule_teacher@example.com",
        "phone": "9876543260",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=teacher_payload,
    )

    assert signup_response.status_code == 201

    teacher_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="SCHT001",
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
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )

    assert login_response.status_code == 200

    teacher_token = login_response.json()["access_token"]

    teacher_headers = {
        "Authorization": f"Bearer {teacher_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Computer Networks",
            "code": "CS407",
            "description": "Computer Networks",
            "teacher_id": str(teacher.uid),
        },
        headers=teacher_headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create schedule
    schedule_response = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Monday",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "room": "Lab 101",
        },
        headers=teacher_headers,
    )

    assert schedule_response.status_code == 201

    data = schedule_response.json()

    assert data["subject_id"] == subject_id
    assert data["teacher_id"] == str(teacher.uid)
    assert data["day_of_week"] == "Monday"
    assert data["start_time"] == "10:00:00"
    assert data["end_time"] == "11:00:00"
    assert data["room"] == "Lab 101"

@pytest.mark.asyncio
async def test_create_schedule_conflict(
    client,
    db_session,
):
    # Create teacher
    teacher_payload = {
        "full_name": "Conflict Test Teacher",
        "email": "schedule_conflict_teacher@example.com",
        "phone": "9876543261",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=teacher_payload,
    )

    assert signup_response.status_code == 201

    teacher_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="SCHT002",
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
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )

    assert login_response.status_code == 200

    teacher_token = login_response.json()["access_token"]

    teacher_headers = {
        "Authorization": f"Bearer {teacher_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Database Management",
            "code": "CS408",
            "description": "Database Management",
            "teacher_id": str(teacher.uid),
        },
        headers=teacher_headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create first schedule
    first_schedule = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Tuesday",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "room": "Room 101",
        },
        headers=teacher_headers,
    )

    assert first_schedule.status_code == 201

    # Create overlapping schedule
    second_schedule = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Tuesday",
            "start_time": "10:30:00",
            "end_time": "11:30:00",
            "room": "Room 102",
        },
        headers=teacher_headers,
    )

    assert second_schedule.status_code == 409

    data = second_schedule.json()

    assert data["message"] == "Schedule conflicts with an existing class"

@pytest.mark.asyncio
async def test_get_schedule(
    client,
    db_session,
):
    # Create teacher
    teacher_payload = {
        "full_name": "Get Schedule Teacher",
        "email": "get_schedule_teacher@example.com",
        "phone": "9876543262",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=teacher_payload,
    )

    assert signup_response.status_code == 201

    teacher_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="SCHT003",
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
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )

    assert login_response.status_code == 200

    teacher_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {teacher_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Operating Systems",
            "code": "CS409",
            "description": "Operating Systems",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create schedule
    schedule_response = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Wednesday",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "room": "Room 201",
        },
        headers=headers,
    )

    assert schedule_response.status_code == 201

    schedule_id = schedule_response.json()["uid"]

    # Get schedule
    response = await client.get(
        f"/api/v1/schedules/{schedule_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["uid"] == schedule_id
    assert data["subject_id"] == subject_id
    assert data["teacher_id"] == str(teacher.uid)
    assert data["day_of_week"] == "Wednesday"
    assert data["start_time"] == "09:00:00"
    assert data["end_time"] == "10:00:00"
    assert data["room"] == "Room 201"

@pytest.mark.asyncio
async def test_get_all_schedules(
    client,
    db_session,
):
    # Create teacher
    teacher_payload = {
        "full_name": "All Schedules Teacher",
        "email": "all_schedules_teacher@example.com",
        "phone": "9876543263",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=teacher_payload,
    )

    assert signup_response.status_code == 201

    teacher_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="SCHT004",
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
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )

    assert login_response.status_code == 200

    teacher_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {teacher_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Computer Graphics",
            "code": "CS410",
            "description": "Computer Graphics",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create first schedule
    first_response = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Thursday",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "room": "Room 301",
        },
        headers=headers,
    )

    assert first_response.status_code == 201

    # Create second schedule
    second_response = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Friday",
            "start_time": "11:00:00",
            "end_time": "12:00:00",
            "room": "Room 302",
        },
        headers=headers,
    )

    assert second_response.status_code == 201

    # Get all schedules
    response = await client.get(
        "/api/v1/schedules",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["teacher_id"] == str(teacher.uid)
    assert data[1]["teacher_id"] == str(teacher.uid)


@pytest.mark.asyncio
async def test_get_teacher_schedule(
    client,
    db_session,
):
    # Create teacher
    teacher_payload = {
        "full_name": "Teacher Schedule Test",
        "email": "teacher_schedule@example.com",
        "phone": "9876543264",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=teacher_payload,
    )

    assert signup_response.status_code == 201

    teacher_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="SCHT005",
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
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )

    assert login_response.status_code == 200

    teacher_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {teacher_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Artificial Intelligence",
            "code": "CS411",
            "description": "Artificial Intelligence",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create schedule
    schedule_response = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Monday",
            "start_time": "14:00:00",
            "end_time": "15:00:00",
            "room": "Room 401",
        },
        headers=headers,
    )

    assert schedule_response.status_code == 201

    # Get teacher schedule
    response = await client.get(
        f"/api/v1/schedules/teacher/{teacher.uid}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["teacher_id"] == str(teacher.uid)
    assert data[0]["subject_id"] == subject_id
    assert data[0]["day_of_week"] == "Monday"
    assert data[0]["start_time"] == "14:00:00"
    assert data[0]["end_time"] == "15:00:00"
    assert data[0]["room"] == "Room 401"

@pytest.mark.asyncio
async def test_get_subject_schedule(
    client,
    db_session,
):
    # Create teacher
    teacher_payload = {
        "full_name": "Subject Schedule Teacher",
        "email": "subject_schedule_teacher@example.com",
        "phone": "9876543265",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=teacher_payload,
    )

    assert signup_response.status_code == 201

    teacher_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="SCHT006",
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
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )

    assert login_response.status_code == 200

    teacher_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {teacher_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Machine Learning",
            "code": "CS412",
            "description": "Machine Learning",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create schedule
    schedule_response = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Friday",
            "start_time": "15:00:00",
            "end_time": "16:00:00",
            "room": "Room 402",
        },
        headers=headers,
    )

    assert schedule_response.status_code == 201

    # Get subject schedule
    response = await client.get(
        f"/api/v1/schedules/subject/{subject_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["uid"] == schedule_response.json()["uid"]
    assert data[0]["subject_id"] == subject_id
    assert data[0]["teacher_id"] == str(teacher.uid)
    assert data[0]["day_of_week"] == "Friday"
    assert data[0]["start_time"] == "15:00:00"
    assert data[0]["end_time"] == "16:00:00"
    assert data[0]["room"] == "Room 402"

@pytest.mark.asyncio
async def test_delete_schedule(
    client,
    db_session,
):
    # Create teacher
    teacher_payload = {
        "full_name": "Delete Schedule Teacher",
        "email": "delete_schedule_teacher@example.com",
        "phone": "9876543266",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=teacher_payload,
    )

    assert signup_response.status_code == 201

    teacher_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="SCHT007",
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
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )

    assert login_response.status_code == 200

    teacher_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {teacher_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Cloud Computing",
            "code": "CS413",
            "description": "Cloud Computing",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create schedule
    schedule_response = await client.post(
        "/api/v1/schedules",
        json={
            "subject_id": subject_id,
            "teacher_id": str(teacher.uid),
            "day_of_week": "Saturday",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "room": "Room 501",
        },
        headers=headers,
    )

    assert schedule_response.status_code == 201

    schedule_id = schedule_response.json()["uid"]

    # Delete schedule
    delete_response = await client.delete(
        f"/api/v1/schedules/{schedule_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    # Verify schedule no longer exists
    get_response = await client.get(
        f"/api/v1/schedules/{schedule_id}",
        headers=headers,
    )

    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_get_nonexistent_schedule(
    client,
    db_session,
):
    # Create teacher
    teacher_payload = {
        "full_name": "Missing Schedule Teacher",
        "email": "missing_schedule_teacher@example.com",
        "phone": "9876543267",
        "role": "teacher",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=teacher_payload,
    )

    assert signup_response.status_code == 201

    teacher_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="SCHT008",
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
            "email": teacher_payload["email"],
            "password": teacher_payload["password"],
        },
    )

    assert login_response.status_code == 200

    teacher_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {teacher_token}",
    }

    # Request a schedule that does not exist
    fake_schedule_id = uuid4()

    response = await client.get(
        f"/api/v1/schedules/{fake_schedule_id}",
        headers=headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Schedule not found"
