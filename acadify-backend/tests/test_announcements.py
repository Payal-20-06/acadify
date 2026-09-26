import pytest
from uuid import uuid4

from src.core.security import create_email_verification_token
from src.models.teacher import Teacher


async def create_verified_teacher(
    client,
    db_session,
    *,
    email: str,
    phone: str,
    employee_id: str,
):
    teacher_payload = {
        "full_name": "Announcement Test Teacher",
        "email": email,
        "phone": phone,
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
        employee_id=employee_id,
        department="Computer Science",
        designation="Assistant Professor",
    )

    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)

    login_response = await client.post(
        "/api/v1/auths/login",
        json={
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return teacher, {
        "Authorization": f"Bearer {token}",
    }


@pytest.mark.asyncio
async def test_create_announcement(
    client,
    db_session,
):
    teacher, headers = await create_verified_teacher(
        client,
        db_session,
        email="announcement_teacher@example.com",
        phone="9876543270",
        employee_id="ANN001",
    )

    response = await client.post(
        "/api/v1/announcements",
        json={
            "title": "Mid Semester Examination",
            "content": (
                "The mid semester examination schedule "
                "has been released."
            ),
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Mid Semester Examination"
    assert (
        data["content"]
        == "The mid semester examination schedule "
        "has been released."
    )
    assert data["created_by"] == str(teacher.user_id)
    assert "uid" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_announcement(
    client,
    db_session,
):
    teacher, headers = await create_verified_teacher(
        client,
        db_session,
        email="get_announcement_teacher@example.com",
        phone="9876543271",
        employee_id="ANN002",
    )

    create_response = await client.post(
        "/api/v1/announcements",
        json={
            "title": "Assignment Submission",
            "content": "Submit your assignment before Friday.",
        },
        headers=headers,
    )

    assert create_response.status_code == 201

    announcement_id = create_response.json()["uid"]

    response = await client.get(
        f"/api/v1/announcements/{announcement_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["uid"] == announcement_id
    assert data["title"] == "Assignment Submission"
    assert data["content"] == "Submit your assignment before Friday."
    assert data["created_by"] == str(teacher.user_id)


@pytest.mark.asyncio
async def test_get_all_announcements(
    client,
    db_session,
):
    _, headers = await create_verified_teacher(
        client,
        db_session,
        email="all_announcements_teacher@example.com",
        phone="9876543272",
        employee_id="ANN003",
    )

    first_response = await client.post(
        "/api/v1/announcements",
        json={
            "title": "First Announcement",
            "content": "First announcement content.",
        },
        headers=headers,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/announcements",
        json={
            "title": "Second Announcement",
            "content": "Second announcement content.",
        },
        headers=headers,
    )

    assert second_response.status_code == 201

    response = await client.get(
        "/api/v1/announcements",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    titles = {announcement["title"] for announcement in data}

    assert "First Announcement" in titles
    assert "Second Announcement" in titles


@pytest.mark.asyncio
async def test_get_nonexistent_announcement(
    client,
    db_session,
):
    _, headers = await create_verified_teacher(
        client,
        db_session,
        email="missing_announcement_teacher@example.com",
        phone="9876543273",
        employee_id="ANN004",
    )

    fake_announcement_id = uuid4()

    response = await client.get(
        f"/api/v1/announcements/{fake_announcement_id}",
        headers=headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Announcement not found"


@pytest.mark.asyncio
async def test_delete_announcement(
    client,
    db_session,
):
    _, headers = await create_verified_teacher(
        client,
        db_session,
        email="delete_announcement_teacher@example.com",
        phone="9876543274",
        employee_id="ANN005",
    )

    create_response = await client.post(
        "/api/v1/announcements",
        json={
            "title": "Delete Announcement",
            "content": "This announcement will be deleted.",
        },
        headers=headers,
    )

    assert create_response.status_code == 201

    announcement_id = create_response.json()["uid"]

    delete_response = await client.delete(
        f"/api/v1/announcements/{announcement_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    get_response = await client.get(
        f"/api/v1/announcements/{announcement_id}",
        headers=headers,
    )

    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_announcement(
    client,
    db_session,
):
    _, headers = await create_verified_teacher(
        client,
        db_session,
        email="delete_missing_teacher@example.com",
        phone="9876543275",
        employee_id="ANN006",
    )

    fake_announcement_id = uuid4()

    response = await client.delete(
        f"/api/v1/announcements/{fake_announcement_id}",
        headers=headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "Announcement not found"