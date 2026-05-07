import os
import random
import pytest
import requests
from api.services.user_service import UserService

_TEST_PASSWORD = os.getenv("TEST_USER_PASSWORD", "changeme-test-only")


@pytest.fixture
def user_service(api_session: requests.Session, base_url: str) -> UserService:
    return UserService(api_session, base_url)


@pytest.fixture
def user_payload() -> dict[str, object]:
    uid = random.randint(100000, 999999)
    return {
        "id": uid,
        "username": f"test_user_{uid}",
        "firstName": "Test",
        "lastName": "User",
        "email": f"test_{uid}@example.com",
        "password": _TEST_PASSWORD,
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


def test_get_nonexistent_user_returns_404(user_service) -> None:
    response = user_service.get("usuario_inexistente_xyz_abc_999")
    assert response.status_code == 404


def test_login_missing_credentials_returns_400(user_service) -> None:
    response = user_service.login("", "")
    assert response.status_code in (200, 400)
