# ACCEPTANCE.md - Project 53: EVA Refactor Factory

**Version**: 1.1.0 (Greenfield Corrected)
**Last Updated**: March 2, 2026  
**Project**: 53-refactor (EVA Refactor Factory)  
**Strategy**: **Greenfield Rewrite** (Standalone POC, NOT production replacement)

---

## Acceptance Philosophy

This document defines **phase-based acceptance criteria** for the **Greenfield development** of standalone POC showcasing autonomous refactoring workflow. **This is NOT a migration/refactor of EVA-JP-v1.2**, but a fresh build from scratch using proven patterns. Each phase must pass ALL criteria before proceeding. Quality gates are enforced via:
- **Veritas audits**: MTI scoring, gap detection
- **Test coverage**: pytest + Playwright >= 80%
- **Feature parity**: EVA-JP-v1.2 feature set vs 53-refactor implementation (reference-only, NOT code porting)
- **Evidence layer**: Immutable audit trail for every story

**Note**: Criteria are checkboxes (◻) that must be completed (☑) before phase sign-off.

---

## Phase 0: Bootstrap (Current)

### Objective
Initialize project infrastructure, governance documents, agents, and data model integration.

### Acceptance Criteria

#### Governance Documents
- [x] ☑ README.md created with vision, architecture, workflow, agents, success criteria (450 lines)
- [x] ☑ PLAN.md created with Phases 0-4 breakdown, initial 29 stories (future: 500+ stories)
- [x] ☑ STATUS.md created with project tracking, sprint progress, quality metrics
- [x] ☑ ACCEPTANCE.md created with phase-based criteria (this document)
- [ ] ◻ LICENSE file added (MIT recommended)
- [ ] ◻ .gitignore configured for Python, Node.js, Azure, .env secrets

#### Project Structure
- [x] ☑ Directory structure created: .github/workflows/, agents/, scripts/, docs/
- [ ] ◻ Git repository initialized (git init + initial commit)
- [ ] ◻ Remote added: https://github.com/eva-foundry/53-refactor
- [ ] ◻ Pushed to main branch (git push -u origin main)

#### Agents & Scripts
- [ ] ◻ scripts/as-is-scanner.js implemented (scans EVA-JP-v1.2 for **feature parity reference**, NOT code porting)
- [ ] ◻ scripts/migration-planner.py implemented with **Greenfield AI prompts** (generates 500+ build-from-scratch stories, NOT migration stories)
- [ ] ◻ scripts/gen-sprint-manifest.py implemented (Greenfield sprint planning for GitHub Actions)
- [ ] ◻ agents/discovery-agent.yml created (GitHub Copilot config with reference-only instructions)
- [ ] ◻ agents/planning-agent.yml created (GitHub Copilot config with Greenfield WBS generation prompts)
- [ ] ◻ agents/execution-agent.yml created (GitHub Copilot config with pattern sources from 31-eva-faces, 33-eva-brain-v2, 28-rbac, 51-ACA)
- [ ] ◻ agents/validation-agent.yml created (GitHub Copilot config with quality gates)

#### GitHub Actions Workflow
- [ ] ◻ .github/workflows/refactor-workflow.yml created (discover → plan → execute → validate jobs)
- [ ] ◻ .github/workflows/sprint-agent.yml created (per-story execution)
- [ ] ◻ Workflow tested via workflow_dispatch trigger (dry-run mode)

#### Data Model Integration
- [ ] ◻ Layer L33 (feature_parity) schema defined in 37-data-model (EVA-JP-v1.2 features → 53-refactor Greenfield features)
- [ ] ◻ Layer L34 (greenfield_decisions) schema defined in 37-data-model (ADRs for Greenfield choices)
- [ ] ◻ API routes implemented: POST /model/feature_parity/, POST /model/greenfield_decisions/
- [ ] ◻ PLAN.md seeded to WBS layer via seed-from-plan.py (29 initial Greenfield build stories)

### Sign-Off Gate

