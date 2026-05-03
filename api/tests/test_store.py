import random
import os
import pytest
import requests
from api.services.store_service import StoreService

_TEST_ORDER_PET_ID = int(os.getenv("TEST_ORDER_PET_ID", "1"))


@pytest.fixture
def store_service(api_session: requests.Session, base_url: str) -> StoreService:
    return StoreService(api_session, base_url)


@pytest.fixture
def order_payload() -> dict[str, object]:
    order_id = random.randint(100000, 999999)
    return {
        "id": order_id,
        "petId": _TEST_ORDER_PET_ID,
        "quantity": 1,
        "shipDate": "2026-05-02T00:00:00.000Z",
        "status": "placed",
        "complete": True,
    }


def test_get_inventory_returns_200(store_service: StoreService) -> None:
    response = store_service.get_inventory()
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_create_order_returns_200(store_service: StoreService, order_payload: dict[str, object]) -> None:
    response = store_service.create_order(order_payload)
    assert response.status_code == 200


def test_get_order_returns_correct_id(store_service: StoreService, order_payload: dict[str, object]) -> None:
    store_service.create_order(order_payload)
    response = store_service.get_order(int(order_payload["id"]))
    assert response.status_code == 200
    assert response.json()["id"] == order_payload["id"]


def test_delete_order_returns_200(store_service: StoreService, order_payload: dict[str, object]) -> None:
    store_service.create_order(order_payload)
    response = store_service.delete_order(int(order_payload["id"]))
    assert response.status_code == 200
