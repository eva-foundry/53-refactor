# PLAN.md - Project 53: EVA Refactor Factory

**Version**: 1.0.0  
**Last Updated**: March 2, 2026  
**Sprint**: Pre-Sprint (Planning Phase)  
**Status**: Bootstrap

---

## Project Metadata

```yaml
project_id: 53-refactor
project_name: EVA Refactor Factory
maturity: idea
source_system: EVA-JP-v1.2
target_system: 53-refactor-output
migration_strategy: hybrid
total_sprints: 20
sprint_duration: 1_week
target_mti: 80
target_coverage: 0.80
```

---

## Phase 0: Bootstrap (Current)

### Objective
Initialize Project 53-refactor infrastructure, governance documents, and data model integration.

### Stories

#### [REFACTOR-00-001] Create project governance documents
**Size**: S | **Status**: in-progress | **Assignee**: @agent:github-copilot

- [x] README.md with vision, architecture, workflow
- [ ] PLAN.md with 4-phase WBS
- [ ] STATUS.md with current state
- [ ] ACCEPTANCE.md with success criteria
- [ ] .gitignore for Python, Node.js, Azure
- [ ] LICENSE (MIT)

#### [REFACTOR-00-002] Create discovery agent
**Size**: M | **Status**: planned | **Assignee**: @agent:discovery-

agent

Scripts:
- `scripts/as-is-scanner.js`: Scans EVA-JP-v1.2, populates data model
- `agents/discovery-agent.yml`: GitHub Copilot agent config

Outputs:
- Data Model records: services, endpoints, screens, containers
- `.eva/discovery.json`: As-is architecture snapshot
- `docs/as-is-architecture.md`: Human-readable report

#### [REFACTOR-00-003] Create planning agent
**Size**: L | **Status**: planned | **Assignee**: @agent:planning-agent

Scripts:
- `scripts/migration-planner.py`: AI-generates 500+ story WBS
- `scripts/technology-recommender.py`: Analyzes tech stack options
- `agents/planning-agent.yml`: GitHub Copilot agent config

Outputs:
- `PLAN.md` (expanded): 500+ stories across 4 phases
- `docs/migration-paths.md`: Option analysis (incremental, greenfield, hybrid)
- `docs/risk-assessment.md`: Risk register with mitigation strategies

#### [REFACTOR-00-004] Create execution agent
**Size**: L | **Status**: planned | **Assignee**: @agent:execution-agent

Scripts:
- `agents/execution-agent.yml`: GitHub Copilot agent config
- `.github/workflows/sprint-agent.yml`: Story execution workflow

Capabilities:
- Reads old code via Data Model (endpoint schemas, dependencies)
- Generates new code using patterns from 31-eva-faces, 33-eva-brain-v2
- Writes tests (pytest unit, pytest integration, Playwright E2E)
- Creates PR with EVA-STORY tags + evidence receipt

#### [REFACTOR-00-005] Create validation agent
**Size**: M | **Status**: planned | **Assignee**: @agent:validation-agent

Scripts:
- `scripts/feature-parity-test.py`: Compares old vs new APIs
- `scripts/performance-benchmark.py`: Latency, throughput comparison
- `agents/validation-agent.yml`: GitHub Copilot agent config

Quality Gates:
- Test coverage >= 80%
- MTI >= 70
- Zero OWASP Top 10 violations
- API contracts match (OpenAPI diff)

#### [REFACTOR-00-006] Create refactor workflow
**Size**: M | **Status**: planned | **Assignee**: @agent:github-copilot

File: `.github/workflows/refactor-workflow.yml`

Stages:
1. Discover: Run Veritas + as-is-scanner
2. Plan: Generate sprint manifest
3. Execute: Run sprint-agent.yml for each story
4. Validate: Feature parity + quality gates
5. Deploy: Azure Container Apps (blue/green)

Triggers:
- `workflow_dispatch` (manual)
- `schedule` (cron: every Monday 9 AM for new sprint)

