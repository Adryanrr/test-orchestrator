# Test Automation Monorepo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python monorepo with API test automation (Swagger Petstore) and Web E2E automation (SauceDemo), both with independent GitHub Actions CI pipelines.

**Architecture:** Two independent modules (`api/` and `web/`) sharing root-level tooling via `pyproject.toml`. Each module has a Service/Page Object layer that the tests consume — tests never call HTTP or Selenium directly. Configuration lives exclusively in `conftest.py` fixtures.

**Tech Stack:** Python 3.12, pytest, requests, selenium, webdriver-manager, pytest-html, GitHub Actions

---

### Task 1: Project Skeleton

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `api/__init__.py`
- Create: `api/services/__init__.py`
- Create: `api/requirements.txt`
- Create: `web/__init__.py`
- Create: `web/pages/__init__.py`
- Create: `web/requirements.txt`
- Create: `.github/workflows/` (directory)

- [ ] **Step 1: Create developer and feat/infra branches**

```bash
git checkout -b developer
git checkout -b feat/infra
```

- [ ] **Step 2: Create pyproject.toml**

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
addopts = "-v"
```

- [ ] **Step 3: Create .gitignore**

```
__pycache__/
*.pyc
*.pyo
.pytest_cache/
reports/
.env
*.egg-info/
dist/
build/
.DS_Store
```

- [ ] **Step 4: Create api module directories and empty init files**

```bash
mkdir -p api/services api/tests web/pages web/tests .github/workflows reports
touch api/__init__.py api/services/__init__.py web/__init__.py web/pages/__init__.py
```

- [ ] **Step 5: Create api/requirements.txt**

```
pytest==8.2.0
requests==2.32.2
pytest-html==4.1.1
```

- [ ] **Step 6: Create web/requirements.txt**

```
pytest==8.2.0
selenium==4.21.0
webdriver-manager==4.0.1
pytest-html==4.1.1
```

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml .gitignore api/ web/ .github/
git commit -m "feat: inicializar estrutura do monorepo"
```

---

### Task 2: API conftest

**Files:**
- Create: `api/conftest.py`

- [ ] **Step 1: Install API dependencies**

```bash
pip install -r api/requirements.txt
```

- [ ] **Step 2: Create api/conftest.py**

```python
import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return "https://petstore.swagger.io/v2"


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()
```

- [ ] **Step 3: Verify pytest can collect the module**

```bash
pytest api/ --collect-only
```

Expected: `no tests ran` (no errors)

- [ ] **Step 4: Commit**

```bash
git add api/conftest.py
git commit -m "feat: adicionar conftest e fixtures de sessão para testes de API"
```

---

### Task 3: UserService (TDD)

**Files:**
- Create: `api/tests/test_user.py`
- Create: `api/services/user_service.py`

- [ ] **Step 1: Write the failing test**

Create `api/tests/test_user.py`:

```python
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
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
pytest api/tests/test_user.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'api.services.user_service'`

- [ ] **Step 3: Implement UserService**

Create `api/services/user_service.py`:

```python
class UserService:
    def __init__(self, session, base_url):
        self._session = session
        self._base_url = base_url

    def create(self, payload):
        return self._session.post(f"{self._base_url}/user", json=payload)

    def get(self, username):
        return self._session.get(f"{self._base_url}/user/{username}")

    def update(self, username, payload):
        return self._session.put(f"{self._base_url}/user/{username}", json=payload)

    def delete(self, username):
        return self._session.delete(f"{self._base_url}/user/{username}")
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
pytest api/tests/test_user.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add api/services/user_service.py api/tests/test_user.py
git commit -m "feat: implementar UserService com endpoints CRUD"
```

---

### Task 4: StoreService (TDD)

**Files:**
- Create: `api/tests/test_store.py`
- Create: `api/services/store_service.py`

- [ ] **Step 1: Write the failing test**

Create `api/tests/test_store.py`:

```python
import random
import pytest
from api.services.store_service import StoreService


@pytest.fixture
def store_service(api_session, base_url):
    return StoreService(api_session, base_url)


@pytest.fixture
def order_payload():
    order_id = random.randint(100000, 999999)
    return {
        "id": order_id,
        "petId": 1,
        "quantity": 1,
        "shipDate": "2026-05-02T00:00:00.000Z",
        "status": "placed",
        "complete": True,
    }


def test_get_inventory_returns_200(store_service):
    response = store_service.get_inventory()
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_create_order_returns_200(store_service, order_payload):
    response = store_service.create_order(order_payload)
    assert response.status_code == 200


def test_get_order_returns_correct_id(store_service, order_payload):
    store_service.create_order(order_payload)
    response = store_service.get_order(order_payload["id"])
    assert response.status_code == 200
    assert response.json()["id"] == order_payload["id"]


def test_delete_order_returns_200(store_service, order_payload):
    store_service.create_order(order_payload)
    response = store_service.delete_order(order_payload["id"])
    assert response.status_code == 200
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
pytest api/tests/test_store.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'api.services.store_service'`

- [ ] **Step 3: Implement StoreService**

Create `api/services/store_service.py`:

```python
class StoreService:
    def __init__(self, session, base_url):
        self._session = session
        self._base_url = base_url

    def get_inventory(self):
        return self._session.get(f"{self._base_url}/store/inventory")

    def create_order(self, payload):
        return self._session.post(f"{self._base_url}/store/order", json=payload)

    def get_order(self, order_id):
        return self._session.get(f"{self._base_url}/store/order/{order_id}")

    def delete_order(self, order_id):
        return self._session.delete(f"{self._base_url}/store/order/{order_id}")
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
pytest api/tests/test_store.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add api/services/store_service.py api/tests/test_store.py
git commit -m "feat: implementar StoreService com endpoints de pedido"
```

---

### Task 5: PetService (TDD)

**Files:**
- Create: `api/tests/test_pet.py`
- Create: `api/services/pet_service.py`

- [ ] **Step 1: Write the failing test**

Create `api/tests/test_pet.py`:

```python
import random
import pytest
from api.services.pet_service import PetService


@pytest.fixture
def pet_service(api_session, base_url):
    return PetService(api_session, base_url)


@pytest.fixture
def pet_payload():
    pet_id = random.randint(100000, 999999)
    return {
        "id": pet_id,
        "name": f"TestDog_{pet_id}",
        "status": "available",
        "photoUrls": ["http://example.com/photo.jpg"],
        "tags": [],
        "category": {"id": 1, "name": "Dogs"},
    }


def test_create_pet_returns_200(pet_service, pet_payload):
    response = pet_service.create(pet_payload)
    assert response.status_code == 200
    assert response.json()["id"] == pet_payload["id"]


def test_get_pet_returns_correct_id(pet_service, pet_payload):
    pet_service.create(pet_payload)
    response = pet_service.get(pet_payload["id"])
    assert response.status_code == 200
    assert response.json()["id"] == pet_payload["id"]


def test_update_pet_returns_200(pet_service, pet_payload):
    pet_service.create(pet_payload)
    updated = {**pet_payload, "name": "UpdatedDog"}
    response = pet_service.update(updated)
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedDog"


def test_find_pets_by_status_returns_list(pet_service):
    response = pet_service.find_by_status("available")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_pet_returns_200(pet_service, pet_payload):
    pet_service.create(pet_payload)
    response = pet_service.delete(pet_payload["id"])
    assert response.status_code == 200
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
pytest api/tests/test_pet.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'api.services.pet_service'`

- [ ] **Step 3: Implement PetService**

Create `api/services/pet_service.py`:

