# Roadmap

**4 phases** | **10 requirements mapped** | All v1 requirements covered ✓

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Infrastructure Setup | Initialize monorepo, standards, and CI base | ARCH-01, ARCH-02, ARCH-03 | 3 |
| 2 | API Automation | Cover all Swagger Petstore endpoints | API-01, API-02, API-03 | 3 |
| 3 | Web Automation | Complete SauceDemo E2E using Selenium | WEB-01, WEB-02 | 2 |
| 4 | Finalization & CI | Ensure pipeline runs all tests and docs are ready | CI-01, CI-02 | 2 |

### Phase Details

**Phase 1: Infrastructure Setup**
Goal: Initialize monorepo, standards, and CI base
Requirements: ARCH-01, ARCH-02, ARCH-03
Success criteria:
1. Repository has correct directory structure for API and Web.
2. Initial GitHub Actions YAML file is present.
3. Git branching model (main, developer, module branches) is established locally.

**Phase 2: API Automation**
Goal: Cover all Swagger Petstore endpoints
Requirements: API-01, API-02, API-03
Success criteria:
1. 'User' endpoint tests pass successfully.
2. 'Store' endpoint tests pass successfully.
3. 'Pet' endpoint tests pass successfully.

**Phase 3: Web Automation**
Goal: Complete SauceDemo E2E using Selenium
Requirements: WEB-01, WEB-02
Success criteria:
1. Page Objects are cleanly separated from test logic.
2. E2E test runs successfully from login to checkout.

**Phase 4: Finalization & CI**
Goal: Ensure pipeline runs all tests and docs are ready
Requirements: CI-01, CI-02
Success criteria:
1. GitHub Actions pipeline executes both API and Web tests automatically.
2. README.md contains execution instructions, technologies, and prints.