**Approved By**: ______________ (User: @marco.presta)  
**Date**: ______________  
**Notes**: Phase 0 Bootstrap complete when all checkboxes above are ☑ (checked).

---

## Phase 1: Reference Analysis (Sprints 1-2, Weeks 1-2)

### Objective
Scan EVA-JP-v1.2 to understand **feature set** for parity tracking. NOT for code porting - this is reference-only discovery.

### Acceptance Criteria

#### Veritas Baseline Audit
- [ ] ◻ Veritas audit completes without errors on EVA-JP-v1.2 (node src/cli.js audit --repo C:\AICOE\EVA-JP-v1.2)
- [ ] ◻ .eva/trust.json generated with MTI baseline score for EVA-JP-v1.2
- [ ] ◻ MTI baseline >= 50 established (EVA-JP-v1.2 current state)
- [ ] ◻ Test coverage measured: ~40% (EVA-JP-v1.2 legacy baseline)
- [ ] ◻ docs/baseline-metrics.md created with EVA-JP-v1.2 summary

#### Feature Set Inventory (Reference Only)
- [ ] ◻ Feature inventory extracted: >= 50 API features (Chat, Search, Upload, Admin, etc.)
- [ ] ◻ Endpoints cataloged: >= 50 endpoints from app/backend/app.py (for feature parity reference)
- [ ] ◻ Screens cataloged: >= 80 screens from app/frontend/src/pages/ (for UI parity reference)
- [ ] ◻ .eva/feature-inventory.json generated (feature list for Greenfield parity tracking)
- [ ] ◻ docs/as-is-feature-set.md created (human-readable feature catalog)
- [ ] ◻ Data Model: POST feature_parity records for each EVA-JP-v1.2 feature (status=planned for Greenfield implementation)

**Note**: This phase does NOT populate code/schema details (NO data model containers, hooks, components). Only feature-level inventory for parity tracking.
- [ ] ◻ Graph queryable via GET /model/graph/?node_id=backend&depth=3
- [ ] ◻ docs/dependency-graph.mermaid created (visual diagram)

#### Technical Debt Analysis
- [ ] ◻ Technical debt report generated: docs/technical-debt.md
- [ ] ◻ Categorized by severity: high (10+), medium (20+), low (30+)
- [ ] ◻ Monolithic app.py flagged (2473 lines → needs decomposition)
- [ ] ◻ Synchronous operations flagged (blocking I/O → async/await)
- [ ] ◻ Missing observability flagged (print statements → OpenTelemetry)
- [ ] ◻ Hardcoded config flagged (env vars → Key Vault)
- [ ] ◻ Low test coverage flagged (40% → target 80%)

#### Architecture Documentation
- [ ] ◻ docs/as-is-architecture.md created (comprehensive 8-section report)
- [ ] ◻ docs/as-is-diagrams.md created (Mermaid diagrams: system, component, sequence)
- [ ] ◻ docs/refactor-candidates.md created (100+ prioritized candidates)
- [ ] ◻ .eva/as-is-architecture.json generated (machine-readable snapshot)

#### Quality Gates
- [ ] ◻ All Discovery stories completed (REFACTOR-01-001 through REFACTOR-01-008)
- [ ] ◻ Zero high-severity blockers for Planning phase
- [ ] ◻ Data Model records validated: query GET /model/agent-summary shows 53-refactor records

### Sign-Off Gate

**Approved By**: ______________  
**Date**: ______________  
**MTI Baseline**: __________ (must be >= 50)  
**Notes**: Phase 1 Discovery complete when all checkboxes above are ☑ and MTI baseline established.

---

## Phase 2: Planning (Sprints 3-4, Weeks 3-4)

### Objective
Generate comprehensive modernization WBS with 500+ stories, risk assessment, and sprint plan.

### Acceptance Criteria

#### TechnolGreenfield Planning (Sprints 3-4, Weeks 3-4)

###Objective
Generate comprehensive Greenfield WBS with 500+ build-from-scratch stories using AI, pattern identification, and sprint planning
.