#### [REFACTOR-00-007] Extend data model with refactor layers
**Size**: S | **Status**: planned | **Assignee**: @agent:github-copilot

New Layers:
- L33: `migrations` (source_files → target_files mapping)
- L34: `refactor_decisions` (architecture decision records)

Scripts:
- `37-data-model/api/routes/migrations.py`
- `37-data-model/api/routes/refactor_decisions.py`
- `37-data-model/model/migrations.json`
- `37-data-model/model/refactor_decisions.json`

---

## Phase 1: Discovery (Sprints 1-2, Weeks 1-2)

### Objective
Scan EVA-JP-v1.2 codebase and generate complete as-is architecture documentation in the Data Model.

### Epic 1: Source Code Analysis

#### [REFACTOR-01-001] Scan EVA-JP-v1.2 backend services
**Sprint**: REFACTOR-S01 | **Size**: M | **Status**: planned | **Assignee**: @agent:discovery-agent

Scan Targets:
- `app/backend/app.py` (2473 lines, monolithic FastAPI app)
- `app/backend/routers/` (if exists)
- `app/backend/approaches/` (RAG approach classes)
- `functions/` (Azure Functions enrichment pipeline)

Data Model Records:
- POST `/model/services/`: backend, enrichment, functions
- POST `/model/endpoints/`: Extract FastAPI routes (@app.get, @app.post, etc.)
- POST `/model/containers/`: Cosmos containers, Blob containers from env vars

Output:
- 4 services
- 50+ endpoints
- 10+ containers

#### [REFACTOR-01-002] Scan EVA-JP-v1.2 frontend components
**Sprint**: REFACTOR-S01 | **Size**: M | **Status**: planned | **Assignee**: @agent:discovery-agent

Scan Targets:
- `app/frontend/src/pages/` (React page components)
- `app/frontend/src/components/` (reusable components)
- `app/frontend/src/api/` (API client calls)

Data Model Records:
- POST `/model/screens/`: One per page component
- POST `/model/hooks/`: Custom React hooks (useState, useEffect patterns)
- POST `/model/components/`: Shared UI components

Output:
- 80+ screens
- 40+ hooks
- 100+ components

#### [REFACTOR-01-003] Extract API contracts and dependencies
**Sprint**: REFACTOR-S01 | **Size**: L | **Status**: planned | **Assignee**: @agent:discovery-agent

Analysis:
- Parse FastAPI Pydantic models → OpenAPI schema
- Extract endpoint request/response types
- Build screen → endpoint call graph (axios/fetch calls)
- Identify external dependencies (Azure OpenAI, AI Search, Blob, Cosmos)

Data Model Records:
- POST `/model/schemas/`: Pydantic models
- POST `/model/relationships/`: screen calls endpoint, endpoint writes container
- POST `/model/infrastructure/`: Azure resources from infra/

Output:
- 50+ schemas
- 200+ relationships
- 20+ infrastructure resources

#### [REFACTOR-01-004] Identify technical debt and anti-patterns
**Sprint**: REFACTOR-S01 | **Size**: M | **Status**: planned | **Assignee**: @agent:discovery-agent

Analysis:
- Monolithic app.py (2473 lines → needs decomposition)
- Hardcoded config (env vars → Key Vault)
- Missing tests (coverage ~40% → target 80%)
- Synchronous operations (blocking I/O → async/await)
- Missing observability (print statements → OpenTelemetry)

Output:
- `docs/technical-debt.md`: Prioritized list (high/medium/low)
- Data Model: Flag high-risk endpoints, screens

#### [REFACTOR-01-005] Run baseline Veritas audit on EVA-JP-v1.2
**Sprint**: REFACTOR-S01 | **Size**: S | **Status**: planned | **Assignee**: @agent:github-copilot

Command:
```bash
cd C:\AICOE\eva-foundry\48-eva-veritas
node src/cli.js audit --repo C:\AICOE\EVA-JP-v1.2 --warn-only
```

