# Apresentação Acadêmica — Slides + Site Estático — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar slides Reveal.js para o dia 07/05, testes negativos de API e Web, e site estático de documentação para o dia 14/05.

**Architecture:** Cinco tarefas em sequência por prioridade. Tarefas 1–2 adicionam testes negativos ao código existente. Tarefa 3 cria `slides/index.html` (prioridade máxima — apresentação amanhã). Tarefas 4–5 criam o site estático em `docs/web/`.

**Tech Stack:** Python 3.12, pytest, requests, selenium. Reveal.js 5.1 + highlight.js (CDN). Prism.js 1.29 (CDN). HTML/CSS/JS vanilla — zero build step, zero servidor.

---

### Task 1: Testes negativos de API

**Files:**
- Modify: `api/services/user_service.py` — adicionar método `login`
- Modify: `api/tests/test_pet.py` — 2 testes negativos
- Modify: `api/tests/test_store.py` — 1 teste negativo
- Modify: `api/tests/test_user.py` — 2 testes negativos

- [ ] **Step 1: Adicionar `login` ao UserService**

Em `api/services/user_service.py`, adicionar ao final da classe:

```python
def login(self, username: str, password: str) -> requests.Response:
    return self._session.get(
        f"{self._base_url}/user/login",
        params={"username": username, "password": password},
    )
```

- [ ] **Step 2: Adicionar negativos em `api/tests/test_pet.py`**

Ao final do arquivo, adicionar:

```python
def test_get_nonexistent_pet_returns_404(pet_service: PetService) -> None:
    response = pet_service.get(9_999_999_999)
    assert response.status_code == 404


def test_create_pet_invalid_payload_returns_error(pet_service: PetService) -> None:
    response = pet_service.create({})
    assert response.status_code in (400, 405, 500)
```

- [ ] **Step 3: Rodar e verificar**

```bash
pytest api/tests/test_pet.py -k "nonexistent or invalid_payload" -v
```

Esperado: 2 PASSED.

- [ ] **Step 4: Adicionar negativo em `api/tests/test_store.py`**

Ao final do arquivo, adicionar:

```python
def test_get_nonexistent_order_returns_404(store_service: StoreService) -> None:
    response = store_service.get_order(9_999_999_999)
    assert response.status_code == 404
```

- [ ] **Step 5: Rodar**

```bash
pytest api/tests/test_store.py::test_get_nonexistent_order_returns_404 -v
```

Esperado: PASSED.

- [ ] **Step 6: Adicionar negativos em `api/tests/test_user.py`**

Ao final do arquivo, adicionar:

```python
def test_get_nonexistent_user_returns_404(user_service) -> None:
    response = user_service.get("usuario_inexistente_xyz_abc_999")
    assert response.status_code == 404


def test_login_missing_credentials_returns_400(user_service) -> None:
    response = user_service.login("", "")
    assert response.status_code == 400
```

- [ ] **Step 7: Rodar toda a suite de API**

```bash
pytest api/tests/ -v
```

Esperado: todos PASSED (positivos + negativos).

- [ ] **Step 8: Commit**

```bash
git add api/services/user_service.py api/tests/test_pet.py api/tests/test_store.py api/tests/test_user.py
git commit -m "test: adicionar casos negativos nos testes de API (404, 400, 405)"
```

---

### Task 2: Testes negativos Web

**Files:**
- Modify: `web/pages/login_page.py` — adicionar `attempt_login` e `get_error_message`
- Modify: `web/tests/test_e2e_purchase.py` — 2 testes negativos de login

- [ ] **Step 1: Atualizar `web/pages/login_page.py`**

Adicionar o locator `_error_msg` e dois métodos à classe `LoginPage`. O arquivo completo ficará assim:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    URL = "https://www.saucedemo.com/"
    _username = (By.ID, "user-name")
    _password = (By.ID, "password")
    _login_btn = (By.ID, "login-button")
    _error_msg = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def open(self) -> None:
        self._driver.get(self.URL)
        self._wait.until(EC.visibility_of_element_located(self._username))

    def fill_credentials(self, username: str, password: str) -> None:
        self._wait.until(EC.visibility_of_element_located(self._username)).send_keys(username)
        self._wait.until(EC.visibility_of_element_located(self._password)).send_keys(password)

    def click_login(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._login_btn)).click()
        self._wait.until(EC.url_contains("inventory"))

    def attempt_login(self) -> None:
        """Click login sem aguardar redirecionamento — para cenários de erro."""
        self._wait.until(EC.element_to_be_clickable(self._login_btn)).click()

    def get_error_message(self) -> str:
        return self._wait.until(EC.visibility_of_element_located(self._error_msg)).text
