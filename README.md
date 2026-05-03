# Test Automation Monorepo

Monorepo com automação de testes de API e Web E2E em Python.

| Pipeline | Status |
|----------|--------|
| API Tests | ![API Tests](https://github.com/Adryanrr/test-orchestrator/actions/workflows/api-tests.yml/badge.svg) |
| Web Tests | ![Web Tests](https://github.com/Adryanrr/test-orchestrator/actions/workflows/web-tests.yml/badge.svg) |

## Tecnologias

| Módulo | Ferramentas |
|--------|-------------|
| API    | Python 3.12, pytest, requests, pytest-html |
| Web    | Python 3.12, pytest, selenium, pytest-html |
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