Baseline Metrics:
- MTI Score: Target >= 50 (establish baseline)
- Test Coverage: ~40% (measured)
- Gaps: Missing implementation, missing tests
- Complexity Coverage: Code parsing score

Output:
- `.eva/trust.json` with baseline MTI
- `docs/baseline-metrics.md`

### Epic 2: Architecture Documentation

#### [REFACTOR-01-006] Generate dependency graph
**Sprint**: REFACTOR-S02 | **Size**: M | **Status**: planned | **Assignee**: @agent:discovery-agent

Graph Nodes:
- Services (backend, frontend, functions, enrichment)
- Endpoints (FastAPI routes)
- Screens (React pages)
- Containers (Cosmos, Blob)

Graph Edges:
- Screen → Endpoint (API calls)
- Endpoint → Container (read/write)
- Endpoint → External Service (Azure OpenAI, AI Search)

Output:
- `POST /model/graph/` records
- `docs/dependency-graph.mermaid`: Visual diagram
- Query: `GET /model/graph/?node_id=backend&depth=3`

#### [REFACTOR-01-007] Document as-is architecture
**Sprint**: REFACTOR-S02 | **Size**: M | **Status**: planned | **Assignee**: @agent:github-copilot

Sections:
1. System Overview (services, scale, tech stack)
2. Frontend Architecture (React components, state management)
3. Backend Architecture (FastAPI routes, RAG approaches)
4. Data Layer (Cosmos schemas, Blob containers)
5. External Dependencies (Azure services)
6. Deployment (Azure App Service, Functions)
7. Security (authentication, authorization, secrets)
8. Observability (logging, monitoring, alerts)

Output:
- `docs/as-is-architecture.md` (comprehensive report)
- `docs/as-is-diagrams.md` (Mermaid diagrams)

#### [REFACTOR-01-008] Identify refactor candidates
**Sprint**: REFACTOR-S02 | **Size**: S | **Status**: planned | **Assignee**: @agent:planning-agent

Criteria:
- High complexity (cyclomatic complexity > 15)
- Low test coverage (< 50%)
- High coupling (many dependencies)
- Performance bottlenecks (P95 latency > 500ms)
- Security risks (hardcoded secrets, SQL injection)

Output:
- `docs/refactor-candidates.md`: Prioritized list (100+ candidates)
- Data Model: Mark endpoints/screens with `refactor_priority: high`

---

## Phase 2: Planning (Sprints 3-4, Weeks 3-4)

### Objective
Generate comprehensive modernization WBS with 500+ stories, risk assessment, and sprint plan.

### Epic 3: Technology Stack Analysis

#### [REFACTOR-02-001] Evaluate frontend migration options
**Sprint**: REFACTOR-S03 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

Options:
1. **Keep React 18** (Low Risk): Minor upgrades only
2. **Upgrade React 19** (Medium Risk): New hooks, improved Suspense
3. **Migrate Fluent UI v8 → v9** (Medium Risk): Component API changes
4. **Add Spark Design System** (Low Risk): Import from 43-eva-spark

Recommendation:
- React 18 → 19 (minor upgrade, backward compatible)
- Fluent UI v8 → v9 (better performance, new components)
- Integrate Spark design system (reduce custom CSS)

Output:
- `docs/frontend-migration-options.md`
- Decision: POST `/model/refactor_decisions/REFACTOR-D001`

#### [REFACTOR-02-002] Evaluate backend migration options
**Sprint**: REFACTOR-S03 | **Size**: L | **Status**: planned | **Assignee**: @agent:planning-agent

Options:
1. **Keep FastAPI monolith** (Low Risk): Minor refactors only
2. **Decompose to modular routers** (Medium Risk): Split app.py (2473 lines) → 10 route modules
3. **Migrate to Agent Framework** (High Risk): Replace approaches/ with Agent Framework agents
4. **Hybrid** (Medium Risk): Decompose routers + Agent Framework for RAG only

Recommendation:
- **Hybrid approach**: Decompose app.py → 10 routers, use Agent Framework for RAG agents
- Keep FastAPI (proven, performant, OpenAPI support)
- Add Pydantic v2 for strict typing
- Add OpenTelemetry for observability

