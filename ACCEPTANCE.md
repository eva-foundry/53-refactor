# ACCEPTANCE.md - Project 53: EVA Refactor Factory

**Version**: 1.0.0  
**Last Updated**: March 2, 2026  
**Project**: 53-refactor (EVA Refactor Factory)  
**Target System**: EVA-JP-v1.2 → Refactored Application

---

## Acceptance Philosophy

This document defines **phase-based acceptance criteria** for the autonomous refactoring of EVA-JP-v1.2. Each phase must pass ALL criteria before proceeding to the next phase. Quality gates are enforced via:
- **Veritas audits**: MTI scoring, gap detection
- **Test coverage**: pytest + Playwright >= 80%
- **Feature parity**: API contract comparison (old vs new)
- **Evidence layer**: Immutable audit trail for every change

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
- [ ] ◻ scripts/as-is-scanner.js implemented (scans EVA-JP-v1.2 → populates data model)
- [ ] ◻ scripts/migration-planner.py implemented (AI generates 500+ stories)
- [ ] ◻ scripts/gen-sprint-manifest.py implemented (sprint planning for GitHub Actions)
- [ ] ◻ agents/discovery-agent.yml created (GitHub Copilot agent config)
- [ ] ◻ agents/planning-agent.yml created (GitHub Copilot agent config)
- [ ] ◻ agents/execution-agent.yml created (GitHub Copilot agent config)
- [ ] ◻ agents/validation-agent.yml created (GitHub Copilot agent config)

#### GitHub Actions Workflow
- [ ] ◻ .github/workflows/refactor-workflow.yml created (discover → plan → execute → validate jobs)
- [ ] ◻ .github/workflows/sprint-agent.yml created (per-story execution)
- [ ] ◻ Workflow tested via workflow_dispatch trigger (dry-run mode)

#### Data Model Integration
- [ ] ◻ Layer L33 (migrations) schema defined in 37-data-model
- [ ] ◻ Layer L34 (refactor_decisions) schema defined in 37-data-model
- [ ] ◻ API routes implemented: POST /model/migrations/, POST /model/refactor_decisions/
- [ ] ◻ PLAN.md seeded to WBS layer via seed-from-plan.py (29 initial stories)

### Sign-Off Gate

**Approved By**: ______________ (User: @marco.presta)  
**Date**: ______________  
**Notes**: Phase 0 Bootstrap complete when all checkboxes above are ☑ (checked).

---

## Phase 1: Discovery (Sprints 1-2, Weeks 1-2)

### Objective
Scan EVA-JP-v1.2 codebase and generate complete as-is architecture documentation in the Data Model.

### Acceptance Criteria

#### Veritas Baseline Audit
- [ ] ◻ Veritas audit completes without errors (node src/cli.js audit --repo C:\AICOE\EVA-JP-v1.2)
- [ ] ◻ .eva/trust.json generated with MTI baseline score
- [ ] ◻ MTI baseline >= 50 (target established)
- [ ] ◻ Test coverage measured: ~40% (legacy code)
- [ ] ◻ Gaps identified: missing tests, missing implementation, technical debt
- [ ] ◻ docs/baseline-metrics.md created with summary

#### Data Model Population
- [ ] ◻ Services documented: >= 4 services (backend, frontend, functions, enrichment)
- [ ] ◻ Endpoints extracted: >= 50 endpoints from app/backend/app.py
- [ ] ◻ Screens extracted: >= 80 screens from app/frontend/src/pages/
- [ ] ◻ Containers documented: >= 10 containers (Cosmos, Blob)
- [ ] ◻ Hooks extracted: >= 40 hooks from app/frontend/src/
- [ ] ◻ Components extracted: >= 100 components from app/frontend/src/components/
- [ ] ◻ Infrastructure documented: >= 20 Azure resources from infra/ (Bicep)
- [ ] ◻ Schemas extracted: >= 50 Pydantic models from app/backend/

#### Dependency Graph
- [ ] ◻ Dependency graph generated with zero broken links
- [ ] ◻ Screen → Endpoint relationships mapped (API calls)
- [ ] ◻ Endpoint → Container relationships mapped (read/write)
- [ ] ◻ Endpoint → External Service relationships mapped (Azure OpenAI, AI Search)
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