```python
class PetService:
    def __init__(self, session, base_url):
        self._session = session
        self._base_url = base_url

    def create(self, payload):
        return self._session.post(f"{self._base_url}/pet", json=payload)

    def get(self, pet_id):
        return self._session.get(f"{self._base_url}/pet/{pet_id}")

    def update(self, payload):
        return self._session.put(f"{self._base_url}/pet", json=payload)

    def find_by_status(self, status):
        return self._session.get(
            f"{self._base_url}/pet/findByStatus", params={"status": status}
        )

    def delete(self, pet_id):
        return self._session.delete(f"{self._base_url}/pet/{pet_id}")
```

- [ ] **Step 4: Run full API suite to confirm all pass**

```bash
pytest api/tests/ -v --junitxml=reports/api-results.xml --html=reports/api-report.html --self-contained-html
```

Expected: 13 passed

- [ ] **Step 5: Commit**

```bash
git add api/services/pet_service.py api/tests/test_pet.py
git commit -m "feat: implementar PetService com endpoints de pet"
```

---

### Task 6: API CI Pipeline + Merge

**Files:**
- Create: `.github/workflows/api-tests.yml`

- [ ] **Step 1: Create .github/workflows/api-tests.yml**

```yaml
name: API Tests

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  api-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r api/requirements.txt

      - name: Run API tests
        run: pytest api/tests/ --junitxml=reports/api-results.xml --html=reports/api-report.html --self-contained-html
        env:
          PYTHONPATH: ${{ github.workspace }}

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: api-report
          path: reports/
```

- [ ] **Step 2: Commit and push feat/infra to trigger pipeline**

```bash
git add .github/workflows/api-tests.yml
git commit -m "feat: configurar GitHub Actions para api-tests"
git push -u origin feat/infra
```

- [ ] **Step 3: Verify pipeline passed on GitHub**

Open GitHub → Actions → confirm `API Tests` workflow is green.

- [ ] **Step 4: Merge feat/infra into developer**

```bash
git checkout developer
git merge feat/infra --no-ff -m "chore: merge feat/infra into developer"
git push origin developer
```

---

### Task 7: Web Base Setup

**Files:**
- Create: `web/conftest.py`

- [ ] **Step 1: Create feat/web-tests branch from developer**

```bash
git checkout -b feat/web-tests
```

- [ ] **Step 2: Install web dependencies**

```bash
pip install -r web/requirements.txt
```

- [ ] **Step 3: Create web/conftest.py**

```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=options)
    chrome_driver.implicitly_wait(10)
    yield chrome_driver
    chrome_driver.quit()
```

- [ ] **Step 4: Commit**

```bash
git add web/conftest.py
git commit -m "feat: adicionar conftest e fixture do WebDriver para testes web"
```

---

### Task 8: Write E2E Test (RED)

**Files:**
- Create: `web/tests/test_e2e_purchase.py`

- [ ] **Step 1: Write the failing test**

Create `web/tests/test_e2e_purchase.py`:

```python
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage


def test_complete_purchase_flow(driver):
    login = LoginPage(driver)
    login.open()
    login.fill_credentials("standard_user", "secret_sauce")
    login.click_login()

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()

    cart = CartPage(driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_info("Test", "User", "12345")
    checkout.finish()

    assert checkout.get_confirmation_message() == "Thank you for your order!"
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
pytest web/tests/test_e2e_purchase.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'web.pages.login_page'`

---

### Task 9: Implement Page Objects (GREEN)

**Files:**
- Create: `web/pages/login_page.py`
- Create: `web/pages/inventory_page.py`
- Create: `web/pages/cart_page.py`
- Create: `web/pages/checkout_page.py`

- [ ] **Step 1: Implement LoginPage**

Create `web/pages/login_page.py`:

```python
from selenium.webdriver.common.by import By


class LoginPage:
    URL = "https://www.saucedemo.com/"
    _username = (By.ID, "user-name")
    _password = (By.ID, "password")
    _login_btn = (By.ID, "login-button")

    def __init__(self, driver):
        self._driver = driver

    def open(self):
        self._driver.get(self.URL)

    def fill_credentials(self, username, password):
        self._driver.find_element(*self._username).send_keys(username)
        self._driver.find_element(*self._password).send_keys(password)

    def click_login(self):
        self._driver.find_element(*self._login_btn).click()
```