### Acceptance Criteria

#### Architecture Decisions (Greenfield Choices)
- [ ] ◻ Frontend decision recorded: POST /model/greenfield_decisions/REFACTOR-ADR001 (React 19 + Fluent UI v9 from 31-eva-faces)
- [ ] ◻ Backend decision recorded: POST /model/greenfield_decisions/REFACTOR-ADR002 (FastAPI + Agent Framework from 33-eva-brain-v2)
- [ ] ◻ Data layer decision recorded: POST /model/greenfield_decisions/REFACTOR-ADR003 (Postgres + Redis, existing marco* resources)
- [ ] ◻ Security decision recorded: POST /model/greenfield_decisions/REFACTOR-ADR004 (RBAC from 28-rbac)
- [ ] ◻ Observability decision recorded: POST /model/greenfield_decisions/REFACTOR-ADR005 (OpenTelemetry from 51-ACA)
- [ ] ◻ docs/greenfield-approach.md created (rationale for build-from-scratch vs migration)
- [ ] ◻ docs/pattern-sources.md created (31-eva-faces, 33-eva-brain-v2, 28-rbac, 51-ACA inventory)

#### WBS Generation (AI-Driven Greenfield)
- [ ] ◻ PLAN.md expanded to >= 500 Greenfield build stories (AI-generated via migration-planner.py with Greenfield prompts)
- [ ] ◻ Epic 11: Backend Greenfield (100+ stories: FastAPI routers, Agent Framework agents, auth, session management)
- [ ] ◻ Epic 12: Frontend Greenfield (80+ stories: React 19 3-face app, copy 31-eva-faces/shared patterns)
- [ ] ◻ Epic 13: Data Layer Setup (60+ stories: Postgres schema, Redis caching, SQLAlchemy models)
- [ ] ◻ Epic 14: Observability Setup (40+ stories: OpenTelemetry, App Insights integration from 51-ACA)
- [ ] ◻ Epic 15: Security Hardening (30+ stories: RBAC from 28-rbac, Key Vault, managed identities)
- [ ] ◻ Epic 16: Testing & Validation (120+ stories: pytest unit, integration, Playwright E2E >= 80% coverage)
- [ ] ◻ Epic 17: Documentation (70+ stories: OpenAPI, architecture diagrams, runbooks)
- [ ] ◻ All stories have size estimation: XS/S/M/L
- [ ] ◻ All stories have sprint assignment: REFACTOR-S05 through REFACTOR-S23
- [ ] ◻ All stories have pattern sources noted: "Copy from 31-eva-faces/shared/hooks/useAuth.ts"

#### Risk Assessment (Greenfield Focus)
- [ ] ◻ docs/risk-assessment.md created with >= 10 Greenfield-specific risks
- [ ] ◻ Risk 1: Pattern integration complexity (mitigation: early integration tests)
- [ ] ◻ Risk 2: Feature parity gaps discovered late (mitigation: continuous validation)
- [ ] ◻ Risk 3: Agent hallucinations (mitigation: human-in-the-loop PR review)
- [ ] ◻ Risk 4: GitHub Codespaces hours exhausted (mitigation: local Docker fallback)
- [ ] ◻ All high-impact risks have contingency plans

#### Sprint Planning (Greenfield Execution)
- [ ] ◻ docs/sprint-plan.md created with 18-sprint Greenfield timeline (S05-S22)
- [ ] ◻ Sprint allocation: Backend Greenfield (S05-S10), Frontend Greenfield (S11-S14), Data Layer (S15-S16), Observability (S17-S18), Security+Testing (S19-S22)
- [ ] ◻ Story dependencies validated: topological sort passes
- [ ] ◻ Effort estimated: total story points calculated (target: 900+ points)

#### Data Model Seeding (Greenfield WBS)
- [ ] ◻ seed-from-plan.py executed: 500+ Greenfield build stories loaded to WBS layer
- [ ] ◻ WBS query validated: GET /model/wbs/?project=53-refactor returns all Greenfield stories
- [ ] ◻ Feature parity records created: POST /model/feature_parity/ for each EVA-JP-v1.2 feature mapped to 53-refactor story

