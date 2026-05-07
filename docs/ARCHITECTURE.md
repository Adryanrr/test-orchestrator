# Arquitetura do Test Orchestrator

## Visão Geral

O projeto é um monorepo de automação de testes dividido em dois módulos independentes: **API** e **Web**. Ambos compartilham o mesmo repositório, pipeline de CI e estrutura de relatórios.

---

## Diagrama de Arquitetura

```
test-orchestrator/
│
├── api/                         Módulo: Testes de API REST
│   ├── services/                Service Layer — encapsula chamadas HTTP
│   │   ├── PetService           POST /pet, GET /pet/{id}, PUT /pet, DELETE /pet/{id}
│   │   ├── StoreService         GET /store/inventory, POST /store/order, DELETE /store/order/{id}
│   │   └── UserService          POST /user, GET /user/{username}, PUT /user, DELETE /user
│   ├── tests/                   Casos de teste — asserções de comportamento
│   │   ├── test_pet.py          CRUD completo de Pet
│   │   ├── test_store.py        Inventário e pedidos
│   │   └── test_user.py        CRUD completo de User
│   └── conftest.py              Fixtures: base_url, api_session
│
├── web/                         Módulo: Testes E2E Web
│   ├── pages/                   Page Object Model — encapsula UI
│   │   ├── LoginPage            Navegação e preenchimento de credenciais
│   │   ├── InventoryPage        Adição de item ao carrinho
│   │   ├── CartPage             Revisão de itens e início do checkout
│   │   └── CheckoutPage         Preenchimento de dados, confirmação e finalização
│   ├── tests/
│   │   └── test_e2e_purchase.py Cenário E2E: login → carrinho → checkout → confirmação
│   └── conftest.py              Fixture: Chrome headless driver + screenshot em falha
│
├── .github/workflows/ci.yml     Pipeline CI/CD
├── reports/                     Artefatos de execução (HTML + JUnit XML)
└── pyproject.toml               Configuração do pytest
```

---

## Padrões de Projeto

### API — Service Layer

Cada recurso da API Petstore possui uma classe de serviço responsável por encapsular os endpoints HTTP. Os testes consomem essas classes via fixtures do pytest, não fazendo chamadas HTTP diretamente.

**Fluxo:**
```
test_create_pet
    │
    ├── fixture: pet_service → PetService(session, base_url)
    ├── fixture: pet_payload → dict com dados aleatórios
    │
    └── pet_service.create(payload) → requests.Response
            │
            └── POST https://petstore.swagger.io/v2/pet
```

**Benefício:** trocar a implementação HTTP (ex: de `requests` para `httpx`) exige mudança apenas na camada de serviços, sem tocar nos testes.

---

### Web — Page Object Model (POM)

Cada página da aplicação SauceDemo é representada por uma classe que encapsula seletores CSS/ID e as interações com o DOM. O teste orquestra os Page Objects em sequência, sem conhecer detalhes de implementação da UI.

**Fluxo:**
```
test_complete_purchase_flow
    │
    ├── LoginPage.open()               → driver.get(URL)
    ├── LoginPage.fill_credentials()   → send_keys nos campos
    ├── LoginPage.click_login()        → click + wait URL /inventory
    │
    ├── InventoryPage.add_first_item() → click no primeiro botão Add to Cart
    ├── InventoryPage.go_to_cart()     → JS click no ícone do carrinho
    │
    ├── CartPage.proceed_to_checkout() → JS click em Checkout + wait URL
    │
    ├── CheckoutPage.fill_info()       → JS nativeInputValueSetter + eventos React
    ├── CheckoutPage.finish()          → JS click em Finish + wait URL
    │
    └── assert confirmation_message == "Thank you for your order!"
```

**Por que JavaScript para inputs no Checkout?**
O SauceDemo usa React com inputs controlados. No Chrome headless do Linux (GitHub Actions), o Selenium nativo não dispara os eventos `input`/`change` que o React espera. A solução é usar o `nativeInputValueSetter` do prototype do `HTMLInputElement` e despachar os eventos manualmente:

```python
JS_SET_INPUT = """
var nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value').set;
nativeSetter.call(arguments[0], arguments[1]);
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
"""
```

---

## Pipeline CI/CD

```
push/pull_request em qualquer branch
           │
     ┌─────┴─────┐
     │           │
 api-tests   web-tests
     │           │
     └─────┬─────┘
           │ (ambos success)
           │ (somente push em feature branch)
           ▼
  auto-merge-to-developer
     │
     ├── gh pr create (se PR não existe)
     └── gh pr merge --squash --admin
```

### Estratégia de merge: Squash

Branches de feature acumulam commits intermediários durante o desenvolvimento. O squash merge consolida todos em um único commit semântico no histórico da `developer`, mantendo o log limpo e legível.

---

## Fluxo de Branches

```
feat/minha-feature  ──push──►  CI (api + web)  ──✅──►  auto PR + squash merge
                                                              │
                                                         developer
                                                              │
                                                      PR manual + aprovação
                                                              │
                                                            main
```

| Branch | Merge via | Aprovação humana |
|---|---|---|
| `feat/*`, `fix/*` | CI auto-merge | Não |
| `developer` | PR manual | Sim |
| `main` | PR manual | Sim (obrigatório) |

---

## Tecnologias e Dependências

| Dependência | Versão | Uso |
|---|---|---|
| `pytest` | ≥8.0 | Runner de testes |
| `requests` | ≥2.31 | Chamadas HTTP (API) |
| `selenium` | ≥4.18 | Automação Web |
| `pytest-html` | ≥4.0 | Relatórios HTML |
| `browser-actions/setup-chrome` | v1 | Chrome no GitHub Actions |

---

## API Testada: Swagger Petstore

Base URL: `https://petstore.swagger.io/v2`

| Recurso | Operações testadas |
|---|---|
| `/pet` | Create, Read, Update, Delete, FindByStatus |
| `/store/inventory` | Read |
| `/store/order` | Create, Read, Delete |
| `/user` | Create, Read, Update, Delete |

Documentação completa: https://petstore.swagger.io

---

## Aplicação Testada: SauceDemo

URL: `https://www.saucedemo.com`

Credenciais utilizadas nos testes: `standard_user` / `secret_sauce`

**Cenário E2E coberto:**

1. Login com credenciais válidas
2. Adição do primeiro produto ao carrinho
3. Navegação ao carrinho e início do checkout
4. Preenchimento de dados pessoais (nome, sobrenome, CEP)
5. Revisão do pedido e finalização
6. Verificação da mensagem de confirmação: `"Thank you for your order!"`