- [ ] **Step 2: Implement InventoryPage**

Create `web/pages/inventory_page.py`:

```python
from selenium.webdriver.common.by import By


class InventoryPage:
    _add_to_cart_btn = (By.CSS_SELECTOR, ".inventory_item button")
    _cart_link = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self._driver = driver

    def add_first_item_to_cart(self):
        self._driver.find_elements(*self._add_to_cart_btn)[0].click()

    def go_to_cart(self):
        self._driver.find_element(*self._cart_link).click()
```

- [ ] **Step 3: Implement CartPage**

Create `web/pages/cart_page.py`:

```python
from selenium.webdriver.common.by import By


class CartPage:
    _checkout_btn = (By.ID, "checkout")

    def __init__(self, driver):
        self._driver = driver

    def proceed_to_checkout(self):
        self._driver.find_element(*self._checkout_btn).click()
```

- [ ] **Step 4: Implement CheckoutPage**

Create `web/pages/checkout_page.py`:

```python
from selenium.webdriver.common.by import By


class CheckoutPage:
    _first_name = (By.ID, "first-name")
    _last_name = (By.ID, "last-name")
    _zip_code = (By.ID, "postal-code")
    _continue_btn = (By.ID, "continue")
    _finish_btn = (By.ID, "finish")
    _confirmation = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self._driver = driver

    def fill_info(self, first_name, last_name, zip_code):
        self._driver.find_element(*self._first_name).send_keys(first_name)
        self._driver.find_element(*self._last_name).send_keys(last_name)
        self._driver.find_element(*self._zip_code).send_keys(zip_code)
        self._driver.find_element(*self._continue_btn).click()

    def finish(self):
        self._driver.find_element(*self._finish_btn).click()

    def get_confirmation_message(self):
        return self._driver.find_element(*self._confirmation).text
```

- [ ] **Step 5: Run E2E test to confirm it passes**

```bash
pytest web/tests/test_e2e_purchase.py -v --junitxml=reports/web-results.xml --html=reports/web-report.html --self-contained-html
```

Expected: 1 passed

- [ ] **Step 6: Commit**

```bash
git add web/tests/test_e2e_purchase.py web/pages/
git commit -m "feat: implementar Page Objects e fluxo E2E de compra no SauceDemo"
```

---

### Task 10: Web CI Pipeline + Merge

**Files:**
- Create: `.github/workflows/web-tests.yml`

- [ ] **Step 1: Create .github/workflows/web-tests.yml**

```yaml
name: Web Tests

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  web-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r web/requirements.txt

      - name: Run Web tests
        run: pytest web/tests/ --junitxml=reports/web-results.xml --html=reports/web-report.html --self-contained-html
        env:
          PYTHONPATH: ${{ github.workspace }}

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: web-report
          path: reports/
```

- [ ] **Step 2: Commit and push feat/web-tests**

```bash
git add .github/workflows/web-tests.yml
git commit -m "feat: configurar GitHub Actions para web-tests"
git push -u origin feat/web-tests
```

- [ ] **Step 3: Verify pipeline passed on GitHub**

Open GitHub → Actions → confirm `Web Tests` workflow is green.

- [ ] **Step 4: Merge feat/web-tests into developer**

```bash
git checkout developer
git merge feat/web-tests --no-ff -m "chore: merge feat/web-tests into developer"
git push origin developer
```

---

### Task 11: README + Entrega Final

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create feat/docs branch from developer**

```bash
git checkout -b feat/docs
```

- [ ] **Step 2: Create README.md at project root**

Content (replace `<usuario>` and `<repo>` with your GitHub username and repository name):