Output:
- `docs/backend-migration-options.md`
- Decision: POST `/model/refactor_decisions/REFACTOR-D002`

#### [REFACTOR-02-003] Evaluate data layer migration options
**Sprint**: REFACTOR-S03 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

Options:
1. **Keep Cosmos DB** (Low Risk): No migration, optimize queries
2. **Migrate to Postgres** (High Risk): Relational model, JSONB for semi-structured
3. **Hybrid: Postgres + Redis** (Medium Risk): Postgres for relational, Redis for caching
4. **Dual-write strategy** (Low Risk): Write to both Cosmos + Postgres, gradual cutover

Recommendation:
- **Postgres + Redis**: Cosmos → Postgres (relational data), Redis (session cache, rate limiting)
- Cost savings: 60% reduction (Cosmos RU/s expensive)
- SQLAlchemy ORM: Supports both Cosmos and Postgres (gradual migration)

Output:
- `docs/data-migration-options.md`
- Decision: POST `/model/refactor_decisions/REFACTOR-D003`

#### [REFACTOR-02-004] Evaluate IaC migration options
**Sprint**: REFACTOR-S03 | **Size**: S | **Status**: planned | **Assignee**: @agent:planning-agent

Options:
1. **Keep Bicep** (Low Risk): Azure-native, no changes
2. **Migrate to Terraform** (Medium Risk): Better state management, multi-cloud
3. **Hybrid: Bicep + Terraform** (High Risk): Use both (not recommended)

Recommendation:
- **Terraform**: Better for multi-environment (dev/staging/prod), reusable modules
- Import modules from 22-rg-sandbox Terraform templates
- Use Azure Backend for state storage

Output:
- `docs/iac-migration-options.md`
- Decision: POST `/model/refactor_decisions/REFACTOR-D004`

### Epic 4: WBS Generation (AI-Driven)

#### [REFACTOR-02-005] Generate backend decomposition stories
**Sprint**: REFACTOR-S04 | **Size**: XL | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Analyze app/backend/app.py (2473 lines). Decompose into modular routers:
- Chat router: /chat, /chat/stream endpoints
- Search router: /search, /search/semantic endpoints
- Upload router: /upload, /upload/status endpoints
- Admin router: /admin/config, /admin/logs endpoints
- etc.

For each router, generate:
- [REFACTOR-03-NNN] Create {router_name} router module
- Size: M (100-300 lines per router)
- Acceptance: OpenAPI schema matches old app.py
- Tests: pytest unit tests, coverage >= 80%
```

Output:
- 100+ stories in `PLAN.md` (Epic 5: Backend Decomposition)
- Each story: title, description, acceptance criteria, size

#### [REFACTOR-02-006] Generate frontend modularization stories
**Sprint**: REFACTOR-S04 | **Size**: XL | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Analyze app/frontend/src. Split monolithic frontend into 3 faces:
- Admin Face: /admin/* routes (user mgmt, config, logs)
- Chat Face: /chat/* routes (RAG chat, history, settings)
- Portal Face: / (landing page, docs, auth)

For each face, generate stories for:
- Page migrations
- Component refactors
- API client updates
- Fluent UI v9 upgrades
```

Output:
- 80+ stories in `PLAN.md` (Epic 6: Frontend Modularization)

#### [REFACTOR-02-007] Generate data migration stories
**Sprint**: REFACTOR-S04 | **Size**: L | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Plan Cosmos → Postgres + Redis migration:
1. Schema design (Cosmos JSON → Postgres tables)
2. Data export scripts (Cosmos query → CSV/JSON)
3. Data import scripts (CSV/JSON → Postgres)
4. Dual-write implementation (write to both, read from Postgres)
5. Data reconciliation (compare Cosmos vs Postgres)
6. Cutover plan (redirect reads to Postgres)
7. Cosmos decommission
```

Output:
- 60+ stories in `PLAN.md` (Epic 7: Data Migration)

#### [REFACTOR-02-008] Generate observability & security stories
**Sprint**: REFACTOR-S04 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Generate stories for:
- OpenTelemetry instrumentation (replace print() with structured logging)
- Application Insights integration (traces, metrics, logs)
- RBAC implementation (use 28-rbac patterns)
- Key Vault integration (migrate env vars → secrets)
- Dependency updates (security patches)
- OWASP Top 10 audit (SQL injection, XSS, CSRF)
```

