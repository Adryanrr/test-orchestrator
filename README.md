# Test Automation Monorepo

Monorepo de automação de testes em Python cobrindo testes de API REST e testes Web E2E, com pipeline de integração contínua via GitHub Actions.

| Pipeline | Status |
|---|---|
| CI Pipeline | ![CI](https://github.com/Adryanrr/test-orchestrator/actions/workflows/ci.yml/badge.svg) |

---

## Sumário

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Execução dos Testes](#execução-dos-testes)
- [Relatórios](#relatórios)
- [Arquitetura de Testes](#arquitetura-de-testes)
- [Pipeline CI/CD](#pipeline-cicd)
- [Fluxo de Branches](#fluxo-de-branches)

---

## Visão Geral

| Módulo | Alvo | Tipo |
|---|---|---|
| **API** | [Swagger Petstore](https://petstore.swagger.io) | REST API — endpoints de Pet, Store e User |
| **Web** | [SauceDemo](https://www.saucedemo.com) | E2E — fluxo completo de compra |

---

## Tecnologias

| Camada | Ferramentas |
|---|---|
| Linguagem | Python 3.12 |
| Testes API | `pytest`, `requests`, `pytest-html` |
| Testes Web | `pytest`, `selenium`, `pytest-html` |
| CI/CD | GitHub Actions |
| Relatórios | JUnit XML + HTML (`pytest-html`) |

---

## Estrutura do Projeto

```
test-orchestrator/
├── api/
│   ├── services/
│   │   ├── pet_service.py
│   │   ├── store_service.py
│   │   └── user_service.py
│   ├── tests/
│   │   ├── test_pet.py
│   │   ├── test_store.py
│   │   └── test_user.py
│   ├── conftest.py
│   └── requirements.txt
├── web/
│   ├── pages/
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── tests/
│   │   └── test_e2e_purchase.py
│   ├── conftest.py
│   └── requirements.txt
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── ARCHITECTURE.md
├── reports/
└── pyproject.toml
```

---

## Pré-requisitos

- Python 3.12+
- Google Chrome instalado (para testes Web locais)
- Git

---

## Instalação

```bash
git clone https://github.com/Adryanrr/test-orchestrator.git
cd test-orchestrator

python -m venv .venv
source .venv/bin/activate

pip install -r api/requirements.txt
pip install -r web/requirements.txt
```

---

## Execução dos Testes

### Testes de API

```bash
pytest api/tests/ -v
```

### Testes Web E2E — modo headless (padrão / CI)

```bash
pytest web/tests/ -v
```

O Chrome roda sem janela visível. É o mesmo modo usado no GitHub Actions.

### Testes Web E2E — modo visual (demo / desenvolvimento)

```bash
HEADLESS=false pytest web/tests/ -v
```

Abre o Chrome com interface gráfica. Útil para depurar ou demonstrar ao vivo.

### Testes Web E2E — modo demo com câmera lenta

```bash
HEADLESS=false DEMO_DELAY=2 pytest web/tests/test_e2e_purchase.py::test_complete_purchase_flow -v
```

Pausa `N` segundos entre cada etapa (login → inventário → carrinho → checkout → confirmação).  
Ajuste `DEMO_DELAY` conforme necessário: `1` rápido, `2` confortável, `3` lento.

### Todos os testes com cobertura de código

```bash
pytest api/tests/ --cov=api --cov-report=term-missing
```

### Com relatório HTML

```bash
pytest api/tests/ --html=reports/api-report.html --self-contained-html
pytest web/tests/ --html=reports/web-report.html --self-contained-html
```

---

## Relatórios

Após cada execução na pipeline, os relatórios ficam disponíveis como artefatos na aba **Actions** do GitHub:

| Artefato | Conteúdo |
|---|---|
| `api-report` | Relatório HTML + JUnit XML dos testes de API |
| `web-report` | Relatório HTML + JUnit XML dos testes Web + screenshot em caso de falha |

---

## Arquitetura de Testes

### API — Service Layer Pattern

Os testes de API seguem o padrão **Service Layer**: cada recurso da API (`Pet`, `Store`, `User`) possui uma classe de serviço que encapsula as chamadas HTTP, mantendo os testes limpos e focados em asserções.

```
conftest.py          → fixtures: base_url, api_session (requests.Session)
api/services/        → encapsulamento das chamadas HTTP por recurso
api/tests/           → asserções de comportamento da API
```

### Web — Page Object Model (POM)

Os testes Web seguem o padrão **Page Object Model**: cada página da aplicação possui uma classe que encapsula os seletores e interações, isolando a lógica de automação da lógica de teste.

```
conftest.py          → fixture: driver (Chrome headless)
web/pages/           → Page Objects: LoginPage, InventoryPage, CartPage, CheckoutPage
web/tests/           → cenário de teste E2E orquestrando os Page Objects
```

---

## Pipeline CI/CD

A pipeline é definida em `.github/workflows/ci.yml` e executa em todo `push` e `pull_request`.

```
push / pull_request
       │
       ├── api-tests ────────────────────────────────┐
       │   └── pytest api/tests/                     │
       │                                             ├── auto-merge-to-developer
       └── web-tests ────────────────────────────────┘   (somente em push de feature branch)
           └── pytest web/tests/
```

**Jobs:**

| Job | Trigger | Condição |
|---|---|---|
| `api-tests` | Todo push/PR | Sempre |
| `web-tests` | Todo push/PR | Sempre |
| `auto-merge-to-developer` | Push em feature branch | Ambos os testes passaram |

---

## Fluxo de Branches

```
feat/* ou fix/*
      │
      │  push → CI roda (api-tests + web-tests)
      │
      ▼
  ✅ Testes passam → PR automático criado → squash merge para developer
  ❌ Testes falham → branch bloqueada, sem merge

developer
      │
      │  PR manual com aprovação humana obrigatória
      ▼
    main
```

| Branch | Proteção |
|---|---|
| `feat/*`, `fix/*` | CI obrigatório (auto-merge se verde) |
| `developer` | CI obrigatório (merge via auto-merge do CI) |
| `main` | CI obrigatório + aprovação humana |
