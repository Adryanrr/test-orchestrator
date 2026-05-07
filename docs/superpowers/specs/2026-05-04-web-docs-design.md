# Design: Documentação Web Interativa

**Data:** 2026-05-04  
**Status:** Aprovado  
**Contexto:** Projeto acadêmico com apresentações em 07/05 e 14/05/2026

---

## Objetivo

Criar uma página web que sirva como documentação viva do projeto `test-orchestrator`, permitindo que qualquer pessoa que clone o repositório entenda o que o projeto faz, como funciona, as decisões arquiteturais tomadas e os erros encontrados — e que possa executar os testes ao vivo pelo próprio navegador.

---

## Estrutura de Arquivos

```
docs/
└── web/
    ├── main.py          # FastAPI app + rotas HTTP e WebSocket
    ├── requirements.txt # fastapi, uvicorn
    ├── static/
    │   ├── style.css    # tema dark/light via CSS Variables + layout
    │   └── app.js       # WebSocket client, syntax highlight init, dark/light toggle
    └── index.html       # single-page com todo o conteúdo
```

---

## Seções da Página

| # | Seção | Conteúdo |
|---|-------|----------|
| 1 | **Hero** | Nome do projeto, badge do CI (GitHub Actions), link para o repositório |
| 2 | **Visão Geral** | O que o projeto faz, quais sistemas testa (Swagger Petstore + SauceDemo) |
| 3 | **Arquitetura** | Diagrama ASCII da estrutura do monorepo, explicação do Service Layer e POM com trechos de código |
| 4 | **Padrões de Projeto** | Service Layer vs Page Object Model lado a lado, benefícios de cada padrão |
| 5 | **Erros & Soluções** | Timeline dos bugs reais encontrados durante o desenvolvimento, com o workaround em código |
| 6 | **Workflow** | Diagrama do fluxo CI/CD e estratégia de branches (feat → developer → main) |
| 7 | **Executar Testes** | Terminal ao vivo com streaming do pytest via WebSocket, badge de resultado final |

---

## Arquitetura Backend

### Tecnologias
- **FastAPI** — framework web Python moderno
- **uvicorn** — servidor ASGI para FastAPI
- **asyncio.subprocess** — execução assíncrona do pytest com leitura linha a linha

### Rotas

| Rota | Tipo | Função |
|------|------|--------|
| `GET /` | HTTP | Serve o `index.html` |
| `GET /static/*` | HTTP | Serve arquivos estáticos (CSS, JS) |
| `WS /ws/run-tests` | WebSocket | Executa pytest e transmite output em tempo real |

### Fluxo de Execução dos Testes

1. Usuário clica em "Rodar todos os testes"
2. Frontend abre conexão WebSocket com `/ws/run-tests`
3. Backend executa `pytest api/tests/ web/tests/ -v` via `asyncio.create_subprocess_exec`
4. Cada linha do stdout é lida de forma assíncrona e enviada ao cliente via WebSocket
5. Ao finalizar, o backend envia uma mensagem JSON prefixada com `__RESULT__:` contendo status (`passed`/`failed`) e contagens — o frontend detecta esse prefixo para distinguir do output de texto normal
6. Frontend fecha a conexão e exibe badge colorido com o resultado

**Comando executado:**
```bash
pytest api/tests/ web/tests/ -v --tb=short
```
com `PYTHONPATH` apontando para a raiz do repositório.

**Como rodar:**
```bash
cd docs/web
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# Acesse: http://localhost:8000
```

---

## Arquitetura Frontend

### Layout
- Sidebar fixa (260px) à esquerda com links de âncora para cada seção
- Seção ativa destacada ao rolar via `IntersectionObserver`
- Conteúdo principal com `max-width: 860px`, centralizado
- Responsivo: sidebar vira menu hamburguer em telas menores que 768px

### Tema Dark/Light
- CSS Custom Properties para todas as cores
- Toggle no canto superior direito, estado persistido em `localStorage`

| Variável | Dark | Light |
|----------|------|-------|
| `--bg` | `#0d0d0d` | `#ffffff` |
| `--surface` | `#1a1a1a` | `#f5f5f5` |
| `--text` | `#e8e8e8` | `#1a1a1a` |
| `--accent` | `#7c6af7` | `#5b4de0` |
| `--border` | `#2a2a2a` | `#e0e0e0` |

### Syntax Highlight
- **Prism.js** via CDN — suporte nativo a Python, sem build step
- Blocos de código com botão "Copiar" em cada snippet

### Terminal ao Vivo
- Container com fundo `#0d0d0d`, fonte monospace, scroll automático
- Colorização por tipo de linha:
  - `PASSED` → verde (`#4ade80`)
  - `FAILED` → vermelho (`#f87171`)
  - `ERROR` → laranja (`#fb923c`)
  - Demais → cinza claro
- Badge final: `✅ N passed` ou `❌ N failed / N errors`

### JavaScript
- Vanilla JS (~150 linhas), sem framework, sem build step
- Responsabilidades: WebSocket client, toggle de tema, scroll spy da sidebar, inicialização do Prism.js

---

## Conteúdo: Erros & Soluções

Seção documental dos bugs reais encontrados. Cada item tem:
- Título do problema
- Contexto (onde e quando ocorreu)
- Causa raiz
- Solução implementada com trecho de código

**Bugs a documentar:**
1. **Inputs React ignorados no headless Chrome (Linux/CI)** — Selenium nativo não dispara eventos `input`/`change` do React; solução via `nativeInputValueSetter` + `dispatchEvent`
2. **Botão Finish sem efeito com ActionChains** — ActionChains simulava eventos sintetizados que o React ignorava; substituído por `driver.execute_script("arguments[0].click()", element)`
3. **Race condition no auto-merge do CI** — dois workflows paralelos disputavam a criação do PR; solução foi unificar em um pipeline único com `concurrency` group
4. **scrollIntoView quebrando interações no checkout** — chamadas de scroll criavam estado inconsistente nos elementos React; removidas de todas as Page Objects

---

## Restrições

- Roda apenas localmente (não é hospedado no GitHub Pages)
- Requer Python 3.12+, Chrome instalado (para testes Web)
- Não executa testes no GitHub Actions — é uma ferramenta local de demonstração
- Dependências novas isoladas em `docs/web/requirements.txt`, sem afetar `api/` e `web/`

---

## Critérios de Sucesso

- [ ] Página carrega em menos de 2 segundos localmente
- [ ] Toggle dark/light funciona e persiste entre sessões
- [ ] Output dos testes aparece linha a linha em tempo real no terminal
- [ ] Badge final mostra resultado correto (passed/failed)
- [ ] Syntax highlight ativo em todos os blocos de código
- [ ] Sidebar destaca a seção atual ao rolar
- [ ] Responsivo em telas de 375px até 1440px
