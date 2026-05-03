import os
import random

import pytest
import requests

from api.services.pet_service import PetService

_DEFAULT_PET_CATEGORY_ID = int(os.getenv("TEST_PET_CATEGORY_ID", "1"))
_DEFAULT_PET_CATEGORY_NAME = os.getenv("TEST_PET_CATEGORY_NAME", "Dogs")
_DEFAULT_PET_STATUS = os.getenv("TEST_PET_STATUS", "available")


@pytest.fixture
def pet_service(api_session: requests.Session, base_url: str) -> PetService:
    return PetService(api_session, base_url)


@pytest.fixture
def pet_payload() -> dict[str, object]:
    pet_id = random.randint(100000, 999999)
    return {
        "id": pet_id,
        "name": f"TestDog_{pet_id}",
        "status": _DEFAULT_PET_STATUS,
        "photoUrls": ["http://example.com/photo.jpg"],
        "tags": [],
        "category": {"id": _DEFAULT_PET_CATEGORY_ID, "name": _DEFAULT_PET_CATEGORY_NAME},
    }


def test_create_pet_returns_200(pet_service: PetService, pet_payload: dict[str, object]) -> None:
    response = pet_service.create(pet_payload)
    assert response.status_code == 200
    assert response.json()["id"] == pet_payload["id"]


def test_get_pet_returns_correct_id(pet_service: PetService, pet_payload: dict[str, object]) -> None:
    pet_id: int = pet_payload["id"]  # type: ignore[assignment]
    pet_service.create(pet_payload)
    response = pet_service.get(pet_id)
    assert response.status_code == 200
    assert response.json()["id"] == pet_id


def test_update_pet_returns_200(pet_service: PetService, pet_payload: dict[str, object]) -> None:
    pet_service.create(pet_payload)
    updated = {**pet_payload, "name": "UpdatedDog"}
    response = pet_service.update(updated)
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedDog"


def test_find_pets_by_status_returns_list(
    pet_service: PetService, pet_payload: dict[str, object]
) -> None:
    pet_id: int = pet_payload["id"]  # type: ignore[assignment]
    pet_service.create(pet_payload)
    response = pet_service.find_by_status(_DEFAULT_PET_STATUS)
    assert response.status_code == 200
    pets = response.json()
    assert isinstance(pets, list)
    assert any(p["id"] == pet_id for p in pets)


def test_delete_pet_returns_200(pet_service: PetService, pet_payload: dict[str, object]) -> None:
    pet_id: int = pet_payload["id"]  # type: ignore[assignment]
    pet_service.create(pet_payload)
    response = pet_service.delete(pet_id)
    assert response.status_code == 200