#### Technology Stack Decisions
- [ ] ◻ Frontend migration decision recorded: POST /model/refactor_decisions/REFACTOR-D001
- [ ] ◻ Backend migration decision recorded: POST /model/refactor_decisions/REFACTOR-D002
- [ ] ◻ Data layer migration decision recorded: POST /model/refactor_decisions/REFACTOR-D003
- [ ] ◻ IaC migration decision recorded: POST /model/refactor_decisions/REFACTOR-D004
- [ ] ◻ docs/frontend-migration-options.md created (3+ options analyzed)
- [ ] ◻ docs/backend-migration-options.md created (4+ options analyzed)
- [ ] ◻ docs/data-migration-options.md created (4+ options analyzed)
- [ ] ◻ docs/iac-migration-options.md created (3+ options analyzed)

#### WBS Generation (AI-Driven)
- [ ] ◻ PLAN.md expanded to >= 500 stories (AI-generated via migration-planner.py)
- [ ] ◻ Epic 11: Backend Decomposition (100+ stories)
- [ ] ◻ Epic 12: Frontend Modularization (80+ stories)
- [ ] ◻ Epic 13: Data Migration (60+ stories)
- [ ] ◻ Epic 14: Feature Parity Validation (20+ stories)
- [ ] ◻ Epic 15: Quality Gates (10+ stories)
- [ ] ◻ Epic 16: Performance & Cost Validation (10+ stories)
- [ ] ◻ All stories have size estimation: XS/S/M/L/XL
- [ ] ◻ All stories have sprint assignment: REFACTOR-S05 through REFACTOR-S23
- [ ] ◻ All stories have dependencies mapped: blockers field populated

#### Risk Assessment
- [ ] ◻ docs/risk-assessment.md created with >= 10 risks identified
- [ ] ◻ Risk 1: Feature Parity Gaps (mitigation strategy defined)
- [ ] ◻ Risk 2: Data Migration Failures (mitigation strategy defined)
- [ ] ◻ Risk 3: Agent Hallucinations (mitigation strategy defined)
- [ ] ◻ Risk 4: Schedule Overrun (mitigation strategy defined)
- [ ] ◻ All high-impact risks have contingency plans
- [ ] ◻ Risks posted to Data Model: POST /model/risks/ for each

#### Sprint Planning
- [ ] ◻ docs/sprint-plan.md created with 20-sprint timeline (S05-S23 after Planning phase)
- [ ] ◻ Sprint allocation: Backend (S05-S14), Frontend (S15-S18), Data (S19-S20), Testing (S21-S22), Validation (S23)
- [ ] ◻ Story dependencies validated: topological sort passes (no circular dependencies)
- [ ] ◻ Effort estimated: total story points calculated (target: 1000+ points)
- [ ] ◻ Velocity target: 50 story points/week (1000 points / 20 weeks)

#### Data Model Seeding
- [ ] ◻ seed-from-plan.py executed: 500+ stories loaded to WBS layer
- [ ] ◻ WBS query validated: GET /model/wbs/?project=53-refactor returns all stories
- [ ] ◻ Sprint metadata extracted: sprint field populated for >= 95% of stories
- [ ] ◻ Assignee metadata extracted: assignee field populated for >= 90% of stories
- [ ] ◻ Blocker metadata extracted: blockers field populated where applicable

#### Quality Gates
- [ ] ◻ All Planning stories completed (REFACTOR-02-001 through REFACTOR-02-012)
- [ ] ◻ PLAN.md version 2.0.0 committed to git (500+ stories)
- [ ] ◻ Zero high-severity blockers for Execution phase
- [ ] ◻ Planning phase review completed (PM approval for WBS + sprint plan)

### Sign-Off Gate

**Approved By**: ______________  
**Date**: ______________  
**Total Stories**: __________ (target >= 500)  
**Total Story Points**: __________ (target >= 1000)  
**Notes**: Phase 2 Planning complete when all checkboxes above are ☑ and WBS approved.

---

## Phase 3: Execution (Sprints 5-22, Weeks 5-22)

### Objective
Autonomously execute refactor via GitHub Actions workflows with full traceability.

### Acceptance Criteria