#### Quality Gates
- [ ] ◻ All Planning stories completed (REFACTOR-02-001 through REFACTOR-02-012)
- [ ] ◻ PLAN.md version 2.0.0 committed (500+ Greenfield stories)
- [ ] ◻ Zero blockers for Greenfield Execution phase

### Sign-Off Gate

**Approved By**: ______________  
**Date**: ______________  
**Total Stories**: __________ (target >= 500)  
**Total Story Points**: __________ (target >= 900)  
**Pattern Sources Identified**: __________ (31-eva-faces, 33-eva-brain-v2, 28-rbac, 51-ACA)  
**Notes**: Phase 2 Greenfield Planning complete when all checkboxes above are ☑

### Acceptance Criteria

#### Sprint 5-14: Backend Decomposition (10 sprints)
- [ ] ◻ 100+ backend stories completed (REFACTOR-03-001 through REFACTOR-03-100)
- [ ] ◻ Monolithic app.py (2473 lines) decomposed into >= 10 modular routers
- [ ] ◻ All Greenfield Execution (Sprints 5-22, Weeks 5-22)

### Objective
Autonomously build standalone POC application from scratch using proven patterns, with full traceability via Evidence Layer.

### Acceptance Criteria

#### Sprint 5-10: Backend Greenfield (6 sprints)
- [ ] ◻ 100+ backend Greenfield stories completed (REFACTOR-11-001 through REFACTOR-11-100)
- [ ] ◻ FastAPI modular routers created from scratch (>= 10 routers: auth, users, chat, search, upload, admin, etc.)
- [ ] ◻ Agent Framework agents implemented for RAG (copy patterns from 33-eva-brain-v2, NO Cosmos RAG approaches ported)
- [ ] ◻ RBAC middleware integrated (copy from 28-rbac, NOT custom EVA-JP-v1.2 auth)
- [ ] ◻ OpenAPI schemas documented for all endpoints
- [ ] ◻ Unit tests written: pytest coverage >= 80% for each router
- [ ] ◻ Integration tests written: API contract tests pass
- [ ] ◻ MTI >= 70 for all backend modules (Veritas audit)
- [ ] ◻ Evidence receipts: 100+ POST /model/evidence/ records
- [ ] ◻ Pattern integration validated: 33-eva-brain-v2 patterns work without modification

#### Sprint 11-14: Frontend Greenfield (4 sprints)
- [ ] ◻ 80+ frontend Greenfield stories completed (REFACTOR-12-001 through REFACTOR-12-080)
- [ ] ◻ React 19 3-face app scaffolded from scratch: admin-face, chat-face, portal-face
- [ ] ◻ 31-eva-faces/shared patterns copied: hooks (useAuth, useActingSession), utils (api-client, formatters), types (User, Session), layouts (AppLayout)
- [ ] ◻ Fluent UI v9 components integrated (NOT Fluent UI v8 legacy components)
- [ ] ◻ API calls implemented: fetch + React Query (NOT axios or custom patterns from EVA-JP-v1.2)
- [ ] ◻ Component tests written: Vitest + Testing Library >= 80% coverage
- [ ] ◻ E2E tests written: Playwright for critical user flows (login, chat, upload, admin)
- [ ] ◻ MTI >= 70 for all frontend modules
- [ ] ◻ Evidence receipts: 80+ POST /model/evidence/ records
- [ ] ◻ Pattern integration validated: 31-eva-faces/shared hooks work without modification