Output:
- 70+ stories in `PLAN.md` (Epic 8: Observability & Security)

#### [REFACTOR-02-009] Generate testing & validation stories
**Sprint**: REFACTOR-S04 | **Size**: L | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Generate comprehensive test suite stories:
- Unit tests: pytest for each router (80% coverage target)
- Integration tests: API contract tests (old vs new)
- E2E tests: Playwright for critical user flows
- Performance tests: Locust load testing (1000 req/s target)
- Security tests: OWASP ZAP scans
- Feature parity tests: Compare old vs new responses
```

Output:
- 120+ stories in `PLAN.md` (Epic 9: Testing & Validation)

#### [REFACTOR-02-010] Generate documentation stories
**Sprint**: REFACTOR-S04 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Document the refactored system:
- Architecture Decision Records (ADRs)
- API documentation (OpenAPI/Swagger)
- Deployment guide (Terraform → Azure)
- Developer guide (setup, testing, contributing)
- Operations runbook (monitoring, troubleshooting)
- Security guide (authentication, authorization, secrets)
```

Output:
- 70+ stories in `PLAN.md` (Epic 10: Documentation)

### Epic 5: Risk Assessment & Sprint Planning

#### [REFACTOR-02-011] Perform risk assessment
**Sprint**: REFACTOR-S04 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

Risks:
1. **Feature Parity Gaps** (High Impact, High Likelihood)
2. **Data Migration Failures** (High Impact, Medium Likelihood)
3. **Agent Hallucinations** (Medium Impact, Medium Likelihood)
4. **Schedule Overrun** (Medium Impact, High Likelihood)
5. **Cost Overruns** (Low Impact, Medium Likelihood)

For each risk:
- Likelihood: Low/Medium/High
- Impact: Low/Medium/High
- Mitigation strategies
- Contingency plans

Output:
- `docs/risk-assessment.md`
- POST `/model/risks/` for each identified risk

#### [REFACTOR-02-012] Generate sprint plan (20 sprints)
**Sprint**: REFACTOR-S04 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

Sprint Allocation:
- Sprint 1-2: Discovery (Phase 1)
- Sprint 3-4: Planning (Phase 2)
- Sprint 5-14: Backend Decomposition (10 sprints, 10 stories/sprint)
- Sprint 15-18: Frontend Modularization (4 sprints, 20 stories/sprint)
- Sprint 19-20: Data Migration (2 sprints, 30 stories/sprint)
- Sprint 21-22: Testing & Validation (2 sprints, 60 stories/sprint)
- Sprint 23: Deployment & Cutover

Output:
- `docs/sprint-plan.md`: 20-sprint timeline
- Each story assigned to sprint_id
- Dependencies mapped (story X blocks story Y)

---

## Phase 3: Execution (Sprints 5-22, Weeks 5-22)

### Objective
Autonomously execute refactor via GitHub Actions workflows with full traceability.

### Epic 11: Backend Decomposition (Sprints 5-14)

#### [REFACTOR-03-001] Create chat router module
**Sprint**: REFACTOR-S05 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Source: `app/backend/app.py:1-500`  
Target: `output/routers/chat.py`

Tasks:
1. Extract chat endpoints from app.py
2. Create FastAPI router: `router = APIRouter(prefix="/chat", tags=["chat"])`
3. Migrate endpoints: `/chat`, `/chat/stream`, `/chat/history`
4. Port Pydantic models: `ChatRequest`, `ChatResponse`
5. Write tests: `tests/routers/test_chat.py` (coverage >= 80%)