#### Sprint 5-14: Backend Decomposition (10 sprints)
- [ ] ◻ 100+ backend stories completed (REFACTOR-03-001 through REFACTOR-03-100)
- [ ] ◻ Monolithic app.py (2473 lines) decomposed into >= 10 modular routers
- [ ] ◻ All routers use FastAPI APIRouter pattern
- [ ] ◻ RAG approaches/ migrated to Agent Framework agents
- [ ] ◻ OpenAPI schemas match old app.py (feature parity)
- [ ] ◻ Unit tests written: pytest coverage >= 80% for each router
- [ ] ◻ Integration tests written: API contract tests pass
- [ ] ◻ MTI >= 70 for all backend modules (Veritas audit)
- [ ] ◻ Zero high-severity gaps in backend (Veritas)
- [ ] ◻ Evidence receipts: 100+ POST /model/evidence/ records

#### Sprint 15-18: Frontend Modularization (4 sprints)
- [ ] ◻ 80+ frontend stories completed (REFACTOR-04-001 through REFACTOR-04-080)
- [ ] ◻ Monolithic frontend split into 3 faces: admin, chat, portal
- [ ] ◻ React 18 upgraded to React 19 (backward compatible)
- [ ] ◻ Fluent UI v8 migrated to Fluent UI v9 (all components)
- [ ] ◻ Spark Design System integrated from 43-eva-spark
- [ ] ◻ API calls migrated: axios → fetch + React Query
- [ ] ◻ Component tests written: Vitest + Testing Library >= 80% coverage
- [ ] ◻ E2E tests written: Playwright for critical user flows
- [ ] ◻ MTI >= 70 for all frontend modules
- [ ] ◻ Evidence receipts: 80+ POST /model/evidence/ records

#### Sprint 19-20: Data Migration (2 sprints)
- [ ] ◻ 60+ data migration stories completed (REFACTOR-05-001 through REFACTOR-05-060)
- [ ] ◻ Postgres schema designed and reviewed (DBA approval)
- [ ] ◻ Dual-write strategy implemented: writes go to both Cosmos + Postgres
- [ ] ◻ Data export scripts created: Cosmos → JSON/CSV
- [ ] ◻ Data import scripts created: JSON/CSV → Postgres
- [ ] ◻ Data reconciliation validated: Cosmos vs Postgres comparison passes
- [ ] ◻ Read cutover completed: all reads from Postgres (Cosmos writes only)
- [ ] ◻ Redis caching implemented: session cache + rate limiting
- [ ] ◻ SQLAlchemy ORM implemented: Postgres connection pool
- [ ] ◻ Data migration tests pass: zero data loss (audit log)
- [ ] ◻ Evidence receipts: 60+ POST /model/evidence/ records

#### Sprint 21-22: Testing & Validation (2 sprints)
- [ ] ◻ 120+ testing stories completed (REFACTOR-06-001 through REFACTOR-06-060+)
- [ ] ◻ Feature parity tests pass: old vs new API contracts match 100%
- [ ] ◻ E2E test suite passes: Playwright for all user flows
- [ ] ◻ Performance tests pass: Locust load test (1000 req/s sustained)
- [ ] ◻ Security scans pass: OWASP ZAP, Bandit, npm audit, Trivy
- [ ] ◻ Secrets scan passes: Git history clean (no leaked credentials)
- [ ] ◻ Test coverage >= 80%: Unit + Integration + E2E combined
- [ ] ◻ MTI >= 70 maintained: All modules pass Veritas audit
- [ ] ◻ Evidence receipts: 120+ POST /model/evidence/ records

#### Overall Execution Quality Gates
- [ ] ◻ All 400+ execution stories completed (Epic 11-13, Sprint 5-22)
- [ ] ◻ Zero high-severity blockers remaining
- [ ] ◻ Quality gates enforced: MTI >= 70 for every story completion
- [ ] ◻ Test coverage >= 80% maintained throughout execution
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

### Objective
Verify feature parity, performance, security, and quality gates before production cutover.

### Acceptance Criteria

#### Feature Parity Validation
- [ ] ◻ API contracts compared: OpenAPI diff shows zero breaking changes
- [ ] ◻ All old endpoints migrated: 50+ endpoints from EVA-JP-v1.2 exist in refactored system
- [ ] ◻ Feature parity tests pass: 100% compatibility (old responses == new responses)
- [ ] ◻ E2E test suite passes: Playwright for all critical user flows
- [ ] ◻ Response times comparable: <= 10% latency difference (old vs new)
- [ ] ◻ docs/api-diff-report.md generated (comprehensive comparison)