```markdown
# Test Automation Monorepo

Monorepo com automação de testes de API e Web E2E em Python.

| Pipeline | Status |
|----------|--------|
| API Tests | ![API Tests](https://github.com/<usuario>/<repo>/actions/workflows/api-tests.yml/badge.svg) |
| Web Tests | ![Web Tests](https://github.com/<usuario>/<repo>/actions/workflows/web-tests.yml/badge.svg) |

## Tecnologias

| Módulo | Ferramentas |
|--------|-------------|
| API    | Python 3.12, pytest, requests, pytest-html |
| Web    | Python 3.12, pytest, selenium, webdriver-manager, pytest-html |
| CI     | GitHub Actions |

## Estrutura

```
test-orchestrator/
├── api/
│   ├── services/     # Service Layer (UserService, StoreService, PetService)
│   ├── tests/        # Casos de teste de API
│   └── conftest.py   # Fixtures: base_url, api_session
├── web/
│   ├── pages/        # Page Objects (Login, Inventory, Cart, Checkout)
│   ├── tests/        # Casos de teste E2E
│   └── conftest.py   # Fixture: driver (Chrome headless)
├── .github/
│   └── workflows/
│       ├── api-tests.yml
│       └── web-tests.yml
└── pyproject.toml
```

## Instalação

```bash
pip install -r api/requirements.txt   # para testes de API
pip install -r web/requirements.txt   # para testes Web
```

## Execução

```bash
# Testes de API
pytest api/tests/ -v

# Testes Web E2E
pytest web/tests/ -v

# Com relatório HTML
pytest api/tests/ --html=reports/api-report.html --self-contained-html
pytest web/tests/ --html=reports/web-report.html --self-contained-html
```

## CI/CD

Ambas as pipelines disparam automaticamente em `push` e `pull_request` para qualquer branch.
Os artefatos (HTML reports) ficam disponíveis para download na aba Actions do GitHub.

## Prints

*(Adicionar screenshots dos relatórios e da pipeline após a primeira execução)*
```

- [ ] **Step 3: Update badges in README with actual GitHub username and repository name**

Edit the two badge URLs in the table to use the real values.

- [ ] **Step 4: Commit README**

```bash
git add README.md
git commit -m "docs: adicionar README com instruções e prints"
```

- [ ] **Step 5: Push feat/docs and merge to developer**

```bash
git push -u origin feat/docs
git checkout developer
git merge feat/docs --no-ff -m "chore: merge feat/docs into developer"
git push origin developer
```

- [ ] **Step 6: Merge developer into main (entrega final)**

```bash
git checkout main
git merge developer --no-ff -m "chore: merge developer into main para entrega final"
git push origin main
```

- [ ] **Step 7: Add screenshots to README**

After all pipelines are green:
1. Go to GitHub Actions → `API Tests` → download `api-report` artifact → open `api-report.html` → screenshot
2. Go to GitHub Actions → `Web Tests` → download `web-report` artifact → open `web-report.html` → screenshot
3. Screenshot the GitHub Actions tab showing both workflows green
4. Add the screenshots to `README.md` under the **Prints** section and commit:

```bash
git add README.md
git commit -m "docs: adicionar prints das pipelines e relatórios de teste"
git push origin main
```

---

## Self-Review Checklist

**Spec coverage:**
- [x] ARCH-01 — Task 1 (monorepo structure + pyproject.toml)
- [x] ARCH-02 — Commits semânticos usados em cada task
- [x] ARCH-03 — Task 11 (README.md unificado)
- [x] API-01 — Tasks 3 (UserService + test_user.py)
- [x] API-02 — Task 4 (StoreService + test_store.py)
- [x] API-03 — Task 5 (PetService + test_pet.py)
- [x] WEB-01 — Task 9 (4 Page Objects implementados)
- [x] WEB-02 — Tasks 8–9 (test_e2e_purchase.py: login → carrinho → checkout)
- [x] CI-01 — Task 6 (api-tests.yml)
- [x] CI-02 — Task 10 (web-tests.yml)