Acceptance:
- [ ] OpenAPI schema matches old app.py
- [ ] All tests pass (pytest)
- [ ] MTI >= 70 (Veritas audit)
- [ ] Feature parity: old `/chat` == new `/chat` (response comparison)

#### [REFACTOR-03-002] Create search router module
**Sprint**: REFACTOR-S05 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Source: `app/backend/app.py:500-800`  
Target: `output/routers/search.py`

Tasks:
1. Extract search endpoints from app.py
2. Create FastAPI router: `router = APIRouter(prefix="/search", tags=["search"])`
3. Migrate endpoints: `/search`, `/search/semantic`, `/search/filters`
4. Port Azure AI Search client logic
5. Write tests: `tests/routers/test_search.py`

Acceptance:
- [ ] Search results match old system (same relevance)
- [ ] Tests pass (pytest + integration)
- [ ] MTI >= 70

#### [REFACTOR-03-003] Create upload router module
**Sprint**: REFACTOR-S06 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Source: `app/backend/app.py:800-1100`  
Target: `output/routers/upload.py`

Tasks:
1. Extract upload endpoints from app.py
2. Create router: `/upload`, `/upload/status`, `/upload/list`
3. Port Blob Storage client logic
4. Add file validation (size, type, virus scan)
5. Write tests: `tests/routers/test_upload.py`

Acceptance:
- [ ] File uploads work (Blob Storage)
- [ ] Validation rules match old system
- [ ] Tests pass

...

**Note**: Stories [REFACTOR-03-004] through [REFACTOR-03-100] follow same pattern.  
Total: 100 backend decomposition stories (10 stories/sprint × 10 sprints).

### Epic 12: Frontend Modularization (Sprints 15-18)

#### [REFACTOR-04-001] Create admin-face project scaffold
**Sprint**: REFACTOR-S15 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Tasks:
1. Clone 31-eva-faces/admin-face structure
2. Update package.json: dependencies, scripts
3. Configure Vite: vite.config.ts
4. Setup Fluent UI v9: import providers
5. Create shared folder: hooks, utils, types

Acceptance:
- [ ] `npm run dev` starts dev server
- [ ] `npm run build` produces dist/
- [ ] Fluent UI v9 components render

#### [REFACTOR-04-002] Migrate admin user management page
**Sprint**: REFACTOR-S15 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Source: `app/frontend/src/pages/Admin/Users.tsx`  
Target: `output/admin-face/src/pages/Users.tsx`

Tasks:
1. Port Users.tsx component (React 18 → 19)
2. Upgrade Fluent UI v8 → v9:
   - `<PrimaryButton>` → `<Button appearance="primary">`
   - `<DetailsList>` → `<DataGrid>`
3. Update API calls: axios → fetch + React Query
4. Write tests: `tests/pages/Users.test.tsx` (Vitest + Testing Library)

Acceptance:
- [ ] User list renders correctly
- [ ] CRUD operations work (create, read, update, delete)
- [ ] Tests pass (Vitest)

...

**Note**: Stories [REFACTOR-04-003] through [REFACTOR-04-080] follow same pattern.  
Total: 80 frontend modularization stories (20 stories/sprint × 4 sprints).

### Epic 13: Data Migration (Sprints 19-20)

#### [REFACTOR-05-001] Design Postgres schema
**Sprint**: REFACTOR-S19 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Tasks:
1. Analyze Cosmos containers: users, documents, chats, uploads
2. Design Postgres tables with proper relations
3. Use JSONB for semi-structured data (chat messages)
4. Add indexes for performance (user_id, document_id)
5. Write migration scripts: Alembic

Acceptance:
- [ ] Schema review passed (DBA approval)
- [ ] Indexes optimized (explain analyze)
- [ ] Migration scripts tested (dev environment)

#### [REFACTOR-05-002] Implement dual-write strategy
**Sprint**: REFACTOR-S19 | **Size**: L | **Status**: planned | **Assignee**: @agent:execution-agent

