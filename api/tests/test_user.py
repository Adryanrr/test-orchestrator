import random
import pytest
from api.services.user_service import UserService


@pytest.fixture
def user_service(api_session, base_url):
    return UserService(api_session, base_url)


@pytest.fixture
def user_payload():
    uid = random.randint(100000, 999999)
    return {
        "id": uid,
        "username": f"test_user_{uid}",
        "firstName": "Test",
        "lastName": "User",
        "email": f"test_{uid}@example.com",
        "password": "password123",
        "phone": "5511999999999",
        "userStatus": 1,
    }


def test_create_user_returns_200(user_service, user_payload):
    response = user_service.create(user_payload)
    assert response.status_code == 200


def test_get_user_returns_username(user_service, user_payload):
    user_service.create(user_payload)
    response = user_service.get(user_payload["username"])
    assert response.status_code == 200
    assert response.json()["username"] == user_payload["username"]


def test_update_user_returns_200(user_service, user_payload):
    user_service.create(user_payload)
    updated = {**user_payload, "firstName": "Updated"}
    response = user_service.update(user_payload["username"], updated)
    assert response.status_code == 200


def test_delete_user_returns_200(user_service, user_payload):
    user_service.create(user_payload)
    response = user_service.delete(user_payload["username"])
    assert response.status_code == 200
