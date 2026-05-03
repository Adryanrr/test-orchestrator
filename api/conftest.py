from collections.abc import Generator
import pytest
import requests


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://petstore.swagger.io/v2"


@pytest.fixture(scope="session")
def api_session() -> Generator[requests.Session, None, None]:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()
