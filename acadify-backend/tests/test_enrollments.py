import pytest

from src.core.security import create_email_verification_token
from src.models.student import Student
from src.models.teacher import Teacher
from src.models.enrollment import Enrollment


@pytest.mark.asyncio
async def test_create_enrollment(client, db_session):

    student_payload = {
        "full_name": "Enrollment Student",
        "email": "enrollmentstudent@example.com",
        "phone": "9876543227",
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

    # Verify student email
    verification_token = create_email_verification_token(
        student_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    # Create Student record
    student = Student(
        user_id=student_user_id,
        enrollment_number="ENR001",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)
    teacher_payload = {
        "full_name": "Enrollment Teacher",
        "email": "enrollmentteacher@example.com",
        "phone": "9876543228",
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

    # Verify teacher email
    verification_token = create_email_verification_token(
        teacher_user_id
    )

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    # Create Teacher record
    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="EMP005",
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

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
    }


    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Software Engineering",
            "code": "CS306",
            "description": "Software Engineering fundamentals",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
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
        headers=headers,
    )

    assert enrollment_response.status_code == 201

    data = enrollment_response.json()

    assert data["student_id"] == str(student.uid)
    assert data["subject_id"] == subject_id

@pytest.mark.asyncio
async def test_create_duplicate_enrollment(client, db_session):
    # Create student
    student_payload = {
        "full_name": "Duplicate Enrollment Student",
        "email": "duplicateenrollmentstudent@example.com",
        "phone": "9876543229",
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
        enrollment_number="ENR002",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Duplicate Enrollment Teacher",
        "email": "duplicateenrollmentteacher@example.com",
        "phone": "9876543230",
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
        employee_id="EMP006",
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

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Operating Systems",
            "code": "CS307",
            "description": "Operating Systems",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    enrollment_payload = {
        "student_id": str(student.uid),
        "subject_id": subject_id,
    }

    # First enrollment
    first_response = await client.post(
        "/api/v1/enrollments",
        json=enrollment_payload,
        headers=headers,
    )

    assert first_response.status_code == 201

    # Duplicate enrollment
    duplicate_response = await client.post(
        "/api/v1/enrollments",
        json=enrollment_payload,
        headers=headers,
    )

    assert duplicate_response.status_code == 409

    data = duplicate_response.json()
    assert data["message"] == "Student is already enrolled in this subject"

@pytest.mark.asyncio
async def test_get_student_enrollments(client, db_session):
    # Create student
    student_payload = {
        "full_name": "Get Enrollment Student",
        "email": "getenrollmentstudent@example.com",
        "phone": "9876543231",
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
        enrollment_number="ENR003",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Get Enrollment Teacher",
        "email": "getenrollmentteacher@example.com",
        "phone": "9876543232",
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
        employee_id="EMP007",
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

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Operating Systems",
            "code": "CS308",
            "description": "Operating Systems",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
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
        headers=headers,
    )

    assert enrollment_response.status_code == 201

    # Get student's enrollments
    response = await client.get(
        f"/api/v1/enrollments/student/{student.uid}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["student_id"] == str(student.uid)
    assert data[0]["subject_id"] == subject_id

@pytest.mark.asyncio
async def test_delete_enrollment(client, db_session):
    # Create student
    student_payload = {
        "full_name": "Delete Enrollment Student",
        "email": "deleteenrollmentstudent@example.com",
        "phone": "9876543233",
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

    verification_token = create_email_verification_token(student_user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    student = Student(
        user_id=student_user_id,
        enrollment_number="ENR004",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Delete Enrollment Teacher",
        "email": "deleteenrollmentteacher@example.com",
        "phone": "9876543234",
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

    verification_token = create_email_verification_token(teacher_user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="EMP008",
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

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    # Create subject
    subject_response = await client.post(
        "/api/v1/subjects",
        json={
            "name": "Computer Architecture",
            "code": "CS309",
            "description": "Computer Architecture",
            "teacher_id": str(teacher.uid),
        },
        headers=headers,
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
        headers=headers,
    )

    assert enrollment_response.status_code == 201

    enrollment_id = enrollment_response.json()["uid"]

    # Delete enrollment
    response = await client.delete(
        f"/api/v1/enrollments/{enrollment_id}",
        headers=headers,
    )

    assert response.status_code == 204

    # Verify enrollment no longer exists
    get_response = await client.get(
        f"/api/v1/enrollments/student/{student.uid}",
        headers=headers,
    )

    assert get_response.status_code == 200
    assert get_response.json() == []

@pytest.mark.asyncio
async def test_student_cannot_delete_enrollment(client, db_session):
    # Create student
    student_payload = {
        "full_name": "Unauthorized Enrollment Student",
        "email": "unauthorizedenrollment2@example.com",
        "phone": "9876543237",
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

    verification_token = create_email_verification_token(student_user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    student = Student(
        user_id=student_user_id,
        enrollment_number="ENR006",
        course="Computer Science",
        semester=6,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Authorization Teacher",
        "email": "authorizationteacher2@example.com",
        "phone": "9876543238",
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

    verification_token = create_email_verification_token(teacher_user_id)

    verify_response = await client.get(
        "/api/v1/auths/verify-email",
        params={"token": verification_token},
    )

    assert verify_response.status_code == 200

    teacher = Teacher(
        user_id=teacher_user_id,
        employee_id="EMP010",
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
            "name": "Compiler Design",
            "code": "CS310",
            "description": "Compiler Design",
            "teacher_id": str(teacher.uid),
        },
        headers=teacher_headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Create enrollment as teacher
    enrollment_response = await client.post(
        "/api/v1/enrollments",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
        },
        headers=teacher_headers,
    )

    assert enrollment_response.status_code == 201

    enrollment_id = enrollment_response.json()["uid"]

    # Login as student
    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": student_payload["email"],
            "password": student_payload["password"],
        },
    )

    assert login_response.status_code == 200

    student_token = login_response.json()["access_token"]

    # Student tries to delete enrollment
    response = await client.delete(
        f"/api/v1/enrollments/{enrollment_id}",
        headers={
            "Authorization": f"Bearer {student_token}",
        },
    )

    # Student should not be allowed to delete enrollment
    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "You do not have permission to access this resource"