Tasks:
1. Create database abstraction layer: `db/repository.py`
2. Implement dual-write: every write → both Cosmos + Postgres
3. Add feature flag: `DUAL_WRITE_ENABLED=true`
4. Monitor writes: latency, errors, consistency
5. Write tests: verify both DBs updated

Acceptance:
- [ ] All writes go to both Cosmos and Postgres
- [ ] Latency acceptable (< 200ms P95)
- [ ] Zero data loss (audit log)

...

**Note**: Stories [REFACTOR-05-003] through [REFACTOR-05-060] follow same pattern.  
Total: 60 data migration stories (30 stories/sprint × 2 sprints).

---

## Phase 4: Validation (Sprints 23, Week 23)

### Objective
Verify feature parity, performance, security, and quality gates before production cutover.

### Epic 14: Feature Parity Validation

#### [REFACTOR-06-001] Compare old vs new API contracts
**Sprint**: REFACTOR-S23 | **Size**: M | **Status**: planned | **Assignee**: @agent:validation-agent

Script: `scripts/feature-parity-test.py`

Tasks:
1. Export OpenAPI schemas: old app.py vs new routers
2. Compare endpoints: paths, methods, request/response schemas
3. Identify breaking changes (flag for manual review)
4. Generate diff report

Acceptance:
- [ ] 100% endpoint coverage (all old endpoints migrated)
- [ ] Zero breaking changes (or approved by PM)
- [ ] Report: `docs/api-diff-report.md`

#### [REFACTOR-06-002] Run E2E test suite on both systems
**Sprint**: REFACTOR-S23 | **Size**: L | **Status**: planned | **Assignee**: @agent:validation-agent

Tests (Playwright):
1. User authentication flow (login, logout)
2. Chat flow (send message, stream response, view history)
3. Search flow (query, filter, pagination)
4. Upload flow (select file, upload, view status)
5. Admin flow (manage users, view logs)

Acceptance:
- [ ] All E2E tests pass on old system (baseline)
- [ ] All E2E tests pass on new system (parity)
- [ ] Response times comparable (< 10% difference)

### Epic 15: Quality Gates

#### [REFACTOR-06-003] Run Veritas audit on refactored system
**Sprint**: REFACTOR-S23 | **Size**: M | **Status**: planned | **Assignee**: @agent:github-copilot

Command:
```bash
node src/cli.js audit --repo C:\AICOE\eva-foundry\53-refactor\output
```

Metrics:
- MTI Score: >= 80 (target, vs baseline 50)
- Test Coverage: >= 80% (measured via pytest cov)
- Gaps: Zero missing implementation
- Quality Gates: All pass (Veritas + custom)

Acceptance:
- [ ] MTI >= 80 (PASS)
- [ ] Coverage >= 80% (PASS)
- [ ] Zero high-severity gaps

#### [REFACTOR-06-004] Run security scans
**Sprint**: REFACTOR-S23 | **Size**: M | **Status**: planned | **Assignee**: @agent:validation-agent

Scans:
1. **OWASP ZAP**: Web application security testing
2. **Bandit**: Python security linter
3. **npm audit**: Node.js dependency vulnerabilities
4. **Trivy**: Container image scanning
5. **Secrets**: Git history scan for leaked secrets

Acceptance:
- [ ] Zero high-severity vulnerabilities
- [ ] Zero secrets in code or Git history
- [ ] All dependencies patched

### Epic 16: Performance & Cost Validation

#### [REFACTOR-06-005] Run performance benchmarks
**Sprint**: REFACTOR-S23 | **Size**: M | **Status**: planned | **Assignee**: @agent:validation-agent

Benchmarks (Locust):
1. Load test: 1000 req/s sustained for 10 minutes
2. Latency: P50, P95, P99 for all endpoints
3. Throughput: Requests per second (old vs new)
4. Resource utilization: CPU, memory, disk I/O

Acceptance:
- [ ] Latency P95 <= 100ms (old: 150ms, improved)
- [ ] Throughput >= 1000 req/s (old: 800 req/s, improved)
- [ ] Resource usage <= 80% (CPU, memory)

