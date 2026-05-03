import requests


class UserService:
    def __init__(self, session: requests.Session, base_url: str) -> None:
        self._session = session
        self._base_url = base_url

    def create(self, payload: dict[str, object]) -> requests.Response:
        return self._session.post(f"{self._base_url}/user", json=payload)

    def get(self, username: str) -> requests.Response:
        return self._session.get(f"{self._base_url}/user/{username}")

    def update(self, username: str, payload: dict[str, object]) -> requests.Response:
        return self._session.put(f"{self._base_url}/user/{username}", json=payload)

    def delete(self, username: str) -> requests.Response:
        return self._session.delete(f"{self._base_url}/user/{username}")
