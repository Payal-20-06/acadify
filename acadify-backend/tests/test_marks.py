import pytest

from src.core.security import create_email_verification_token
from src.models.student import Student
from src.models.teacher import Teacher


@pytest.mark.asyncio
async def test_create_marks(
    client,
    db_session,
):
    # Create student
    student_payload = {
        "full_name": "Marks Test Student",
        "email": "marks_student@example.com",
        "phone": "9876543250",
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
        enrollment_number="MARK001",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Marks Test Teacher",
        "email": "marks_teacher@example.com",
        "phone": "9876543251",
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
        employee_id="MARKT001",
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
            "name": "Data Structures",
            "code": "CS401",
            "description": "Data Structures",
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

    # Create marks
    marks_response = await client.post(
        "/api/v1/marks",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
            "assessment_type": "Mid Semester",
            "marks_obtained": 42,
            "max_marks": 50,
        },
        headers=teacher_headers,
    )

    assert marks_response.status_code == 201

    data = marks_response.json()

    assert data["student_id"] == str(student.uid)
    assert data["subject_id"] == subject_id
    assert data["assessment_type"] == "Mid Semester"
    assert data["marks_obtained"] == 42
    assert data["max_marks"] == 50

@pytest.mark.asyncio
async def test_create_invalid_marks(
    client,
    db_session,
):
    # Create student
    student_payload = {
        "full_name": "Invalid Marks Student",
        "email": "invalid_marks_student@example.com",
        "phone": "9876543252",
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
        enrollment_number="MARK002",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Invalid Marks Teacher",
        "email": "invalid_marks_teacher@example.com",
        "phone": "9876543253",
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
        employee_id="MARKT002",
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
            "name": "Operating Systems",
            "code": "CS402",
            "description": "Operating Systems",
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

    # Try to create invalid marks
    marks_response = await client.post(
        "/api/v1/marks",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
            "assessment_type": "Mid Semester",
            "marks_obtained": 60,
            "max_marks": 50,
        },
        headers=teacher_headers,
    )

    assert marks_response.status_code == 400

    data = marks_response.json()

    assert data["message"] ==  "Marks obtained cannot be greater than maximum marks"


@pytest.mark.asyncio
async def test_create_marks_student_not_enrolled(
    client,
    db_session,
):
    # Create student
    student_payload = {
        "full_name": "Not Enrolled Marks Student",
        "email": "marks_not_enrolled@example.com",
        "phone": "9876543254",
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
        enrollment_number="MARK003",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Not Enrolled Marks Teacher",
        "email": "marks_not_enrolled_teacher@example.com",
        "phone": "9876543255",
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
        employee_id="MARKT003",
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
            "code": "CS404",
            "description": "Database Systems",
            "teacher_id": str(teacher.uid),
        },
        headers=teacher_headers,
    )

    assert subject_response.status_code == 201

    subject_id = subject_response.json()["uid"]

    # Do NOT create enrollment.
    # The student is intentionally not enrolled in the subject.

    marks_response = await client.post(
        "/api/v1/marks",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
            "assessment_type": "Mid Semester",
            "marks_obtained": 40,
            "max_marks": 50,
        },
        headers=teacher_headers,
    )

    assert marks_response.status_code == 400

    data = marks_response.json()

    assert data["message"] == "Student is not enrolled in this subject"

@pytest.mark.asyncio
async def test_get_student_marks(
    client,
    db_session,
):
    # Create student
    student_payload = {
        "full_name": "Get Marks Student",
        "email": "get_marks_student@example.com",
        "phone": "9876543256",
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
        enrollment_number="MARK004",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Get Marks Teacher",
        "email": "get_marks_teacher@example.com",
        "phone": "9876543257",
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
        employee_id="MARKT004",
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
            "name": "Computer Architecture",
            "code": "CS405",
            "description": "Computer Architecture",
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

    # Create marks
    marks_response = await client.post(
        "/api/v1/marks",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
            "assessment_type": "Mid Semester",
            "marks_obtained": 45,
            "max_marks": 50,
        },
        headers=teacher_headers,
    )

    assert marks_response.status_code == 201

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

    student_headers = {
        "Authorization": f"Bearer {student_token}",
    }

    # Get student's marks
    marks_response = await client.get(
        f"/api/v1/marks/student/{student.uid}",
        headers=student_headers,
    )

    assert marks_response.status_code == 200

    data = marks_response.json()

    assert len(data) == 1
    assert data[0]["student_id"] == str(student.uid)
    assert data[0]["subject_id"] == subject_id
    assert data[0]["assessment_type"] == "Mid Semester"
    assert data[0]["marks_obtained"] == 45
    assert data[0]["max_marks"] == 50

@pytest.mark.asyncio
async def test_get_marks(
    client,
    db_session,
):
    # Create student
    student_payload = {
        "full_name": "Single Marks Student",
        "email": "single_marks_student@example.com",
        "phone": "9876543258",
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
        enrollment_number="MARK005",
        course="Computer Science",
        semester=5,
    )

    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    # Create teacher
    teacher_payload = {
        "full_name": "Single Marks Teacher",
        "email": "single_marks_teacher@example.com",
        "phone": "9876543259",
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
        employee_id="MARKT005",
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
            "name": "Software Engineering",
            "code": "CS406",
            "description": "Software Engineering",
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

    # Create marks
    marks_response = await client.post(
        "/api/v1/marks",
        json={
            "student_id": str(student.uid),
            "subject_id": subject_id,
            "assessment_type": "End Semester",
            "marks_obtained": 85,
            "max_marks": 100,
        },
        headers=teacher_headers,
    )

    assert marks_response.status_code == 201

    marks_id = marks_response.json()["uid"]

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

    student_headers = {
        "Authorization": f"Bearer {student_token}",
    }

    # Get single marks record
    response = await client.get(
        f"/api/v1/marks/{marks_id}",
        headers=student_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["uid"] == marks_id
    assert data["student_id"] == str(student.uid)
    assert data["subject_id"] == subject_id
    assert data["assessment_type"] == "End Semester"
    assert data["marks_obtained"] == 85
    assert data["max_marks"] == 100