#### Sprint 15-16: Data Layer Setup (2 sprints)
- [ ] ◻ 60+ data layer Greenfield stories completed (REFACTOR-13-001 through REFACTOR-13-060)
- [ ] ◻ Postgres schema designed from scratch (NO Cosmos schema porting, clean relational design)
- [ ] ◻ Connection to existing marco-eva-postgres configured (new DB: refactor_poc)
- [ ] ◻ SQLAlchemy async models created (asyncpg driver, connection pooling)
- [ ] ◻ Alembic migrations implemented for schema versioning
- [ ] ◻ Redis caching integrated: connect to existing marco-eva-cache (key prefix: refactor:*)
- [ ] ◻ Cache strategy implemented: session cache + API response cache
- [ ] ◻ Data layer tests pass: unit tests for models, integration tests for queries
- [ ] ◻ MTI >= 70 for data layer
- [ ] ◻ Evidence receipts: 60+ POST /model/evidence/ records

#### Sprint 17-18: Observability & Deployment (2 sprints)
- [ ] ◻ 40+ observability stories completed (REFACTOR-14-001 through REFACTOR-14-040)
- [ ] ◻ OpenTelemetry instrumentation added (copy patterns from 51-ACA Application-Insights-Logger.ps1)
- [ ] ◻ App Insights integration: connect to existing marco-eva-appinsights
- [ ] ◻ Structured logging implemented (Python structlog / logging.json)
- [ ] ◻ Deployment to marco-containerenv successful (az containerapp create --name marco-refactor-backend)
- [ ] ◻ Health endpoints implemented: /health, /ready, /metrics
- [ ] ◻ Evidence receipts: 40+ POST /model/evidence/ records
- [ ] ◻ ADO bidirectional sync active: WBS ↔ ADO work items synchronized
- [ ] ◻ Evidence layer complete: 400+ evidence receipts collected
- [ ] ◻ No critical bugs introduced (P0/P1 severity)
- [ ] ◻ Sprint velocity maintained: >= 50 story points/week average

### Sign-Off Gate

**Approved By**: ______________  
**Date**: ______________  
**Stories Completed**: __________ / __________ (target 400+/500+)  
**MTI Score**: __________ (target >= 70)  
**Test Coverage**: __________% (target >= 80%)  
**Notes**: Phase 3 Execution complete when all checkboxes above are ☑ and quality gates pass.

---

## Phase 4: Validation (Sprint 23, Week 23)

#### Sprint 19-22: Security & Testing (4 sprints)
- [ ] ◻ 150+ security + testing stories completed (REFACTOR-15-001 through REFACTOR-16-120)
- [ ] ◻ RBAC tested: 28-rbac patterns validated (role-based access control)
- [ ] ◻ Key Vault integration: connect to marco-eva-kv, retrieve secrets securely
- [ ] ◻ Managed identities configured: passwordless auth to Postgres, Redis, Storage
- [ ] ◻ Feature parity tests implemented: Compare 53-refactor endpoints vs EVA-JP-v1.2 feature set (100% coverage)
- [ ] ◻ Performance tests implemented: Locust load test (1000 req/s sustained)
- [ ] ◻ Security scans & Feature Parity (Sprint 23, Week 23)

### Objective
Verify feature parity, performance, security, and quality gates for standalone POC demonstration.

**Note**: This is a **standalone POC** (NOT production replacement of EVA-JP-v1.2). Success = high-quality demonstration of autonomous Greenfield development.

### Acceptance Criteria

#### Feature Parity Validation (vs EVA-JP-v1.2 Reference)
- [ ] ◻ Feature inventory comparison: 53-refactor implements >= 95% of EVA-JP-v1.2 feature set
- [ ] ◻ API feature parity tests pass: Chat, Search, Upload, Admin features work as expected
- [ ] ◻ UI feature parity tests pass: Playwright tests verify UI flows match EVA-JP-v1.2 user experience
- [ ] ◻ E2E test suite passes: 100% critical user flows validated
- [ ] ◻ Response times comparable: <= 20% latency difference (acceptable for POC)
- [ ] ◻ docs/feature-parity-report.md generated (comprehensive comparison vs EVA-JP-v1.2)

