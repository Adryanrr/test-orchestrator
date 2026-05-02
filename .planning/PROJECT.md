# Test Orchestrator

## O que é isso

Um monorepo de automação de testes em Python, seguindo uma arquitetura semelhante à do BMI, mas em Python, e adotando o padrão de backend do back-v3 da TT. Inclui automação de testes de API para o Swagger Petstore e automação de testes Web E2E para o SauceDemo usando Selenium. O projeto se integra a uma pipeline de CI (GitHub Actions) para executar ambas as suítes de teste.

## Valor Central

Demonstrar capacidade robusta em automação de testes com excelente organização de código, padrões de projeto (como Page Objects), commits semânticos e execução contínua via CI/CD.

## Requisitos

### Validados

(Nenhum ainda — entregue para validar)

### Ativos

- [ ] Configuração da estrutura do monorepo em Python
- [ ] Automação de API (Swagger Petstore) cobrindo os endpoints User, Store e Pet
- [ ] Automação Web (SauceDemo) usando Selenium com fluxo E2E (login, adicionar ao carrinho, finalizar compra)
- [ ] Pipeline de CI executando ambos os projetos de automação
- [ ] Documentação (README.md) com instruções, tecnologias e prints de execução
- [ ] Uso de Commits Semânticos e estratégia de ramificação (main, developer, e branches de módulo)

### Fora de Escopo

- [ ] Implementação das APIs ou aplicações web reais — O foco do projeto é exclusivamente na automação de testes dos serviços existentes.

## Contexto

Este é um trabalho escolar/acadêmico para avaliar a capacidade técnica no desenvolvimento de automação de testes.
- **Datas:** Apresentações nos dias 07 e 14 de maio.
- **Critérios de Avaliação:** Qualidade do código, organização, reusabilidade, estratégia de testes, execução em CI/CD e domínio do conteúdo.
- **Restrição de Commits:** Commits devem seguir um padrão semântico (feat, fix, etc.) e serão avaliados.

## Restrições

- **Linguagem**: Python
- **Ferramentas**: Selenium para Web, bibliotecas padrão do Python/requests para API
- **Estrutura do Repositório**: Único repositório / monorepo para ambas as automações com um único README.
- **Comentários**: Permitidos apenas comentários essenciais.

## Principais Decisões

| Decisão | Justificativa | Resultado |
|----------|-----------|---------|
| Uso do pytest | Framework de testes padrão e poderoso em Python | — Pendente |
| GitHub Actions para CI | Fácil integração com repositórios GitHub para execução da pipeline | — Pendente |
| Page Object Model | Especificado como boa prática para automação de testes web | — Pendente |

---
*Atualizado em: 2026-05-02 após a inicialização*

## Evolução

Este documento evolui nas transições de fase e limites de milestone.

**Após cada transição de fase** (via `/gsd-transition`):
1. Requisitos invalidados? → Mover para Fora de Escopo com o motivo
2. Requisitos validados? → Mover para Validados com referência à fase
3. Novos requisitos surgiram? → Adicionar em Ativos
4. Decisões a registrar? → Adicionar em Principais Decisões
5. "O que é isso" ainda preciso? → Atualizar se houve mudança

**Após cada milestone** (via `/gsd-complete-milestone`):
1. Revisão completa de todas as seções
2. Verificação do Valor Central — ainda é a prioridade certa?
3. Auditoria de Fora de Escopo — os motivos ainda são válidos?
4. Atualizar Contexto com o estado atual
