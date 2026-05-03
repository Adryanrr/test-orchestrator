## 🌿 Padrão de commit Semânticas

## 📌 Tipos mais usados

* **feat** → nova funcionalidade
* **fix** → correção de bug
* **refactor** → mudança interna sem alterar comportamento
* **test** → criação/alteração de testes
* **docs** → documentação
* **chore** → tarefas gerais (config, build, etc)

---

## 🧪 Exemplos práticos

```bash
feat: adiciona fluxo de checkout E2E
fix: corrige erro no login
test: adiciona testes para criação de usuário
refactor: reorganiza estrutura dos testes
docs: atualiza README com instruções
chore: adiciona pipeline de CI
```

---

## 🎯 Por que isso importa

* Facilita entender o histórico do projeto
* Ajuda na organização e revisão de código
* Permite gerar changelogs automaticamente
* Mostra maturidade profissional (isso pesa na avaliação)

## 🌿 Padrão de Branches Semânticas

Assim como os commits, as branches também devem seguir um padrão claro para indicar **o tipo de trabalho que está sendo realizado**.

### 🧠 Estrutura básica

```bash
tipo/nome-da-branch
```

Opcional (mais organizado):

```bash
tipo/escopo-descricao
```

---

## 📌 Tipos mais usados (mesmos dos commits)

* **feat/** → nova funcionalidade
* **fix/** → correção de bug
* **refactor/** → refatoração de código
* **test/** → criação ou alteração de testes
* **docs/** → documentação
* **chore/** → tarefas gerais (configuração, CI, etc)

---

## 🧪 Exemplos práticos

```bash
feat/checkout-e2e
feat/api-user-crud

fix/login-error
fix/pipeline-failure

test/api-pet-endpoints
test/web-checkout-flow

refactor/project-structure
refactor/page-objects

docs/readme-update
docs/api-documentation

chore/add-ci-pipeline
chore/update-dependencies
```

---

## 🎯 Boas práticas

* Use **kebab-case** (palavras separadas por `-`)
* Seja **curto e descritivo**
* Evite nomes genéricos como:

  ```bash
  ajuste
  teste
  coisa-nova
  ```

---

## 🔗 Relação entre Branch e Commit

O ideal é manter consistência:

```bash
branch: feat/checkout-e2e
commit: feat: adiciona fluxo de checkout E2E
```

👉 Isso deixa o histórico extremamente claro e profissional.

---

## 🚀 Fluxo recomendado

1. Criar branch:

```bash
git checkout -b feat/api-user-crud
```

2. Fazer commits semânticos:

```bash
feat: adiciona endpoint de criação de usuário
```

3. Abrir Pull Request para `develop`