#### Quality Gates (POC High-Bar Targets)
- [ ] ◻ **Veritas audit passes**: node src/cli.js audit --repo C:\AICOE\eva-foundry\53-refactor\output
- [ ] ◻ **MTI Score >= 80**: Target achieved (vs EVA-JP-v1.2 baseline ~50, 60% improvement demonstrated)
- [ ] ◻ **Test Coverage >= 80%**: Measured via pytest --cov + Playwright (vs EVA-JP-v1.2 ~40%)
- [ ] ◻ **Zero high-severity gaps**: Veritas gap report clean
- [ ] ◻ WBS field population >= 95%: sprint, assignee, ado_id, status populated
- [ ] ◻ Evidence Layer validation: 500+ evidence receipts collected, queryable via `/model/evidence/?project_id=53-refactor`

#### Security Validation
- [ ] ◻ OWASP ZAP scan passes: Zero high-severity vulnerabilities
- [ ] ◻ Bandit scan passes: Zero high-severity Python security issues
- [ ] ◻ npm audit passes: Zero high-severity Node.js vulnerabilities
- [ ] ◻ Trivy container scan passes: Zero high-severity image vulnerabilities
- [ ] ◻ Secrets scan passes: Git history clean (no leaked credentials)
- [ ] ◻ OWASP Top 10 compliance: Zero violations

#### Performance Validation (POC Benchmarks)
- [ ] ◻ Load test passes: 1000 req/s sustained for 5 minutes (Locust benchmark)
- [ ] ◻ Latency P95 <= 150ms: Acceptable for POC demonstration
- [ ] ◻ Throughput >= 800 req/s: Comparable to EVA-JP-v1.2 baseline
- [ ] ◻ Resource utilization <= 80%: CPU, memory within acceptable limits
- [ ] ◻ Error rate <= 0.5%: 99.5% success rate under load (acceptable for POC)
- [ ] ◻ docs/performance-report.md generated

#### Infrastructure Validation (Existing marco* Resources)
- [ ] ◻ marco-eva-postgres connection validated: Postgres DB `refactor_poc` accessible, queries work
- [ ] ◻ marco-eva-cache connection validated: Redis caching functional, key prefix `refactor:*` isolated
- [ ] ◻ marco-containerenv deployment successful: `marco-refactor-backend` app running, health checks pass
- [ ] ◻ marcoeva storage connection validated: Blob uploads work
- [ ] ◻ marco-eva-kv integration validated: Secrets retrieved securely
- [ ] ◻ marco-eva-appinsights telemetry validated: Logs, traces, metrics flowing
- [ ] ◻ **Zero new infrastructure created**: All resources use existing marco* sandbox (zero new Azure cost800 req/s)
- [ ] ◻ Resource utilization <= 80%: CPU, memory within acceptable limits
- [ ] ◻ Error rate <= 0.1%: 99.9% success rate under load
- [ ] ◻ docs/performance-report.md generated (benchmark comparison)

#### Cost Validation
- [ ] ◻ Azure cost calculated: Monthly spend for refactored system
- [ ] ◻ Cost comparison: Refactored <= 60% of EVA-JP-v1.2 cost (40%+ reduction)
- [ ] ◻ Cosmos DB decommissioned: $80/month RU/s → $0
- [ ] ◻ Postgres + Redis cost: $48/month total (60% cheaper than Cosmos)
- [ ] ◻ ROI justified: Payback period <= 6 months
- [ ] ◻ docs/cost-analysis.md generated (detailed breakdown)

#### Deployment Validation
- [ ] ◻ Terraform IaC validated: terraform plan shows expected resources
- [ ] ◻ Blue/green deployment successful: Traffic switched without downtime
- [ ] ◻ Rollback plan tested: Can revert to EVA-JP-v1.2 within 15 minutes
- [ ] ◻ Monitoring configured: Application Insights dashboards + alerts
- [ ] ◻ Runbook created: docs/operations-runbook.md (troubleshooting, escalation)
- [ ] ◻ Parallel deployment validated: Both systems run side-by-side for 1 week (traffic shadowing 10%)