```

- [ ] **Step 2: Adicionar testes em `web/tests/test_e2e_purchase.py`**

Ao final do arquivo (após as importações existentes), adicionar:

```python
def test_login_invalid_credentials(driver):
    login = LoginPage(driver)
    login.open()
    login.fill_credentials("standard_user", "wrong_password")
    login.attempt_login()
    assert "Username and password do not match" in login.get_error_message()


def test_login_locked_user(driver):
    login = LoginPage(driver)
    login.open()
    login.fill_credentials("locked_out_user", "secret_sauce")
    login.attempt_login()
    assert "locked out" in login.get_error_message()
```

- [ ] **Step 3: Rodar todos os testes web**

```bash
pytest web/tests/ -v
```

Esperado: 3 PASSED (1 positivo + 2 negativos).

- [ ] **Step 4: Commit**

```bash
git add web/pages/login_page.py web/tests/test_e2e_purchase.py
git commit -m "test: adicionar testes negativos de login web (credenciais inválidas e usuário bloqueado)"
```

---

### Task 3: Slides Reveal.js

**Files:**
- Create: `slides/index.html`

- [ ] **Step 1: Criar diretório**

```bash
mkdir -p slides
```

- [ ] **Step 2: Criar `slides/index.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Test Orchestrator — Automação de Testes</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reset.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/black.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/monokai.css">
  <style>
    :root { --r-main-font-size: 26px; }
    .reveal pre { box-shadow: none; width: 100%; }
    .reveal pre code { max-height: 420px; font-size: 0.72em; line-height: 1.5; }
    .reveal h2 { color: #a78bfa; font-size: 1.4em; }
    .reveal h3 { color: #818cf8; font-size: 1.05em; }
    .tag { display: inline-block; background: #1e1b4b; color: #a78bfa;
           border: 1px solid #4338ca; border-radius: 4px; padding: 3px 12px;
           font-size: 0.55em; margin: 0 4px; }
    .green { color: #4ade80; }
    .red   { color: #f87171; }
    .muted { color: #9ca3af; font-size: 0.75em; }
    .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1em; text-align: left; }
    table { font-size: 0.68em; }
    td, th { padding: 7px 13px !important; }
    .reveal table th { background: #1e1b4b; }
  </style>
</head>
<body>
<div class="reveal">
  <div class="slides">

    <!-- 1. Capa -->
    <section>
      <h1 style="font-size:1.8em">Test Orchestrator</h1>
      <p style="color:#9ca3af">Monorepo de Automação de Testes em Python</p>
      <div style="margin:24px 0">
        <span class="tag">Python 3.12</span>
        <span class="tag">pytest</span>
        <span class="tag">Selenium</span>
        <span class="tag">requests</span>
        <span class="tag">GitHub Actions</span>
      </div>
      <p><img src="https://github.com/Adryanrr/test-orchestrator/actions/workflows/ci.yml/badge.svg" alt="CI Status"></p>
      <p class="muted">github.com/Adryanrr/test-orchestrator</p>
    </section>

    <!-- 2. O que este projeto testa -->
    <section>
      <h2>O que este projeto testa?</h2>
      <div class="two-col" style="margin-top:1em">
        <div>
          <h3>REST API — Swagger Petstore</h3>
          <ul style="font-size:0.78em;line-height:1.8">
            <li>Recursos: <strong>Pet, Store, User</strong></li>
            <li>CRUD completo por recurso</li>
            <li>Cenários positivos e negativos</li>
            <li>HTTP client: <code>requests</code></li>
          </ul>
        </div>
        <div>
          <h3>Web E2E — SauceDemo</h3>
          <ul style="font-size:0.78em;line-height:1.8">
            <li>Fluxo completo: login → carrinho → checkout</li>
            <li>Login válido e inválido</li>
            <li>Headless Chrome no CI</li>
            <li>Browser: <code>selenium</code></li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 3. Monorepo -->
    <section>
      <h2>Arquitetura — Monorepo</h2>
      <pre><code class="language-text" data-trim>
test-orchestrator/
├── api/
│   ├── services/        ← Service Layer (encapsula HTTP)
│   │   ├── pet_service.py
│   │   ├── store_service.py
│   │   └── user_service.py
│   ├── tests/           ← Asserções de comportamento
│   └── conftest.py      ← Fixtures: api_session, base_url
├── web/
│   ├── pages/           ← Page Object Model
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── tests/           ← Cenários E2E
│   └── conftest.py      ← Fixture: driver + screenshot em falha
└── .github/workflows/ci.yml
      </code></pre>
      <p class="muted">Módulos independentes — pipeline e relatórios compartilhados</p>
    </section>

    <!-- 4. Service Layer -->
    <section>
      <h2>Service Layer Pattern</h2>
      <pre><code class="language-python" data-trim>
class PetService:
    def __init__(self, session: requests.Session, base_url: str) -> None:
        self._session = session
        self._base_url = base_url

    def create(self, payload: dict[str, object]) -> requests.Response:
        return self._session.post(f"{self._base_url}/pet", json=payload)

    def get(self, pet_id: int) -> requests.Response:
        return self._session.get(f"{self._base_url}/pet/{pet_id}")

    def delete(self, pet_id: int) -> requests.Response:
        return self._session.delete(f"{self._base_url}/pet/{pet_id}")
      </code></pre>
      <p class="muted">Trocar <code>requests</code> por <code>httpx</code>? Muda só aqui — testes intactos.</p>
    </section>

    <!-- 5. Page Object Model -->
    <section>
      <h2>Page Object Model</h2>
      <pre><code class="language-python" data-trim>
class LoginPage:
    _username  = (By.ID, "user-name")
    _login_btn = (By.ID, "login-button")
    _error_msg = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_credentials(self, username: str, password: str) -> None:
        self._wait.until(EC.visibility_of_element_located(
            self._username)).send_keys(username)

    def click_login(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._login_btn)).click()
        self._wait.until(EC.url_contains("inventory"))

    def get_error_message(self) -> str:
        return self._wait.until(EC.visibility_of_element_located(
            self._error_msg)).text
      </code></pre>
      <p class="muted">Seletor muda em 1 lugar — nenhum teste quebra.</p>
    </section>

    <!-- 6. Fixtures -->
    <section>
      <h2>Fixtures &amp; Conftest</h2>
      <pre><code class="language-python" data-trim>
# api/conftest.py — sessão HTTP reutilizada em todos os testes
@pytest.fixture(scope="session")
def api_session() -> Generator[requests.Session, None, None]:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()

# web/conftest.py — screenshot automático quando um teste falha
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
      </code></pre>
      <p class="muted">Injeção de dependências — zero boilerplate nos testes.</p>
    </section>

    <!-- 7. Positivos vs Negativos -->
    <section>
      <h2>Testes Positivos vs Negativos</h2>
      <div class="two-col">
        <div>
          <h3 class="green">✅ Positivo</h3>
          <pre><code class="language-python" data-trim>
def test_get_pet_returns_correct_id(
    pet_service, pet_payload
):
    pet_service.create(pet_payload)
    response = pet_service.get(
        pet_payload["id"]
    )
    assert response.status_code == 200
    assert response.json()["id"] == \
        pet_payload["id"]
          </code></pre>
        </div>
        <div>
          <h3 class="red">❌ Negativo</h3>
          <pre><code class="language-python" data-trim>
def test_get_nonexistent_pet_returns_404(
    pet_service
):
    response = pet_service.get(
        9_999_999_999
    )
    assert response.status_code == 404
          </code></pre>
        </div>
      </div>
    </section>

    <!-- 8. Cobertura de negativos -->
    <section>
      <h2>Cobertura de Casos Negativos</h2>
      <table>
        <thead>
          <tr><th>Recurso</th><th>Cenário</th><th>Código esperado</th></tr>
        </thead>
        <tbody>
          <tr><td>Pet API</td><td>GET ID inexistente</td><td class="red">404</td></tr>
          <tr><td>Pet API</td><td>POST payload vazio</td><td class="red">400 / 405</td></tr>
          <tr><td>Store API</td><td>GET order inexistente</td><td class="red">404</td></tr>
          <tr><td>User API</td><td>GET username inexistente</td><td class="red">404</td></tr>
          <tr><td>User API</td><td>Login sem credenciais</td><td class="red">400</td></tr>
          <tr><td>Web E2E</td><td>Login senha errada</td><td class="red">erro no DOM</td></tr>
          <tr><td>Web E2E</td><td>Usuário bloqueado</td><td class="red">erro no DOM</td></tr>
        </tbody>
      </table>
    </section>

    <!-- 9. Pipeline CI/CD -->
    <section>
      <h2>Pipeline CI/CD</h2>
      <pre><code class="language-text" data-trim>
push / pull_request
       │
       ├── api-tests ─────────────────────────────┐
       │   pytest api/tests/ -v                   │
       │                                          ├─► auto-merge → developer
       └── web-tests ─────────────────────────────┘   (feature branches)
           pytest web/tests/ -v

✅ Ambos passam → squash merge automático via gh pr merge
❌ Qualquer falha → branch bloqueada, sem merge
      </code></pre>
      <p class="muted">
        <code>concurrency: ci-${GITHUB_REF}</code> cancela runs duplicados
      </p>
    </section>

    <!-- 10. Branch Strategy -->
    <section>
      <h2>Branch Strategy</h2>
      <pre><code class="language-text" data-trim>
feat/* ou fix/*
      │
      │  push → CI (api-tests + web-tests em paralelo)
      ▼
  ✅ verde → PR automático → squash merge → developer
  ❌ falha → branch bloqueada, sem merge

developer
      │  PR manual + aprovação humana
      ▼
    main
      </code></pre>
      <table style="margin-top:0.5em">
        <tr><th>Branch</th><th>Merge via</th><th>Aprovação humana</th></tr>
        <tr><td><code>feat/*</code></td><td>CI auto-merge (squash)</td><td>Não</td></tr>
        <tr><td><code>developer</code></td><td>PR manual</td><td>Sim</td></tr>
        <tr><td><code>main</code></td><td>PR manual</td><td>Sim (obrigatório)</td></tr>
      </table>
    </section>

    <!-- 11. Commits Semânticos -->
    <section>
      <h2>Commits Semânticos</h2>
      <pre><code class="language-text" data-trim>
feat: estrutura inicial do monorepo Python
fix:  usar JS nativo para inputs React no checkout
ci:   habilitar permissão para criar PRs via Actions
docs: adicionar ARCHITECTURE.md
fix:  remover scrollIntoView de todas as page objects
ci:   unificar workflows para corrigir race condition
test: adicionar casos negativos nos testes de API
      </code></pre>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font-size:0.65em;margin-top:1em;text-align:left">
        <div><code>feat:</code> nova funcionalidade</div>
        <div><code>fix:</code>  correção de bug</div>
        <div><code>ci:</code>   pipeline / workflow</div>
        <div><code>docs:</code> documentação</div>
        <div><code>test:</code> adição de testes</div>
        <div><code>refactor:</code> sem mudança de comportamento</div>
      </div>
    </section>

    <!-- 12. Demo ao vivo -->
    <section>
      <h2>Demo ao Vivo</h2>
      <div style="margin:1.5em auto;max-width:640px;background:#0d0d0d;border:1px solid #333;border-radius:8px;padding:24px;text-align:left;font-family:monospace;font-size:0.75em;line-height:1.8">
        <span style="color:#9ca3af">$ </span>pytest api/tests/ web/tests/ -v<br><br>
        <span class="green">api/tests/test_pet.py::test_create_pet_returns_200 PASSED</span><br>
        <span class="green">api/tests/test_pet.py::test_get_nonexistent_pet_returns_404 PASSED</span><br>
        <span class="green">api/tests/test_user.py::test_login_missing_credentials_returns_400 PASSED</span><br>
        <span class="green">web/tests/test_e2e_purchase.py::test_complete_purchase_flow PASSED</span><br>
        <span class="green">web/tests/test_e2e_purchase.py::test_login_invalid_credentials PASSED</span><br>
        <span class="green">web/tests/test_e2e_purchase.py::test_login_locked_user PASSED</span><br>
        <br>
        <span class="green">═══════════ N passed in X.XXs ═══════════</span>
      </div>
      <p class="muted">Terminal ao lado — execução em tempo real</p>
    </section>

    <!-- 13. Conclusão -->
    <section>
      <h2>Conclusão</h2>
      <div class="two-col" style="margin:1em 0">
        <div>
          <h3>Cobertura de testes</h3>
          <ul style="font-size:0.75em;line-height:1.9">
            <li>Pet API: 5 positivos + 2 negativos</li>
            <li>Store API: 3 positivos + 1 negativo</li>
            <li>User API: 4 positivos + 2 negativos</li>
            <li>Web E2E: 1 positivo + 2 negativos</li>
          </ul>
        </div>
        <div>
          <h3>Padrões aplicados</h3>
          <ul style="font-size:0.75em;line-height:1.9">
            <li>Service Layer (API)</li>
            <li>Page Object Model (Web)</li>
            <li>Fixtures pytest (injeção)</li>
            <li>Commits semânticos</li>
            <li>Gitflow + CI/CD automático</li>
          </ul>
        </div>
      </div>
      <p><a href="https://github.com/Adryanrr/test-orchestrator" style="color:#a78bfa">
        github.com/Adryanrr/test-orchestrator
      </a></p>
    </section>

  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.js"></script>
<script>
  Reveal.initialize({
    hash: true,
    slideNumber: 'c/t',
    transition: 'slide',
    controls: true,
    progress: true,
    plugins: [RevealHighlight]
  });
</script>
</body>
</html>
```

- [ ] **Step 3: Verificar no browser**

```bash
open slides/index.html
```

Verificar: 13 slides navegam com setas, `F` ativa fullscreen, syntax highlight ativo nos blocos Python e text.

- [ ] **Step 4: Commit**

```bash
git add slides/index.html
git commit -m "feat: adicionar slides Reveal.js para apresentação do dia 07/05"
```

---

### Task 4: Site estático — CSS e JS

**Files:**
- Create: `docs/web/style.css`
- Create: `docs/web/app.js`

- [ ] **Step 1: Criar `docs/web/style.css`**

```css
:root {
  --bg: #0d0d0d;
  --surface: #1a1a1a;
  --text: #e8e8e8;
  --accent: #7c6af7;
  --border: #2a2a2a;
  --muted: #888888;
  --sidebar-w: 260px;
}
[data-theme="light"] {
  --bg: #ffffff;
  --surface: #f5f5f5;
  --text: #1a1a1a;
  --border: #e0e0e0;
  --muted: #555555;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, sans-serif;
  display: flex;
  min-height: 100vh;
  transition: background 0.2s, color 0.2s;
}
#sidebar {
  width: var(--sidebar-w);
  min-height: 100vh;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 24px 0;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  flex-shrink: 0;
}
.sidebar-logo {
  padding: 0 20px 20px;
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  border-bottom: 1px solid var(--border);
  margin-bottom: 8px;
}
#sidebar ul { list-style: none; }
#sidebar ul li a {
  display: block;
  padding: 10px 20px;
  color: var(--muted);
  text-decoration: none;
  font-size: 13px;
  border-left: 3px solid transparent;
  transition: all 0.15s;
}
#sidebar ul li a:hover,
#sidebar ul li a.active {
  color: var(--accent);
  background: rgba(124,106,247,0.08);
  border-left-color: var(--accent);
}
main {
  flex: 1;
  max-width: 860px;
  margin: 0 auto;
  padding: 48px 40px;
}
section { margin-bottom: 80px; scroll-margin-top: 24px; }
h1 { font-size: 2rem; margin-bottom: 8px; }
h2 { font-size: 1.5rem; color: var(--accent); margin-bottom: 24px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }
h3 { font-size: 1.05rem; margin-bottom: 12px; margin-top: 24px; }
p  { line-height: 1.7; margin-bottom: 16px; }
a  { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
table { width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 24px; }
th { background: var(--surface); padding: 10px 14px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: .05em; color: var(--muted); border-bottom: 1px solid var(--border); }
td { padding: 10px 14px; border-bottom: 1px solid var(--border); }
pre {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px 20px 20px 20px;
  overflow-x: auto;
  margin-bottom: 24px;
}
code { font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; font-size: 13px; }
:not(pre) > code { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 2px 6px; font-size: 12px; }
.copy-btn {
  position: absolute; top: 10px; right: 10px;
  background: var(--border); border: none; border-radius: 4px;
  padding: 4px 10px; font-size: 11px; color: var(--muted);
  cursor: pointer; transition: background 0.15s;
}
.copy-btn:hover { background: var(--accent); color: white; }
#theme-toggle {
  position: fixed; top: 16px; right: 16px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 8px 14px; cursor: pointer;
  font-size: 14px; z-index: 100; color: var(--text);
}
.hero-meta { color: var(--muted); font-size: 14px; margin-bottom: 20px; }
.badge-row { margin: 16px 0; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
.status-pass { color: #4ade80; font-weight: 600; }
.status-fail { color: #f87171; font-weight: 600; }
.timeline { border-left: 2px solid var(--border); padding-left: 24px; }
.timeline-item { position: relative; margin-bottom: 36px; }
.timeline-item::before {
  content: ''; position: absolute; left: -31px; top: 5px;
  width: 12px; height: 12px; border-radius: 50%;
  background: var(--accent); border: 2px solid var(--bg);
}
.timeline-item .tl-meta { font-size: 12px; color: var(--muted); margin-bottom: 6px; }
iframe.report { width: 100%; height: 580px; border: 1px solid var(--border); border-radius: 8px; background: white; margin-bottom: 24px; }
@media (max-width: 768px) {
  body { flex-direction: column; }
  #sidebar { width: 100%; height: auto; position: relative; min-height: unset; }
  main { padding: 24px 16px; }
  .two-col { grid-template-columns: 1fr; }
}
```

- [ ] **Step 2: Criar `docs/web/app.js`**

```javascript
// --- Tema dark/light ---
const toggle = document.getElementById('theme-toggle');

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  toggle.textContent = theme === 'light' ? '🌙' : '☀️';
  localStorage.setItem('theme', theme);
}

setTheme(localStorage.getItem('theme') || 'dark');
toggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  setTheme(current === 'dark' ? 'light' : 'dark');
});

// --- Scroll-spy sidebar ---
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('#sidebar a');

const spy = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    navLinks.forEach(l => l.classList.remove('active'));
    const link = document.querySelector(`#sidebar a[href="#${entry.target.id}"]`);
    if (link) link.classList.add('active');
  });
}, { rootMargin: '-15% 0px -70% 0px' });

sections.forEach(s => spy.observe(s));

// --- Botões de copiar ---
document.querySelectorAll('pre').forEach(pre => {
  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.textContent = 'Copiar';
  btn.addEventListener('click', () => {
    const text = pre.querySelector('code').textContent;
    navigator.clipboard.writeText(text).then(() => {
      btn.textContent = 'Copiado!';
      setTimeout(() => { btn.textContent = 'Copiar'; }, 2000);
    });
  });
  pre.appendChild(btn);
});
```

- [ ] **Step 3: Commit**

```bash
git add docs/web/style.css docs/web/app.js
git commit -m "feat: adicionar CSS e JS do site estático de documentação"
```

---

### Task 5: Site estático — HTML

**Files:**
- Create: `docs/web/index.html`

- [ ] **Step 1: Criar `docs/web/index.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Test Orchestrator — Documentação</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css">
  <link rel="stylesheet" href="style.css">
</head>
<body>

<button id="theme-toggle">☀️</button>

<nav id="sidebar">
  <div class="sidebar-logo">Test Orchestrator</div>
  <ul>
    <li><a href="#hero">Início</a></li>
    <li><a href="#arquitetura">Arquitetura</a></li>
    <li><a href="#padroes">Padrões de Projeto</a></li>
    <li><a href="#testes">Testes</a></li>
    <li><a href="#erros">Erros &amp; Soluções</a></li>
    <li><a href="#pipeline">Pipeline &amp; Branches</a></li>
    <li><a href="#relatorios">Relatórios</a></li>
  </ul>
</nav>

<main>

  <!-- HERO -->
  <section id="hero">
    <h1>Test Orchestrator</h1>
    <p class="hero-meta">Monorepo de automação de testes em Python — API REST + Web E2E</p>
    <div class="badge-row">
      <img src="https://github.com/Adryanrr/test-orchestrator/actions/workflows/ci.yml/badge.svg" alt="CI">
    </div>
    <div class="two-col" style="margin-top:24px">
      <div class="card">
        <h3>REST API</h3>
        <p style="font-size:14px">Swagger Petstore V2 — endpoints de Pet, Store e User. Padrão Service Layer.</p>
        <code>pytest · requests · pytest-html</code>
      </div>
      <div class="card">
        <h3>Web E2E</h3>
        <p style="font-size:14px">SauceDemo — fluxo completo de compra. Padrão Page Object Model.</p>
        <code>pytest · selenium · Chrome headless</code>
      </div>
    </div>
    <p><a href="https://github.com/Adryanrr/test-orchestrator">github.com/Adryanrr/test-orchestrator</a></p>
  </section>

  <!-- ARQUITETURA -->
  <section id="arquitetura">
    <h2>Arquitetura</h2>
    <pre><code class="language-text">test-orchestrator/
├── api/
│   ├── services/        ← Service Layer — encapsula chamadas HTTP
│   │   ├── pet_service.py
│   │   ├── store_service.py
│   │   └── user_service.py
│   ├── tests/           ← Asserções de comportamento da API
│   │   ├── test_pet.py
│   │   ├── test_store.py
│   │   └── test_user.py
│   └── conftest.py      ← Fixtures: api_session (requests.Session), base_url
├── web/
│   ├── pages/           ← Page Object Model — encapsula interações da UI
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── tests/
│   │   └── test_e2e_purchase.py
│   └── conftest.py      ← Fixture: Chrome headless + screenshot em falha
├── .github/workflows/ci.yml
├── reports/             ← Artefatos: HTML + JUnit XML
└── pyproject.toml</code></pre>

    <h3>Por que Monorepo?</h3>
    <table>
      <tr><th>Decisão</th><th>Justificativa</th></tr>
      <tr><td>Único repositório para API + Web</td><td>Pipeline de CI compartilhada, relatórios centralizados, configuração do pytest unificada</td></tr>
      <tr><td>Módulos independentes (<code>api/</code>, <code>web/</code>)</td><td>Dependências isoladas por <code>requirements.txt</code>, sem interferência entre suítes</td></tr>
      <tr><td>Squash merge em feature branches</td><td>Histórico limpo na <code>developer</code> — commits intermediários consolidados em um único commit semântico</td></tr>
    </table>
  </section>

  <!-- PADRÕES -->
  <section id="padroes">
    <h2>Padrões de Projeto</h2>

    <h3>Service Layer — API</h3>
    <p>Cada recurso da API possui uma classe que encapsula as chamadas HTTP. Os testes consomem essas classes via fixtures do pytest, sem fazer chamadas HTTP diretamente.</p>
    <pre><code class="language-python">class PetService:
    def __init__(self, session: requests.Session, base_url: str) -> None:
        self._session = session
        self._base_url = base_url

    def create(self, payload: dict[str, object]) -> requests.Response:
        return self._session.post(f"{self._base_url}/pet", json=payload)

    def get(self, pet_id: int) -> requests.Response:
        return self._session.get(f"{self._base_url}/pet/{pet_id}")</code></pre>
    <p style="font-size:14px;color:var(--muted)">Benefício: trocar <code>requests</code> por <code>httpx</code> exige mudança apenas na camada de serviços — testes permanecem intactos.</p>

    <h3>Page Object Model — Web</h3>
    <p>Cada página da aplicação SauceDemo é representada por uma classe que encapsula seletores e interações. O teste orquestra os Page Objects sem conhecer detalhes de implementação da UI.</p>
    <pre><code class="language-python">class LoginPage:
    _username  = (By.ID, "user-name")
    _login_btn = (By.ID, "login-button")
    _error_msg = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_credentials(self, username: str, password: str) -> None:
        self._wait.until(EC.visibility_of_element_located(
            self._username)).send_keys(username)

    def click_login(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._login_btn)).click()
        self._wait.until(EC.url_contains("inventory"))

    def get_error_message(self) -> str:
        return self._wait.until(EC.visibility_of_element_located(
            self._error_msg)).text</code></pre>
    <p style="font-size:14px;color:var(--muted)">Benefício: seletor de um elemento muda em exatamente 1 lugar — nenhum teste precisa ser atualizado.</p>
  </section>

  <!-- TESTES -->
  <section id="testes">
    <h2>Testes</h2>

    <h3>Cobertura por recurso</h3>
    <table>
      <tr><th>Módulo</th><th>Recurso</th><th>Positivos</th><th>Negativos</th></tr>
      <tr><td>API</td><td>Pet</td><td>5</td><td>2</td></tr>
      <tr><td>API</td><td>Store</td><td>3</td><td>1</td></tr>
      <tr><td>API</td><td>User</td><td>4</td><td>2</td></tr>
      <tr><td>Web</td><td>E2E Purchase</td><td>1</td><td>2</td></tr>
    </table>

    <h3>Testes negativos — validando erros da aplicação</h3>
    <p>Testes negativos verificam que a aplicação retorna erros corretos diante de entradas inválidas. Eles passam (<span class="status-pass">PASSED</span>) porque o sistema se comporta corretamente.</p>
    <pre><code class="language-python"># API — recurso inexistente
def test_get_nonexistent_pet_returns_404(pet_service: PetService) -> None:
    response = pet_service.get(9_999_999_999)
    assert response.status_code == 404

# API — credenciais ausentes
def test_login_missing_credentials_returns_400(user_service) -> None:
    response = user_service.login("", "")
    assert response.status_code == 400

# Web — usuário bloqueado
def test_login_locked_user(driver):
    login = LoginPage(driver)
    login.open()
    login.fill_credentials("locked_out_user", "secret_sauce")
    login.attempt_login()
    assert "locked out" in login.get_error_message()</code></pre>
  </section>

  <!-- ERROS E SOLUÇÕES -->
  <section id="erros">
    <h2>Erros &amp; Soluções</h2>
    <p>Bugs reais encontrados durante o desenvolvimento e as soluções aplicadas.</p>

    <div class="timeline">

      <div class="timeline-item">
        <div class="tl-meta">Bug #1 — web/pages/checkout_page.py</div>
        <h3>Inputs React ignorados no Chrome headless (Linux/CI)</h3>
        <p style="font-size:14px">O Selenium nativo (<code>send_keys</code>) não dispara os eventos <code>input</code>/<code>change</code> que o React espera em inputs controlados. No headless do Linux o campo ficava vazio.</p>
        <pre><code class="language-python">JS_SET_INPUT = """
var nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value').set;
nativeSetter.call(arguments[0], arguments[1]);
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
"""
driver.execute_script(JS_SET_INPUT, element, value)</code></pre>
      </div>

      <div class="timeline-item">
        <div class="tl-meta">Bug #2 — web/pages/checkout_page.py</div>
        <h3>Botão Finish sem efeito com ActionChains</h3>
        <p style="font-size:14px"><code>ActionChains</code> simulava eventos sintetizados que o React ignorava. Substituído por clique via JavaScript direto no elemento.</p>
        <pre><code class="language-python">driver.execute_script("arguments[0].click();", element)</code></pre>
      </div>

      <div class="timeline-item">
        <div class="tl-meta">Bug #3 — .github/workflows/ci.yml</div>
        <h3>Race condition no auto-merge do CI</h3>
        <p style="font-size:14px">Dois workflows paralelos (<code>api-tests</code> e <code>web-tests</code>) disputavam a criação do PR para <code>developer</code>. Solução: unificar em um pipeline único com <code>concurrency</code> group.</p>
        <pre><code class="language-yaml">concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true</code></pre>
      </div>

      <div class="timeline-item">
        <div class="tl-meta">Bug #4 — web/pages/ (todas as pages)</div>
        <h3>scrollIntoView quebrando interações no checkout</h3>
        <p style="font-size:14px">Chamadas de <code>scrollIntoView</code> antes de interagir com elementos criavam estado inconsistente nos componentes React. Removidas de todas as Page Objects.</p>
      </div>

    </div>
  </section>

  <!-- PIPELINE -->
  <section id="pipeline">
    <h2>Pipeline &amp; Branches</h2>

    <h3>Fluxo CI/CD</h3>
    <pre><code class="language-text">push / pull_request
       │
       ├── api-tests ─────────────────────────────────┐
       │   pytest api/tests/ -v                       │
       │   artefato: api-report.html + api-results.xml│
       │                                              ├─► auto-merge → developer
       └── web-tests ─────────────────────────────────┘   (apenas feature branches)
           pytest web/tests/ -v
           artefato: web-report.html + screenshot em falha

✅ Ambos passam → squash merge automático (gh pr merge --squash)
❌ Qualquer falha → branch bloqueada, sem merge</code></pre>

    <h3>Estratégia de branches</h3>
    <table>
      <tr><th>Branch</th><th>Merge via</th><th>Aprovação humana</th></tr>
      <tr><td><code>feat/*</code>, <code>fix/*</code></td><td>CI auto-merge (squash)</td><td>Não</td></tr>
      <tr><td><code>developer</code></td><td>PR manual</td><td>Sim</td></tr>
      <tr><td><code>main</code></td><td>PR manual</td><td>Sim (obrigatório)</td></tr>
    </table>

    <h3>Commits semânticos</h3>
    <pre><code class="language-text">feat: estrutura inicial do monorepo Python
fix:  usar JS nativo para inputs React no checkout
ci:   habilitar permissão para criar PRs via Actions
docs: adicionar ARCHITECTURE.md
fix:  remover scrollIntoView de todas as page objects
ci:   unificar workflows para corrigir race condition
test: adicionar casos negativos nos testes de API</code></pre>
  </section>

  <!-- RELATÓRIOS -->
  <section id="relatorios">
    <h2>Relatórios</h2>
    <p style="font-size:14px;color:var(--muted)">
      Gere os relatórios localmente antes de abrir esta página:
      <code>pytest api/tests/ --html=../../reports/api-report.html --self-contained-html</code>
    </p>

    <h3>Testes de API</h3>
    <iframe class="report" src="../../reports/api-report.html" title="API Test Report"></iframe>

    <h3>Testes Web E2E</h3>
    <iframe class="report" src="../../reports/web-report.html" title="Web Test Report"></iframe>
  </section>

</main>

<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-core.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
<script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Gerar relatórios para os iframes funcionarem**

```bash
cd /caminho/para/test-orchestrator
pytest api/tests/ --html=reports/api-report.html --self-contained-html
pytest web/tests/ --html=reports/web-report.html --self-contained-html
```

- [ ] **Step 3: Abrir o site no browser e verificar**

```bash
open docs/web/index.html
```

Verificar: sidebar destaca seção ativa ao rolar, toggle dark/light funciona, iframes dos reports carregam, syntax highlight ativo, botões de copiar funcionam.

- [ ] **Step 4: Commit**

```bash
git add docs/web/index.html
git commit -m "feat: adicionar site estático de documentação para apresentação do dia 14/05"
```
