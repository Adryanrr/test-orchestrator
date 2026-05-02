# Roadmap

**4 fases** | **10 requisitos mapeados** | Todos os requisitos v1 cobertos ✓

| # | Fase | Objetivo | Requisitos | Critérios de Sucesso |
|---|-------|------|--------------|------------------|
| 1 | Configuração de Infraestrutura | Inicializar monorepo, padrões e base do CI | ARCH-01, ARCH-02, ARCH-03 | 3 |
| 2 | Automação de API | Cobrir todos os endpoints do Swagger Petstore | API-01, API-02, API-03 | 3 |
| 3 | Automação Web | Concluir o fluxo E2E do SauceDemo usando Selenium | WEB-01, WEB-02 | 2 |
| 4 | Finalização & CI | Garantir que a pipeline rode todos os testes e a documentação esteja pronta | CI-01, CI-02 | 2 |

### Detalhes das Fases

**Fase 1: Configuração de Infraestrutura**
Objetivo: Inicializar monorepo, padrões e base do CI
Requisitos: ARCH-01, ARCH-02, ARCH-03
Critérios de Sucesso:
1. O repositório tem a estrutura de diretórios correta para API e Web.
2. O arquivo YAML inicial do GitHub Actions está presente.
3. O modelo de ramificação do git (main, developer, branches de módulo) foi estabelecido localmente.

**Fase 2: Automação de API**
Objetivo: Cobrir todos os endpoints do Swagger Petstore
Requisitos: API-01, API-02, API-03
Critérios de Sucesso:
1. Os testes do endpoint 'User' passam com sucesso.
2. Os testes do endpoint 'Store' passam com sucesso.
3. Os testes do endpoint 'Pet' passam com sucesso.

**Fase 3: Automação Web**
Objetivo: Concluir o fluxo E2E do SauceDemo usando Selenium
Requisitos: WEB-01, WEB-02
Critérios de Sucesso:
1. Os Page Objects estão claramente separados da lógica de testes.
2. O teste E2E roda com sucesso do login ao checkout.

**Fase 4: Finalização & CI**
Objetivo: Garantir que a pipeline rode todos os testes e a documentação esteja pronta
Requisitos: CI-01, CI-02
Critérios de Sucesso:
1. A pipeline do GitHub Actions executa tanto os testes de API quanto os testes Web automaticamente.
2. O README.md contém as instruções de execução, tecnologias utilizadas e prints da execução.