#### Quality Gates
- [ ] ◻ **Veritas audit passes**: node src/cli.js audit --repo output/
- [ ] ◻ **MTI Score >= 80**: Target achieved (vs baseline 50, 60% improvement)
- [ ] ◻ **Test Coverage >= 80%**: Measured via pytest --cov + Playwright
- [ ] ◻ **Zero high-severity gaps**: Veritas gap report clean
- [ ] ◻ WBS field population >= 95%: sprint, assignee, ado_id populated
- [ ] ◻ Evidence Layer validation: 500+ evidence receipts collected

#### Security Validation
- [ ] ◻ OWASP ZAP scan passes: Zero high-severity vulnerabilities
- [ ] ◻ Bandit scan passes: Zero high-severity Python security issues
- [ ] ◻ npm audit passes: Zero high-severity Node.js vulnerabilities
- [ ] ◻ Trivy container scan passes: Zero high-severity image vulnerabilities
- [ ] ◻ Secrets scan passes: Git history clean (no leaked credentials or API keys)
- [ ] ◻ OWASP Top 10 compliance: Zero violations (SQL injection, XSS, CSRF, etc.)

#### Performance Validation
- [ ] ◻ Load test passes: 1000 req/s sustained for 10 minutes (Locust)
- [ ] ◻ Latency P95 <= 100ms: Improved from EVA-JP-v1.2 baseline (150ms)
- [ ] ◻ Throughput >= 1000 req/s: Improved from EVA-JP-v1.2 baseline (800 req/s)
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

#### Pre-Cutover Preparation
- [ ] ◻ Cutover plan documented: docs/cutover-plan.md
- [ ] ◻ Stakeholder notification: Users informed 48 hours in advance
- [ ] ◻ Rollback tested: Can revert to EVA-JP-v1.2 within 15 minutes
- [ ] ◻ Database backup: Cosmos DB snapshot taken (point-in-time restore enabled)
- [ ] ◻ Monitoring enabled: Application Insights alerts configured (latency, error rate, availability)

#### Cutover Execution
- [ ] ◻ Traffic shadowing completed: 10% traffic to new system for 1 week (validation period)
- [ ] ◻ Blue/green swap executed: Traffic switched from old to new via Azure Traffic Manager
- [ ] ◻ DNS updated: Canonical URLs point to refactored system
- [ ] ◻ Health checks pass: GET /health returns 200 OK (new system)
- [ ] ◻ Zero downtime: Users experience no interruption during cutover
- [ ] ◻ Old system on standby: EVA-JP-v1.2 kept running for 3 months (rollback window)

#### Post-Cutover Monitoring (First 24 Hours)
- [ ] ◻ Error rate <= 0.1%: 99.9% availability maintained
- [ ] ◻ Latency P95 <= 100ms: Performance SLA met
- [ ] ◻ Zero critical bugs: No P0/P1 incidents
- [ ] ◻ User feedback collected: Survey responses positive (>= 80% satisfaction)
- [ ] ◻ Rollback NOT triggered: System stable

#### Post-Cutover Validation (First Week)
- [ ] ◻ All critical user flows validated: Chat, search, upload, admin working
- [ ] ◻ Data consistency validated: Postgres vs Cosmos reconciliation passes
- [ ] ◻ Performance sustained: Latency, throughput within SLA for 7 days
- [ ] ◻ Cost tracking: Azure spend aligns with forecast ($120/month target)
- [ ] ◻ Security monitoring: Zero incidents (SIEM alerts clean)

#### Legacy System Decommission (3 Months Post-Cutover)
- [ ] ◻ Rollback window expired: EVA-JP-v1.2 no longer needed
- [ ] ◻ Cosmos DB decommissioned: Container deleted, cost eliminated
- [ ] ◻ Old App Service deleted: Resources cleaned up
- [ ] ◻ Bicep IaC archived: Terraform is now the source of truth
- [ ] ◻ Documentation updated: All references to EVA-JP-v1.2 marked as legacy

### Sign-Off Gate

**Approved By**: ______________  
**Date**: ______________  
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
