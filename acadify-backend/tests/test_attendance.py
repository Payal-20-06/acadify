import pytest

from src.core.security import create_email_verification_token
from src.models.student import Student
from src.models.teacher import Teacher


@pytest.mark.asyncio
async def test_create_attendance(client, db_session):


    student_payload = {
        "full_name": "Attendance Student",
        "email": "attendance_student@example.com",
        "phone": "9876543240",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=student_payload,
    )

    assert signup_response.status_code == 201

    student_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        student_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    student = Student(
        user_id=student_user_id,
        enrollment_number="ATT001",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)


    teacher_payload = {
        "full_name": "Attendance Teacher",
        "email": "attendance_teacher@example.com",
        "phone": "9876543241",
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
        employee_id="ATTEMP001",
        department="Computer Science",
        designation="Assistant Professor",
    )

    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)


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


    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Operating Systems",
            "code": "CS401",
            "description": "Operating Systems",
            "teacher_id": str(teacher.uid),
        },
        headers=teacher_headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]


    enrollment_response = await client.post(
        "/api/v1/enrollments",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
        },
        headers=teacher_headers,
    )

    assert enrollment_response.status_code == 201

    attendance_response = await client.post(
        "/api/v1/attendance",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
            "date": "2026-09-26",
            "is_present": True,
        },
        headers=teacher_headers,
    )

    assert attendance_response.status_code == 201

    data = attendance_response.json()

    assert data["student_id"] == str(student.uid)
    assert data["subject_id"] == subject_id
    assert data["date"] == "2026-09-26"
    assert data["is_present"] is True

@pytest.mark.asyncio
async def test_create_attendance_student_not_enrolled(
    client,
    db_session,
):
    # Create student
    student_payload = {
        "full_name": "Not Enrolled Student",
        "email": "attendance_not_enrolled@example.com",
        "phone": "9876543242",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=student_payload,
    )

    assert signup_response.status_code == 201

    student_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        student_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    student = Student(
        user_id=student_user_id,
        enrollment_number="ATT002",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Attendance Teacher 2",
        "email": "attendance_teacher2@example.com",
        "phone": "9876543243",
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
        employee_id="ATTEMP002",
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
            "name": "Database Systems",
            "code": "CS402",
            "description": "Database Systems",
            "teacher_id": str(teacher.uid),
        },
        headers=teacher_headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Do NOT create enrollment

    # Try to create attendance
    attendance_response = await client.post(
        "/api/v1/attendance",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
            "date": "2026-09-27",
            "is_present": True,
        },
        headers=teacher_headers,
    )

    assert attendance_response.status_code == 400

    data = attendance_response.json()

    assert data["message"] == "Student is not enrolled in this subject"

@pytest.mark.asyncio
async def test_create_duplicate_attendance(
    client,
    db_session,
):
    # Create student
    student_payload = {
        "full_name": "Duplicate Attendance Student",
        "email": "attendance_duplicate@example.com",
        "phone": "9876543244",
        "role": "student",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123",
    }

    signup_response = await client.post(
        "/api/v1/auths/signup",
        json=student_payload,
    )

    assert signup_response.status_code == 201

    student_user_id = signup_response.json()["user"]["uid"]

    verification_token = create_email_verification_token(
        student_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    student = Student(
        user_id=student_user_id,
        enrollment_number="ATT003",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Duplicate Attendance Teacher",
        "email": "attendance_duplicate_teacher@example.com",
        "phone": "9876543245",
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
        employee_id="ATTEMP003",
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
            "code": "CS403",
            "description": "Computer Networks",
            "teacher_id": str(teacher.uid),
        },
        headers=teacher_headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create enrollment
    enrollment_response = await client.post(
        "/api/v1/enrollments",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
        },
        headers=teacher_headers,
    )

    assert enrollment_response.status_code == 201

    attendance_payload = {
        "student_id": str(student.uid),
        "subject_id": subject_id,
        "date": "2026-09-28",
        "is_present": True,
    }

    # First attendance
    first_response = await client.post(
        "/api/v1/attendance",
        json=attendance_payload,
        headers=teacher_headers,
    )

    assert first_response.status_code == 201

    # Duplicate attendance
    second_response = await client.post(
        "/api/v1/attendance",
        json=attendance_payload,
        headers=teacher_headers,
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["message"] == "Attendance already recorded for this date"
