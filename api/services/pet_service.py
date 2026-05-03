import requests


class PetService:
    def __init__(self, session: requests.Session, base_url: str) -> None:
        self._session = session
        self._base_url = base_url

    def create(self, payload: dict[str, object]) -> requests.Response:
        return self._session.post(f"{self._base_url}/pet", json=payload)

    def get(self, pet_id: int) -> requests.Response:
        return self._session.get(f"{self._base_url}/pet/{pet_id}")

    def update(self, payload: dict[str, object]) -> requests.Response:
        return self._session.put(f"{self._base_url}/pet", json=payload)

    def find_by_status(self, status: str) -> requests.Response:
        return self._session.get(
            f"{self._base_url}/pet/findByStatus", params={"status": status}
        )

    def delete(self, pet_id: int) -> requests.Response:
        return self._session.delete(f"{self._base_url}/pet/{pet_id}")