#### Final Quality Gates (Critical)
- [ ] ◻ **All 6 validation stories completed** (REFACTOR-06-001 through REFACTOR-06-006)
- [ ] ◻ **Feature parity: 100%** (all old functionality available in new system)
- [ ] ◻ **MTI Score >= 80** (60% improvement from baseline 50)
- [ ] ◻ **Test Coverage >= 80%** (unit + integration + E2E)
- [ ] ◻ **Security: Zero high-severity issues** (OWASP Top 10 compliant)
- [ ] ◻ **Performance: Latency P95 <= 100ms** (33% improvement)
- [ ] ◻ **Cost: 40%+ reduction** (Postgres + Redis vs Cosmos)
- [ ] ◻ **Zero P0/P1 bugs** (critical issues resolved before cutover)

### Sign-Off Gate

**Approved By**: ______________  
**Date**: ______________  
**MTI Score**: __________ / 80 (target)  
**Test Coverage**: __________% / 80% (target)  
**Cost Reduction**: __________% / 40% (target)  
**Production Cutover Date**: ______________  
**Notes**: Phase 4 Validation complete when all checkboxes above are ☑ and final quality gates pass. **Production cutover approved.**

---

## Post-Validation: Production Cutover

### Objective
Safely transition from EVA-JP-v1.2 to refactored system with zero downtime and rollback capability.

### Acceptance Criteria

#### POC Demonstration Preparation
- [ ] ◻ Demo script created: docs/demo-script.md (guided walkthrough of key features)
- [ ] ◻ Architecture diagrams finalized: Mermaid diagrams showing Greenfield structure, pattern sources
- [ ] ◻ Deployment runbook created: docs/deployment-runbook.md (how to deploy to marco* resources)
- [ ] ◻ Evidence report generated: docs/evidence-report.md (500+ evidence receipts, DPDCA audit trail)
- [ ] ◻ Pattern integration report: docs/pattern-integration-report.md (how 31-eva-faces, 33-eva-brain-v2, 28-rbac, 51-ACA patterns were used)

#### POC Demonstration Validation
- [ ] ◻ Live demo successful: Walkthrough of Chat, Search, Upload, Admin features
- [ ] ◻ Pattern showcase: Demonstrated copied patterns work without modification (31-eva-faces/shared hooks, 33-eva-brain-v2 Agent Framework, 28-rbac RBAC middleware, 51-ACA OpenTelemetry)
- [ ] ◻ Zero-infrastructure showcase: Validated zero new Azure costs (all marco* existing resources)
- [ ] ◻ Veritas-Model-ADO workflow showcase: Dashboard shows 500+ stories, evidence receipts, MTI tracking
- [ ] ◻ Evidence Layer showcase: Query `/model/evidence/?project_id=53-refactor` returns complete audit trail
- [ ] ◻ Quality showcase: MTI >= 80 (vs EVA-JP-v1.2 ~50), test coverage >= 80% (vs ~40%)

#### Documentation & Knowledge Transfer
- [ ] ◻ README.md finalized: Complete project overview, architecture, deployment instructions
- [ ] ◻ LESSONS-LEARNED.md created: What worked, what didn't, recommendations for future Greenfield projects
- [ ] ◻ ADO work items closed: All 500+ stories marked `status=done` in ADO board
- [ ] ◻ GitHub wiki updated: https://github.com/eva-foundry/53-refactor/wiki with complete documentation
- [ ] ◻ Stakeholder presentation: PowerPoint deck + live demo to project sponsors

### Sign-Off Gate

**Approved By**: ______________  
**Date**: ______________  
**Project Type**: Standalone POC (NOT production release)  
**Greenfield Success Demonstrated**: ☐ YES ☐ NO  
**Pattern Reuse Validated**: ☐ YES ☐ NO  
**Zero New Infrastructure Confirmed**: ☐ YES ☐ NO  
**Cutover Status**: ☐ SUCCESS / ☐ ROLLBACK  
**Notes**: Production cutover complete when all checkboxes above are ☑ and system stable for 1 week.

---

## Summary: Overall Project Acceptance

