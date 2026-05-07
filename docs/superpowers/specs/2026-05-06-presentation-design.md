# Design: Apresentação Acadêmica — Slides + Site Estático

**Data:** 2026-05-06
**Status:** Aprovado
**Contexto:** Trabalho acadêmico — apresentações em 07/05 e 14/05/2026

---

## Objetivo

Criar dois artefatos de apresentação para o projeto `test-orchestrator`, demonstrando domínio em QA e arquitetura de software em nível sênior:

1. **Slides Reveal.js** — apresentação na sala (07/05), narrativa linear, projetada no browser
2. **Site Estático** — documentação permanente no repositório (14/05), navegação livre

---

## Prioridade de Entrega

| Artefato | Data | Propósito |
|---|---|---|
| `slides/index.html` | 07/05 | Apresentação em sala, projetado no browser |
| `docs/web/index.html` | 14/05 | Documentação navegável do repositório |

---

## Artefato 1 — Slides Reveal.js

### Tecnologia

- **Reveal.js** via CDN — zero dependências locais, funciona offline
- Tema dark customizado via CSS override
- Syntax highlight: **highlight.js** (já incluído no Reveal.js)
- Arquivo único: `slides/index.html`

### Estrutura dos Slides (13 slides)

| # | Título | Conteúdo |
|---|--------|----------|
| 1 | Capa | Nome do projeto, stack (Python · Selenium · pytest · GitHub Actions), badge CI |
| 2 | Problema & Objetivo | Por que automação? O que o projeto cobre (Petstore REST + SauceDemo E2E) |
| 3 | Arquitetura — Monorepo | Diagrama ASCII da estrutura. Trade-offs de coesão vs acoplamento |
| 4 | Service Layer Pattern | Código real: `PetService` encapsulando HTTP. Benefício: troca de lib sem tocar nos testes |
| 5 | Page Object Model | Código real: `LoginPage`, `CheckoutPage`. Benefício: seletor muda em 1 lugar |
| 6 | Fixtures & Conftest | Como pytest injeta dependências. Driver, session, screenshot em falha |
| 7 | Testes Positivos vs Negativos | Lado a lado: `test_create_pet` (positivo) vs `test_create_pet_invalid` (negativo) |
| 8 | Casos Negativos em Detalhe | Login inválido (401), pet inexistente (404), order inválido (400/405), user duplicado |
| 9 | Pipeline CI/CD | Fluxo: push → api-tests ∥ web-tests → auto-merge. O que acontece quando falha |
| 10 | Branch Strategy | feat/* → developer (auto) → main (aprovação humana). Por que squash merge |
| 11 | Commits Semânticos | Exemplos reais do `git log`. Tipos: feat, fix, ci, docs |
| 12 | Demo ao Vivo | Slide de contexto — testes rodam no terminal ao lado |
| 13 | Conclusão & Links | Métricas finais (total de testes API + Web, recursos cobertos), link do repo |

### Navegação

- Setas do teclado para avançar/voltar
- `F` para fullscreen na apresentação
- `S` para modo speaker notes (uso opcional)
- `O` para visão geral dos slides

---

## Artefato 2 — Site Estático

### Tecnologia

- HTML/CSS/JS vanilla — zero framework, zero build step
- Abre com `open docs/web/index.html` no terminal
- Syntax highlight: **Prism.js** via CDN (suporte nativo a Python)
- Arquivo único principal: `docs/web/index.html` + `style.css` + `app.js`

### Estrutura de Arquivos

```
docs/
└── web/
    ├── index.html    ← página principal (todas as seções)
    ├── style.css     ← tema dark/light via CSS custom properties
    └── app.js        ← sidebar scroll-spy, toggle dark/light, copy buttons

slides/
└── index.html        ← Reveal.js slides
```

### Seções da Página (7 seções)

| # | Seção | Conteúdo |
|---|-------|----------|
| 1 | Hero | Nome, badge CI ao vivo, link do repositório |
| 2 | Arquitetura | Diagrama ASCII do monorepo + explicação das decisões de design |
| 3 | Padrões de Projeto | Service Layer e POM lado a lado com snippets reais (Prism.js) |
| 4 | Testes — Positivos & Negativos | Tabela de cobertura + código dos casos negativos (401, 404, 400) |
| 5 | Erros & Soluções | Timeline dos 4 bugs reais encontrados durante o desenvolvimento |
| 6 | Pipeline & Branches | Fluxo CI/CD + estratégia de branches + commits semânticos |
| 7 | Relatórios | iframes embutindo `reports/api-report.html` e `reports/web-report.html` (ver nota abaixo) |

### Features do Site

- **Sidebar fixa** (260px) com links de âncora, scroll-spy via `IntersectionObserver`
- **Toggle dark/light** no canto superior direito, estado persistido em `localStorage`
- **Syntax highlight** Python via Prism.js — botão "Copiar" em cada bloco
- **iframes dos reports** pytest-html — resultados reais sem backend
- **Responsivo** — sidebar vira menu hamburguer abaixo de 768px

> **Nota sobre os reports:** `reports/*` está no `.gitignore`. Para os iframes funcionarem, é necessário gerar os reports antes de abrir o site:
> ```bash
> pytest api/tests/ --html=reports/api-report.html --self-contained-html
> pytest web/tests/ --html=reports/web-report.html --self-contained-html
> ```
> Como alternativa para o dia 14/05, o `.gitignore` pode ser ajustado para commitar os reports gerados, garantindo que o site funcione sem rodar pytest.

### Diferenças em relação à spec anterior (2026-05-04)

A spec anterior planejava FastAPI + WebSocket para execução ao vivo dos testes. Esta spec substitui por:

| Removido | Substituído por |
|---|---|
| FastAPI + uvicorn | Zero backend |
| WebSocket + terminal ao vivo | iframes dos reports pytest-html |
| `docs/web/main.py` | Nada — site é puramente estático |

A demonstração ao vivo dos testes ocorre na apresentação (slide 12 + terminal), não no site.

---

## Testes Negativos — O que Escrever

Os testes negativos validam que a aplicação retorna os erros corretos. São testes que passam (`PASSED`) porque o sistema se comporta corretamente ao receber entrada inválida.

### API — Casos a implementar

| Arquivo | Teste | Cenário | Asserção |
|---|---|---|---|
| `api/tests/test_pet.py` | `test_get_nonexistent_pet` | GET /pet/{id} com ID inexistente | `status_code == 404` |
| `api/tests/test_pet.py` | `test_create_pet_invalid_payload` | POST /pet com body vazio | `status_code in (400, 405, 500)` |
| `api/tests/test_store.py` | `test_get_nonexistent_order` | GET /store/order/{id} inválido | `status_code == 404` |
| `api/tests/test_user.py` | `test_get_nonexistent_user` | GET /user/{username} inexistente | `status_code == 404` |
| `api/tests/test_user.py` | `test_login_invalid_credentials` | GET /user/login com credenciais erradas | `status_code == 400` |

### Web — Casos a implementar

| Arquivo | Teste | Cenário | Asserção |
|---|---|---|---|
| `web/tests/test_e2e_purchase.py` | `test_login_invalid_credentials` | Login com senha errada | Mensagem de erro visível no DOM |
| `web/tests/test_e2e_purchase.py` | `test_login_locked_user` | Login com `locked_out_user` | Mensagem de bloqueio visível |

---

## Critérios de Sucesso

### Slides
- [ ] 13 slides navegam corretamente com setas do teclado
- [ ] Fullscreen funciona com `F`
- [ ] Blocos de código têm syntax highlight Python
- [ ] Funciona offline (sem internet)
- [ ] Demo ao vivo: pytest roda no terminal ao lado do slide 12

### Site Estático
- [ ] Abre com `open docs/web/index.html` sem servidor
- [ ] Toggle dark/light funciona e persiste entre sessões
- [ ] Sidebar destaca a seção ativa ao rolar
- [ ] Syntax highlight ativo em todos os blocos Python
- [ ] iframes dos reports pytest-html carregam corretamente
- [ ] Responsivo em 375px → 1440px
- [ ] Botão "Copiar" funciona em cada bloco de código

### Testes Negativos
- [ ] 5 casos negativos de API escritos e passando no CI
- [ ] 2 casos negativos de Web escritos e passando no CI