#### [REFACTOR-06-006] Calculate cost comparison
**Sprint**: REFACTOR-S23 | **Size**: S | **Status**: planned | **Assignee**: @agent:github-copilot

Cost Items:
1. **Cosmos DB RU/s**: $X/month → $0 (decommissioned)
2. **Postgres Flexible Server**: $0 → $Y/month
3. **Redis Cache**: $0 → $Z/month
4. **App Service**: $A/month → $A/month (same)
5. **Functions**: $B/month → $B/month (same)

Acceptance:
- [ ] Total cost reduced by >= 40% (Postgres + Redis cheaper than Cosmos)
- [ ] ROI justified (6-month payback period)

---

## Backlog (Future Enhancements)

### Epic 17: Advanced Features (Post-Refactor)

- [ ] [REFACTOR-07-001] Add multi-tenant support (isolated data per tenant)
- [ ] [REFACTOR-07-002] Implement rate limiting (Redis-based)
- [ ] [REFACTOR-07-003] Add caching layer (Redis + CDN)
- [ ] [REFACTOR-07-004] Migrate to microservices (Kubernetes)
- [ ] [REFACTOR-07-005] Add GraphQL API (alternative to REST)
- [ ] [REFACTOR-07-006] Implement real-time features (WebSockets)
- [ ] [REFACTOR-07-007] Add mobile app (React Native)

---

## Appendix A: Story Size Guidelines

**XS** (1-2 hours):
- Simple config changes
- Documentation updates
- Minor bug fixes

**S** (4-6 hours):
- Small feature additions
- Refactor single function
- Add unit tests

**M** (1-2 days):
- Refactor single module
- Migrate single router
- Add integration tests

**L** (3-5 days):
- Refactor large component
- Complex data migration
- Feature with multiple endpoints

**XL** (1-2 weeks):
- Complete subsystem refactor
- Multi-step migration
- Cross-cutting concerns

---

## Appendix B: Veritas Integration

All stories use Veritas for quality gates:

```bash
# Run Veritas audit after each story completion
node scripts/veritas-audit.js --story REFACTOR-03-001

# Quality gates:
# 1. MTI >= 70
# 2. Test coverage >= 80%
# 3. Zero high-severity gaps
# 4. WBS fields populated (sprint, assignee, ado_id)

# If gates fail:
# - Block PR merge
# - Notify agent for fixes
# - Log violations to trust.json
```

---

## Appendix C: Evidence Collection

Every story completion generates evidence receipt:

```json
{
  "story_id": "REFACTOR-03-001",
  "sprint_id": "REFACTOR-S05",
  "phase": "DO",
  "agent": "agent:execution-agent",
  "correlation_id": "REFACTOR-S05-20260302-2300",
  "artifacts": {
    "files_changed": ["output/routers/chat.py", "tests/routers/test_chat.py"],
    "lines_added": 350,
    "lines_removed": 0,
    "test_result": "PASS",
    "coverage": 0.85,
    "mti_score": 74
  },
  "validation": {
    "test_result": "PASS",
    "lint_result": "PASS",
    "security_scan": "PASS",
    "feature_parity": true
  },
  "commits": ["abc123 feat(REFACTOR-03-001): create chat router module"],
  "timeline": {
    "started_at": "2026-03-02T18:00:00Z",
    "completed_at": "2026-03-02T20:30:00Z",
    "duration_ms": 9000000
  }
}
```

POST to `/model/evidence/` after each story.

---

**End of PLAN.md v1.0.0**

**Next Steps**:
1. Complete Phase 0 Bootstrap (stories REFACTOR-00-001 through REFACTOR-00-007)
2. Run Discovery (Phase 1: Sprints 1-2)
3. Generate full 500+ story WBS via AI (Phase 2: Sprints 3-4)
4. Execute autonomous refactor (Phase 3: Sprints 5-22)
5. Validate and deploy (Phase 4: Sprint 23)