### Critical Success Criteria (Must Pass ALL)

| Criterion | Target | Actual | Status |
|---|---|---|---|
| **MTI Improvement** | >= 60% (50 → 80) | ______ | ☐ PASS / ☐ FAIL |
| **Test Coverage** | >= 80% | ______% | ☐ PASS / ☐ FAIL |
| **Feature Parity** | 100% | ______% | ☐ PASS / ☐ FAIL |
| **Performance (P95)** | <= 100ms | ______ms | ☐ PASS / ☐ FAIL |
| **Throughput** | >= 1000 req/s | ______ req/s | ☐ PASS / ☐ FAIL |
| **Cost Reduction** | >= 40% | ______% | ☐ PASS / ☐ FAIL |
| **Security** | Zero high-severity | ______ issues | ☐ PASS / ☐ FAIL |
| **Availability** | >= 99.9% | ______% | ☐ PASS / ☐ FAIL |

### Project Sign-Off

**Project Manager**: ______________ (Signature)  
**Date**: ______________

**Product Owner**: ______________ (Signature)  
**Date**: ______________

**Technical Lead**: ______________ (Signature)  
**Date**: ______________

**Security Lead**: ______________ (Signature)  
**Date**: ______________

**Operations Lead**: ______________ (Signature)  
**Date**: ______________

---

## Appendix A: Veritas Integration

**Quality Gates Enforced Per Story**:
1. MTI >= 70: Veritas audit must pass before marking story done
2. Test Coverage >= 80%: pytest --cov-fail-under=80 must exit 0
3. Zero high-severity gaps: Veritas gap report must be clean
4. WBS field population: sprint, assignee, ado_id must be populated
5. Evidence receipt: POST /model/evidence/ must succeed

**Veritas Audit Command**:
```bash
node src/cli.js audit --repo C:\AICOE\eva-foundry\53-refactor\output
```

**Automated Enforcement**:
- GitHub Actions workflow: refactor-workflow.yml includes validate job
- Quality gates block PR merge if Veritas fails
- Agent notified to fix violations before proceeding

---

## Appendix B: Evidence Layer Integration

**Evidence Receipts Required**:
- Every story completion → POST /model/evidence/ with:
  - `story_id`, `sprint_id`, `phase` (DO, CHECK)
  - `artifacts`: files changed, lines added/removed, test results, coverage
  - `validation`: test_result, lint_result, security_scan, feature_parity
  - `commits`: Git commit SHAs with EVA-STORY tags
  - `timeline`: started_at, completed_at, duration_ms

**Queryability**:
- Evidence receipts queryable by sprint: `GET /model/evidence/?sprint_id=REFACTOR-S05`
- Evidence receipts queryable by story: `GET /model/evidence/?story_id=REFACTOR-03-001`
- Portfolio-level aggregation: Total cost, duration, test coverage across all stories

**Immutability**:
- Evidence receipts are immutable (no PUT/DELETE)
- Provides tamper-proof audit trail for entire refactor (March-August 2026)

---

## Appendix C: Rollback Plan

**Rollback Triggers**:
- Critical bug: P0 severity, affects > 50% of users
- Data loss: Postgres vs Cosmos reconciliation fails
- Performance degradation: P95 latency > 200ms (2x SLA)
- Security incident: OWASP Top 10 vulnerability exploited
- Availability: < 99% for > 1 hour

**Rollback Procedure** (15 minutes):
1. Switch Traffic Manager: Route 100% traffic to EVA-JP-v1.2 (old system)
2. DNS rollback: Update canonical URLs to point to old App Service
3. Disable dual-write: Stop writes to Postgres (Cosmos only)
4. Notify stakeholders: Email + Slack alert
5. Post-mortem: Root cause analysis → fix → re-attempt cutover

**Rollback Window**: 3 months (EVA-JP-v1.2 remains active until June 2026)

---

**END OF ACCEPTANCE.md v1.0.0**

**Next Review**: After Phase 0 Bootstrap completes (governance documents + git repository initialized)
