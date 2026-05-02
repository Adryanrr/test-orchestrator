# Test Orchestrator

## What This Is

A Python-based automated testing monorepo, following an architecture similar to BMI but in Python, and adopting the backend standard from TT's back-v3. It includes API test automation for Swagger Petstore and E2E Web test automation for SauceDemo using Selenium. The project integrates with a CI pipeline (GitHub Actions) to execute both test suites.

## Core Value

Demonstrate robust test automation capability with excellent code organization, design patterns (like Page Objects), semantic commits, and continuous integration execution.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Python Monorepo structure setup
- [ ] API Automation (Swagger Petstore) covering User, Store, and Pet endpoints
- [ ] Web Automation (SauceDemo) using Selenium with an E2E flow (login, add to cart, checkout)
- [ ] CI Pipeline executing both automation projects
- [ ] Documentation (README.md) with instructions, technologies, and execution prints
- [ ] Adherence to Semantic Commits and specific Branching strategy (main, developer, module branches)

### Out of Scope

- [ ] Implementation of the actual APIs or Web applications — This project focuses purely on the test automation of existing services.

## Context

This is an assignment to evaluate technical capacity in test automation.
- **Due Dates:** Presentations on May 7 and 14.
- **Evaluation Criteria:** Code quality, organization, reusability, test strategy, CI/CD execution, and content domain.
- **Commit constraints:** Meaningful semantic commits (feat, fix, etc.) will be evaluated.

## Constraints

- **Language**: Python
- **Tools**: Selenium for Web, standard Python libraries/requests for API
- **Repository Structure**: Single repository / monorepo for both automations with a single README.
- **Comments**: Only essential comments allowed.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use of pytest | Standard and powerful test framework in Python | — Pending |
| GitHub Actions for CI | Easy integration with GitHub repositories for pipeline execution | — Pending |
| Page Object Model | Specified as a best practice for web test automation | — Pending |

---
*Last updated: 2026-05-02 after initialization*

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state
