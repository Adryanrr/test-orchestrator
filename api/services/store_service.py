import requests


class StoreService:
    def __init__(self, session: requests.Session, base_url: str) -> None:
        self._session = session
        self._base_url = base_url

    def get_inventory(self) -> requests.Response:
        return self._session.get(f"{self._base_url}/store/inventory")

    def create_order(self, payload: dict[str, object]) -> requests.Response:
        return self._session.post(f"{self._base_url}/store/order", json=payload)

    def get_order(self, order_id: int) -> requests.Response:
        return self._session.get(f"{self._base_url}/store/order/{order_id}")

    def delete_order(self, order_id: int) -> requests.Response:
        return self._session.delete(f"{self._base_url}/store/order/{order_id}")
