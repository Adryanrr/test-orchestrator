# Design: Test Automation Monorepo

**Data:** 2026-05-02
**Projeto:** test-orchestrator
**Status:** Aprovado

---

## Visão Geral

Monorepo Python com dois módulos de automação de testes independentes:
1. **API** — cobertura completa do Swagger Petstore via `pytest` + `requests`
2. **Web** — fluxo E2E no SauceDemo via `pytest` + `selenium` + `webdriver-manager`

Ambos integrados a pipelines independentes no GitHub Actions.

---

## Estrutura do Repositório

```
test-orchestrator/
├── .github/
│   └── workflows/
│       ├── api-tests.yml
│       └── web-tests.yml
│
├── api/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── store_service.py
│   │   └── pet_service.py
│   ├── tests/
│   │   ├── test_user.py
│   │   ├── test_store.py
│   │   └── test_pet.py
│   ├── conftest.py
│   └── requirements.txt
│
├── web/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── tests/
│   │   └── test_e2e_purchase.py
│   ├── conftest.py
│   └── requirements.txt
│
├── reports/
├── pyproject.toml
└── README.md
```

---

## Stack de Tecnologias

| Módulo | Framework | HTTP/Driver | Relatório |
|--------|-----------|-------------|-----------|
| API | pytest | requests | JUnit XML + pytest-html |
| Web | pytest | selenium + webdriver-manager | JUnit XML + pytest-html |

**Python:** 3.12
**CI:** GitHub Actions (`ubuntu-latest`)

---

## Arquitetura

### API — Service Layer Pattern

Cada `Service` encapsula as chamadas HTTP para um recurso do Petstore. Os testes importam o service e validam status code, schema e comportamento de erro. Nenhum teste chama `requests` diretamente.

```
conftest.py         → fixture base_url = "https://petstore.swagger.io/v2"
UserService         → POST /user, GET /user/{username}, PUT /user/{username}, DELETE /user/{username}
StoreService        → GET /store/inventory, POST /store/order, GET /store/order/{id}, DELETE /store/order/{id}
PetService          → POST /pet, GET /pet/{id}, PUT /pet, GET /pet/findByStatus, DELETE /pet/{id}
```

Cada teste cria o recurso, valida e limpa — sem dependência de ordem entre testes.

### Web — Page Object Model

Cada Page Object representa uma tela do SauceDemo. Encapsula locators e ações. Os testes leem como uma história sequencial.

```
conftest.py         → fixture driver (init + teardown do WebDriver, modo headless)
LoginPage           → fill_credentials(user, password), click_login()
InventoryPage       → add_first_item_to_cart()
CartPage            → proceed_to_checkout()
CheckoutPage        → fill_info(first, last, zip), finish(), get_confirmation_message()
```

O teste E2E chama os Page Objects em sequência e faz assert na mensagem final de confirmação.

---

## CI/CD

### `api-tests.yml`
- Gatilho: `push` e `pull_request` em qualquer branch
- Runner: `ubuntu-latest`
- Passos: checkout → setup Python 3.12 → `pip install` → `pytest` com JUnit XML + HTML → upload artefato

### `web-tests.yml`
- Gatilho: `push` e `pull_request` em qualquer branch
- Runner: `ubuntu-latest` (Chrome pré-instalado)
- Driver: headless via `webdriver-manager`
- Passos: checkout → setup Python 3.12 → `pip install` → `pytest` com JUnit XML + HTML → upload artefato

Os dois jobs aparecem separados no painel do GitHub Actions.

---

## Estratégia de Branches

```
main                    # entrega final
└── developer           # homologação
    ├── feat/infra      # fase 1: estrutura e CI base
    ├── feat/api-tests  # fase 2: automação API
    ├── feat/web-tests  # fase 3: automação Web
    └── feat/docs       # fase 4: README e prints
```

PRs: branch de módulo → `developer`. Entrega: `developer` → `main`.

---

## Padrão de Commits

Tipos: `feat`, `fix`, `docs`, `chore`, `test`

Exemplos:
```
feat: inicializar estrutura do monorepo
feat: implementar UserService com endpoints CRUD
feat: adicionar testes do endpoint /user
feat: implementar Page Object LoginPage
feat: adicionar fluxo E2E de compra no SauceDemo
feat: configurar GitHub Actions para api-tests
feat: configurar GitHub Actions para web-tests
docs: adicionar README com instruções e prints
fix: corrigir seletor do botão de checkout
```

---

## Padrões de Qualidade de Código

- **Zero comentários** no código — nomes revelam intenção
- **Funções pequenas** — cada método faz uma única coisa
- **Sem valores hardcoded** — URLs e credenciais em fixtures/variáveis
- **Nomes descritivos** — `test_create_user_returns_201`, não `test_user_1`
- **Independência entre testes** — cada teste cria, valida e limpa seu próprio estado

---

## Cobertura de Requisitos

| Requisito | Coberto por |
|-----------|-------------|
| ARCH-01 | Estrutura de monorepo com `api/` e `web/` + `pyproject.toml` |
| ARCH-02 | Commits semânticos por convenção + exemplos documentados |
| ARCH-03 | README.md unificado na raiz |
| API-01 | `UserService` + `test_user.py` |
| API-02 | `StoreService` + `test_store.py` |
| API-03 | `PetService` + `test_pet.py` |
| WEB-01 | Page Objects em `web/pages/` |
| WEB-02 | `test_e2e_purchase.py` com fluxo login → carrinho → checkout |
| CI-01 | `api-tests.yml` |
| CI-02 | `web-tests.yml` |
