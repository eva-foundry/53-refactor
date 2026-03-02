# PLAN.md - Project 53: EVA Refactor Factory

**Version**: 1.0.0  
**Last Updated**: March 2, 2026 5:12 PM ET (Phase 2 audit complete)  
**Sprint**: Phase 2 Complete → Ready for Phase 3 Execution  
**Status**: Greenfield Planning Complete (115 stories seeded, architecture documented)

---

## Project Metadata

**IMPORTANT**: Project 53 has its **OWN DEDICATED Azure DevOps project** (`EVA-Refactor`) and is **NOT mixed** with `eva-poc` or any other project.

```yaml
project_id: 53-refactor
project_name: EVA Refactor Factory
maturity: idea
reference_system: EVA-JP-v1.2  # Feature parity reference (NOT source for code porting)
target_system: 53-refactor-output  # Greenfield standalone POC
migration_strategy: greenfield  # Build from scratch, NOT port/decompose
development_environment: github_codespaces  # 180 hrs available
total_sprints: 20
sprint_duration: 1_week
target_mti: 80
target_coverage: 0.80
infrastructure: existing_marco_resources  # Use 22-rg-sandbox marco* resources
quality_bar: high  # Like 51-ACA reference implementation
ado_project_name: EVA-Refactor
ado_epic_id: '33'
ado_team: EVA-Refactor Team
ado_url: https://dev.azure.com/marcopresta/EVA-Refactor
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
**Size**: M | **Status**: planned | **Assignee**: @agent:discovery-agent

Scripts:
- `scripts/as-is-scanner.js`: Scans EVA-JP-v1.2 for **feature parity reference** (NOT for code porting)
- `agents/discovery-agent.yml`: GitHub Copilot agent config

Outputs:
- Data Model records: services, endpoints, screens, containers (feature set reference)
- `.eva/discovery.json`: As-is feature set snapshot for parity tracking
- `docs/as-is-feature-set.md`: Human-readable feature list

**Purpose**: Understand **what** EVA-JP-v1.2 does (features), NOT **how** it's implemented (code).

#### [REFACTOR-00-003] Create planning agent
**Size**: L | **Status**: planned | **Assignee**: @agent:planning-agent

Scripts:
- `scripts/migration-planner.py`: AI-generates 500+ **Greenfield build stories** (NOT migration)
- `agents/planning-agent.yml`: GitHub Copilot agent config with Greenfield prompts

AI Prompt Strategy:
> "Generate WBS for building standalone POC from scratch using React 19 + Agent Framework + Postgres.
> DO NOT port code from EVA-JP-v1.2. Generate stories for writing NEW code using patterns from:
> 31-eva-faces/shared, 33-eva-brain-v2, 28-rbac, 51-ACA."

Outputs:
- `PLAN.md` (expanded): 500+ Greenfield build stories (Backend Greenfield, Frontend Greenfield, Data Layer Setup, Observability, Security, Testing, Documentation)
- `docs/greenfield-approach.md`: Rationale for build-from-scratch vs migration
- `docs/risk-assessment.md`: Risk register with mitigation strategies

#### [REFACTOR-00-004] Create execution agent with Greenfield instructions
- `.github/workflows/sprint-agent.yml`: Story execution workflow

Capabilities:
- Reads **feature requirements** via Data Model (NOT old code)
- Generates **new code from scratch** using patterns from 31-eva-faces/shared, 33-eva-brain-v2, 28-rbac, 51-ACA
- Writes tests (pytest unit, pytest integration, Playwright E2E)
- Creates PR with EVA-STORY tags + evidence receipt

**NOT Allowed**:
- Copying code from EVA-JP-v1.2
- Porting legacy monolithic structure
- Using Cosmos DB SDKs (Greenfield uses Postgres)

**Allowed**:
- Copying proven patterns from 31-eva-faces/shared (hooks, utils, types)
- Referencing EVA-JP-v1.2 for feature parity validation
- Using Agent Framework examples from 33-eva-brain-v2
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
1. Discofeature_parity` (EVA-JP-v1.2 features → 53-refactor features mapping for completeness tracking)
- L34: `greenfield_decisions` (architecture decision records for Greenfield choices)

Examples:
```json
// L33: feature_parity
{
  "id": "PARITY-CHAT-001",
  "reference_feature": "Chat RAG with Azure OpenAI",
  "reference_path": "EVA-JP-v1.2/app/backend/app.py#L234",
  "greenfield_story": "REFACTOR-11-045",
  "status": Reference Analysis (Sprints 1-2, Weeks 1-2)

### Objective
Scan EVA-JP-v1.2 to understand **feature set** for parity tracking. NOT for code porting - this is reference-only discovery.

### Epic 1: Feature Set Discovery

#### [REFACTOR-01-001] Scan EVA-JP-v1.2 backend for feature inventory
**Sprint**: REFACTOR-S01 | **Size**: M | **Status**: planned | **Assignee**: @agent:discovery-agent

**Purpose**: Understand what features exist (Chat, Search, Upload, Admin), NOT how they're implemented.

Scan Targets:
- `app/backend/app.py` → Extract API endpoints (methods, paths, purpose)
- `app/backend/approaches/` → Identify RAG patterns (for feature parity, NOT code reuse)
- `functions/` → Document enrichment pipeline features

Data Model Records (for reference):
- POST `/model/feature_parity/`: Map features (e.g., "Chat RAG" -> will become REFACTOR-11-045)
- Summary: 50+ API features identified for Greenfield reimplementation

Output:
- `.eva/feature-inventory.json`: API features list
- `docs/as-is-feature-set.md`: Human-readable feature catalog
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

## Phase 2: Greenfield Planning (Sprints 3-4, Weeks 3-4)

### Objective
Generate comprehensive Greenfield WBS with 500+ build-from-scratch stories using AI, pattern identification from proven implementations (31-eva-faces, 33-eva-brain-v2, 28-rbac, 51-ACA), and sprint planning.

### Epic 3: Architecture Decisions (Greenfield)

#### [REFACTOR-02-001] Document frontend Greenfield choices
**Sprint**: REFACTOR-S03 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

**Decision**: Build React 19 + Fluent UI v9 + Vite 3-face app from scratch

**Pattern Sources**:
- **31-eva-faces**: Proven 3-face architecture (admin-face, chat-face, portal-face)
- **31-eva-faces/shared**: hooks (useAuth, useActingSession), utils (api-client, formatters), types (User, Session), layouts (AppLayout)

**Why Greenfield** (vs porting EVA-JP-v1.2 React 18 monolith):
- EVA-JP-v1.2 uses mixed Fluent UI v8/v9 (technical debt)
- Monolithic structure (hard to maintain)
- Missing test coverage (~40%)
- **Clean slate**: React 19 + Fluent UI v9 only, modular from day 1, >= 80% test coverage target

Output:
- `docs/greenfield-approach.md` (rationale section: Frontend)
- ADR: POST `/model/greenfield_decisions/REFACTOR-ADR001`

#### [REFACTOR-02-002] Document backend Greenfield choices
**Sprint**: REFACTOR-S03 | **Size**: L | **Status**: planned | **Assignee**: @agent:planning-agent

**Decision**: Build FastAPI + Microsoft Agent Framework from scratch with modular routers

**Pattern Sources**:
- **33-eva-brain-v2**: Agent Framework RAG patterns, multi-agent orchestration, modular router structure
- **28-rbac**: RBAC middleware for FastAPI (role-based auth)
- **51-ACA**: OpenTelemetry + Application Insights telemetry patterns

**Why Greenfield** (vs refactoring EVA-JP-v1.2 monolithic app.py):
- EVA-JP-v1.2 app.py is 2473 lines (monolithic, hard to test)
- 4 custom RAG approaches (maintenance burden, no observability)
- Missing async/await (blocking I/O)
- **Clean slate**: Modular routers from day 1, Agent Framework unified RAG, async throughout, OpenTelemetry instrumentation

Output:
- `docs/greenfield-approach.md` (rationale section: Backend)
- ADR: POST `/model/greenfield_decisions/REFACTOR-ADR002`

#### [REFACTOR-02-003] Document data layer Greenfield choices
**Sprint**: REFACTOR-S03 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

**Decision**: Use existing `marco-sandbox-cosmos` for POC (zero new cost) OR create small Postgres if relational model critical

**Infrastructure**:
- **Cosmos DB**: `marco-sandbox-cosmos` (existing, EsDAICoE-Sandbox)
  - Advantages: Already exists, zero new cost, proven at scale
  - Schema: Design clean Cosmos containers (NOT ported from EVA-JP-v1.2 legacy schema)
- **Alternative**: Postgres Flexible Server B1ms (~$30/mo) if relational model critical
- **Cache**: In-memory cache (Python `cachetools`) for POC, upgrade to Redis if needed (~$16/mo)

**Why Greenfield schema**:
- EVA-JP-v1.2 Cosmos schema has legacy technical debt
- **Clean slate**: Design optimal schema for Greenfield use cases

Output:
- `docs/greenfield-approach.md` (rationale section: Data Layer)
- ADR: POST `/model/greenfield_decisions/REFACTOR-ADR003`

#### [REFACTOR-02-004] Document infrastructure Greenfield choices
**Sprint**: REFACTOR-S03 | **Size**: S | **Status**: planned | **Assignee**: @agent:planning-agent

**Decision**: Deploy to existing App Service Plan (marco-sandbox-asp-backend) - **ZERO new infrastructure**

**Deployment**:
- **Backend**: Add new App Service to `marco-sandbox-asp-backend` (Linux, canadacentral) - existing plan, zero new cost
- **Frontend**: Static Web App Free tier OR add to existing App Service
- **Container Registry**: `marcosandacr20260203.azurecr.io` (existing, Basic tier)
- **Secrets**: `marcosandkv20260203` (existing Key Vault)
- **Telemetry**: `marco-sandbox-appinsights` (existing App Insights)

**Total Cost**: **$0/month** (uses existing resources only)

Output:
- `docs/greenfield-approach.md` (rationale section: Infrastructure)
- ADR: POST `/model/greenfield_decisions/REFACTOR-ADR004`

### Epic 4: WBS Generation (AI-Driven Greenfield)

#### [REFACTOR-02-005] Generate Backend Greenfield stories with AI
**Sprint**: REFACTOR-S04 | **Size**: XL | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Given EVA-JP-v1.2 feature inventory (Chat RAG, Semantic Search, Document Upload, Admin Config),
generate Greenfield backend WBS for building from scratch:

DO NOT port/migrate app.py (2473 lines). Write NEW routers using 33-eva-brain-v2 patterns:
- Chat router: Build using Agent Framework RAG patterns from 33-eva-brain-v2/routes/chat.py
- Search router: Build using Azure AI Search patterns from 33-eva-brain-v2/routes/search.py
- Upload router: Build using Blob Storage patterns from 33-eva-brain-v2/routes/upload.py
- Admin router: Build using 28-rbac middleware patterns for role-based access

For each router, generate:
- [REFACTOR-03-NNN] Build {router_name} router using {pattern_source}
- Size: M (100-300 lines per router, NEW code)
- Pattern Location: Exact file path in 33-eva-brain-v2 or 28-rbac
- Acceptance: OpenAPI schema documented, pytest >= 80% coverage
- Tests: pytest fixtures from 51-ACA patterns
```

Output:
- 100+ stories in `PLAN.md` (Epic 11: Backend Greenfield)
- Each story: title, pattern source, acceptance criteria, size

#### [REFACTOR-02-006] Generate Frontend Greenfield stories with AI
**Sprint**: REFACTOR-S04 | **Size**: XL | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Given EVA-JP-v1.2 feature inventory, generate Greenfield frontend WBS for building 3-face app:

DO NOT port app/frontend/src. Build NEW React 19 3-face app using 31-eva-faces patterns:
- Admin Face: Build /admin/* routes using 31-eva-faces/admin-face structure (UserManagement, ConfigPanel, LogViewer pages)
- Chat Face: Build /chat routes using 31-eva-faces/chat-face structure (ChatInterface, HistoryPanel, SettingsDrawer components)
- Portal Face: Build / landing page using 31-eva-faces/portal-face structure

Copy 31-eva-faces/shared:
- hooks: useAuth, useActingSession (bootstraps H1 handshake)
- utils: api-client (axios wrapper with auth), formatters
- types: User, Session, ApiResponse
- layouts: AppLayout (nav, header, footer)

For each page/component, generate:
- [REFACTOR-04-NNN] Build {component_name} using 31-eva-faces/{pattern_path}
- Size: S (50-150 lines per component, NEW code)
- Pattern Location: Exact file path in 31-eva-faces
- Acceptance: Fluent UI v9 only, Vitest tests >= 80% coverage
```

Output:
- 80+ stories in `PLAN.md` (Epic 12: Frontend Greenfield)

#### [REFACTOR-02-007] Generate Data Layer Greenfield stories with AI
**Sprint**: REFACTOR-S04 | **Size**: L | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Given data requirements (user profiles, chat history, documents, sessions),
generate Greenfield data layer WBS for building from scratch:

DO NOT migrate Cosmos schema. Design NEW schema optimized for use cases:
- Option 1: Cosmos DB (existing marco-sandbox-cosmos, zero cost)
  - Design clean containers: users, sessions, documents, chat_threads
  - Partition keys optimized for query patterns (NOT legacy EVA-JP-v1.2 keys)
  - TTL policies for ephemeral data (sessions: 24h, temp files: 1h)
- Option 2: Postgres Flexible Server B1ms (~$30/mo) if relational model critical
  - Alembic migrations for schema versioning
  - SQLAlchemy ORM models
  - Connection pooling (asyncpg for async)

Stories for:
1. Schema design (new, NOT ported)
2. ORM models (SQLAlchemy or Pydantic for Cosmos)
3. Repository pattern (abstract data access)
4. Seed data scripts (dev environment bootstrap)
5. In-memory cache (Python cachetools for POC, Redis optional later)
```

Output:
- 60+ stories in `PLAN.md` (Epic 13: Data Layer Greenfield)

#### [REFACTOR-02-008] Generate Observability & Security Greenfield stories with AI
**Sprint**: REFACTOR-S04 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Generate Greenfield observability & security stories (NO migration, NEW code):

Observability (51-ACA patterns):
- OpenTelemetry instrumentation: Use 51-ACA telemetry patterns (structured logging, trace/span decorators)
- Application Insights: Configure using 51-ACA observability setup (connection string from Key Vault)
- Metrics: Custom metrics for RAG quality (answer relevance, latency percentiles)

Security (28-rbac + 31-eva-faces patterns):
- RBAC: Use 28-rbac FastAPI middleware (role decorators: @requires_role("admin"))
- Auth: Copy 31-eva-faces useActingSession hook (H1 handshake with X-Actor-OID header)
- Secrets: Key Vault client patterns (retrieve connection strings, API keys)
- OWASP: Input validation (Pydantic models), output escaping (React sanitization), CORS config

Stories for each area with pattern source (exact file path).
```

Output:
- 70+ stories in `PLAN.md` (Epic 14: Observability & Security)

#### [REFACTOR-02-009] Generate Testing & Validation Greenfield stories with AI
**Sprint**: REFACTOR-S04 | **Size**: L | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Generate comprehensive Greenfield test suite stories (>= 80% coverage target):

Backend Tests (pytest patterns from 33-eva-brain-v2):
- Unit tests: Each router (mock dependencies, test business logic)
- Integration tests: Real API calls (test against dev environment)
- Fixtures: Reusable test data (users, sessions, documents)

Frontend Tests (Vitest + Playwright patterns from 31-eva-faces):
- Component tests: Vitest for each component (render, props, events)
- Integration tests: API mocking (MSW for chat, search, upload)
- E2E tests: Playwright for critical flows (login → chat → upload)

Feature Parity Tests:
- Compare Greenfield POC vs EVA-JP-v1.2 feature set (NOT API contract)
- Validate: All EVA-JP-v1.2 features exist in POC (may differ in implementation)
- Performance: Greenfield POC meets/exceeds EVA-JP-v1.2 latency (p95 < 2s for chat)

Stories for each test category with pattern source.
```

Output:
- 120+ stories in `PLAN.md` (Epic 15: Testing & Validation)

#### [REFACTOR-02-010] Generate Documentation Greenfield stories with AI
**Sprint**: REFACTOR-S04 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

AI Prompt:
```
Document the Greenfield system:
- Architecture Decision Records (ADRs): Why Greenfield vs migration
- Architecture diagrams: 3-face frontend, modular backend with patterns
- API documentation (OpenAPI/Swagger): Auto-generated from FastAPI
- Deployment guide: App Service deployment to marco-sandbox-asp-backend
- Developer guide: Codespaces setup, local Docker, testing
- Pattern catalog: Which 31-eva-faces/33-eva-brain-v2 patterns used where
- Operations runbook: Monitoring (App Insights), troubleshooting, scaling
- Security guide: RBAC (28-rbac), Key Vault, authentication (useActingSession)
```

Output:
- 70+ stories in `PLAN.md` (Epic 16: Documentation)

### Epic 5: Sprint Planning

#### [REFACTOR-02-011] Organize Greenfield stories into 20 sprints
**Sprint**: REFACTOR-S04 | **Size**: M | **Status**: planned | **Assignee**: @agent:planning-agent

Sprint Allocation (Greenfield execution):
- Sprint 1-2: Reference Analysis (Phase 1) - Feature inventory of EVA-JP-v1.2
- Sprint 3-4: Greenfield Planning (Phase 2) - Architecture decisions, WBS generation (500+ stories)
- Sprint 5-14: Backend Greenfield (10 sprints, 10 stories/sprint) - Build FastAPI routers from scratch using 33-eva-brain-v2
- Sprint 15-18: Frontend Greenfield (4 sprints, 20 stories/sprint) - Build React 19 3-face app using 31-eva-faces patterns
- Sprint 19-20: Data Layer Setup (2 sprints, 30 stories/sprint) - Design Cosmos schema OR create Postgres
- Sprint 21-22: Testing & Validation (2 sprints, 60 stories/sprint) - pytest + Vitest + Playwright >= 80% coverage
- Sprint 23: POC Demonstration & Pattern Showcase

Output:
- `docs/sprint-plan.md`: 20-sprint timeline with Greenfield milestones
- Each story assigned to sprint_id
- Dependencies mapped (Backend routers before Frontend API calls)

---

## Phase 3: Greenfield Execution (Sprints 5-22, Weeks 5-22)

### Objective
Autonomously build Greenfield POC via GitHub Copilot agent with full evidence traceability.

### Epic 11: Backend Greenfield (Sprints 5-14)

#### [REFACTOR-03-001] Build chat router using 33-eva-brain-v2 patterns
**Sprint**: REFACTOR-S05 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Pattern Source: `33-eva-brain-v2/services/eva-brain-api/app/routes/chat.py`  
Target: `output/backend/routers/chat.py` (NEW FILE)

Tasks:
1. Copy Agent Framework RAG pattern from 33-eva-brain-v2/routes/chat.py
2. Create FastAPI router: `router = APIRouter(prefix="/chat", tags=["chat"])`
3. Build endpoints: `/chat` (POST), `/chat/stream` (WebSocket), `/chat/history` (GET)
4. Use Agent Framework client patterns (NOT port EVA-JP-v1.2 custom RAG)
5. Write tests: `tests/routers/test_chat.py` using 51-ACA pytest patterns (coverage >= 80%)

Acceptance:
- [ ] OpenAPI schema documented (FastAPI auto-generation)
- [ ] All tests pass (pytest with fixtures from 51-ACA)
- [ ] MTI >= 70 (Veritas audit with EVA-STORY tags)
- [ ] Feature parity: Chat functionality matches EVA-JP-v1.2 (NOT API contract)

#### [REFACTOR-03-002] Build search router using 33-eva-brain-v2 patterns
**Sprint**: REFACTOR-S05 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Pattern Source: `33-eva-brain-v2/services/eva-brain-api/app/routes/search.py`  
Target: `output/backend/routers/search.py` (NEW FILE)

Tasks:
1. Copy Azure AI Search patterns from 33-eva-brain-v2/routes/search.py
2. Create FastAPI router: `router = APIRouter(prefix="/search", tags=["search"])`
3. Build endpoints: `/search` (POST), `/search/semantic` (POST), `/search/filters` (GET)
4. Use Azure AI Search SDK (NOT port EVA-JP-v1.2 custom search)
5. Write tests: `tests/routers/test_search.py` with mock AI Search client

Acceptance:
- [ ] Search results relevant (semantic search working)
- [ ] Tests pass (pytest + integration with dev AI Search index)
- [ ] MTI >= 70

#### [REFACTOR-03-003] Build upload router using 33-eva-brain-v2 patterns
**Sprint**: REFACTOR-S06 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Pattern Source: `33-eva-brain-v2/services/eva-brain-api/app/routes/upload.py`  
Target: `output/backend/routers/upload.py` (NEW FILE)

Tasks:
1. Copy Azure Blob Storage patterns from 33-eva-brain-v2/routes/upload.py
2. Create router: `/upload` (POST multipart), `/upload/status` (GET), `/upload/list` (GET)
3. Use Blob Storage SDK (azure-storage-blob) with marcosand20260203 storage account
4. Create container: "refactor-uploads" in existing storage account
4. Add file validation (size, type, virus scan)
5. Write tests: `tests/routers/test_upload.py`

Acceptance:
- [ ] File uploads work (Blob Storage)
- [ ] Validation rules match old system
- [ ] Tests pass

...

**Note**: Stories [REFACTOR-03-004] through [REFACTOR-03-100] follow same pattern using 33-eva-brain-v2 patterns.  
Total: 100 backend Greenfield stories (10 stories/sprint × 10 sprints).

### Epic 12: Frontend Greenfield (Sprints 15-18)

#### [REFACTOR-04-001] Create admin-face project scaffold from 31-eva-faces
**Sprint**: REFACTOR-S15 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Pattern Source: `31-eva-faces/admin-face/`  
Target: `output/admin-face/` (NEW PROJECT)

Tasks:
1. Copy 31-eva-faces/admin-face project structure (NOT port EVA-JP-v1.2 admin UI)
2. Update package.json: dependencies (React 19, Fluent UI v9, Vite), scripts
3. Configure Vite: vite.config.ts with dev server, build optimizations
4. Setup Fluent UI v9: FluentProvider, theme configuration
5. Copy 31-eva-faces/shared: hooks (useAuth, useActingSession), utils (api-client), types, layouts

Acceptance:
- [ ] `npm run dev` starts dev server on port 3000
- [ ] `npm run build` produces optimized dist/ bundle
- [ ] Fluent UI v9 components render (test with sample Button)
- [ ] EVA-STORY tags configured (admin-face project initialization)

#### [REFACTOR-04-002] Build admin user management page using 31-eva-faces patterns
**Sprint**: REFACTOR-S15 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Pattern Source: `31-eva-faces/admin-face/src/pages/UserManagement.tsx`  
Target: `output/admin-face/src/pages/Users.tsx` (NEW FILE)

Tasks:
1. Copy UserManagement pattern from 31-eva-faces (NOT port EVA-JP-v1.2 Users.tsx)
2. Build with React 19 + Fluent UI v9:
   - `<Button appearance="primary">` (NOT v8 PrimaryButton)
   - `<DataGrid>` for user list (NOT v8 DetailsList)
   - `<Dialog>` for CRUD forms
3. API calls: Use copied api-client from 31-eva-faces/shared/utils
4. Auth: Use copied useActingSession hook (H1 handshake)
5. Write tests: `tests/pages/Users.test.tsx` using Vitest + Testing Library patterns from 31-eva-faces

Acceptance:
- [ ] User list renders with DataGrid
- [ ] CRUD operations work (create, read, update, delete via API)
- [ ] Tests pass (Vitest >= 80% coverage)
- [ ] MTI >= 70 (EVA-STORY: REFACTOR-04-002 tags)

...

**Note**: Stories [REFACTOR-04-003] through [REFACTOR-04-080] follow same pattern using 31-eva-faces patterns.  
Total: 80 frontend Greenfield stories (20 stories/sprint × 4 sprints).

### Epic 13: Data Layer Setup (Sprints 19-20)

#### [REFACTOR-05-001] Design Cosmos containers schema (Greenfield)
**Sprint**: REFACTOR-S19 | **Size**: M | **Status**: planned | **Assignee**: @agent:execution-agent

Database: `marco-sandbox-cosmos` (existing, zero new cost)  
Target: NEW container schemas (NOT ported from EVA-JP-v1.2 legacy schema)

Tasks:
1. Design clean Cosmos containers optimized for Greenfield use cases:
   - `users`: partition_key=/user_id, fields: id, email, roles, preferences, created_at
   - `sessions`: partition_key=/session_id, TTL=86400 (24h auto-expire), fields: id, user_id, token, expires_at
   - `documents`: partition_key=/user_id, fields: id, filename, storage_path, uploaded_by, metadata, created_at
   - `chat_threads`: partition_key=/user_id, fields: id, thread_id, messages[], created_at, updated_at
2. Design partition keys optimized for query patterns (NOT legacy EVA-JP-v1.2 keys)
3. Add TTL policies for ephemeral data (sessions: 24h, temp files: 1h)
4. Write Cosmos SDK client: `db/cosmos_client.py` with async operations

Acceptance:
- [ ] Container schemas documented in `docs/data-model.md`
- [ ] Partition key strategy reviewed (query efficiency)
- [ ] TTL policies tested (dev environment)
- [ ] EVA-STORY tags: REFACTOR-05-001

#### [REFACTOR-05-002] Implement Cosmos repository pattern
**Sprint**: REFACTOR-S19 | **Size**: L | **Status**: planned | **Assignee**: @agent:execution-agent

Pattern: Abstract data access with repository classes (NOT direct Cosmos SDK calls)

Tasks:
1. Create repository base class: `db/repository_base.py` (generic CRUD operations)
2. Implement specific repositories:
   - `UserRepository`: create_user, get_user, update_user, delete_user, list_users
   - `SessionRepository`: create_session, get_session, validate_session (with TTL check)
   - `DocumentRepository`: create_document, get_document, list_user_documents, delete_document
   - `ChatRepository`: create_thread, get_thread, add_message, list_user_threads
3. Use async/await throughout (NOT blocking I/O like EVA-JP-v1.2)
4. Add in-memory cache: Python `cachetools` for frequently accessed data (user profiles, session validation)
5. Write tests: `tests/db/test_repositories.py` with mock Cosmos client

Acceptance:
- [ ] All repositories implement CRUD operations
- [ ] Async operations tested (asyncio.run in pytest)
- [ ] Cache hit rate >= 80% for user profile queries
- [ ] MTI >= 70

...

**Note**: Stories [REFACTOR-05-003] through [REFACTOR-05-060] follow same pattern.  
Total: 60 data layer setup stories (30 stories/sprint × 2 sprints).

---

## Phase 4: Validation & POC Demonstration (Sprint 23, Week 23)

### Objective
Verify feature parity with EVA-JP-v1.2, performance benchmarks, security gates, and quality thresholds before presenting POC.

### Epic 14: Feature Parity Validation

#### [REFACTOR-06-001] Validate feature parity with EVA-JP-v1.2
**Sprint**: REFACTOR-S23 | **Size**: M | **Status**: planned | **Assignee**: @agent:validation-agent

Script: `scripts/feature-parity-check.py`

Tasks:
1. Compare EVA-JP-v1.2 feature inventory vs Greenfield POC implemented features
2. Validate: All EVA-JP-v1.2 features exist in POC (implementation may differ)
3. Test user flows: Login → Chat → Search → Upload → Admin (E2E)
4. Performance comparison: Chat latency (p50, p95, p99) POC vs EVA-JP-v1.2
5. Generate parity report: `docs/feature-parity-report.md`

Acceptance:
- [ ] 100% feature coverage (all EVA-JP-v1.2 features exist in POC)
- [ ] Performance equal or better (p95 chat latency <= EVA-JP-v1.2 baseline)
- [ ] Report documents: Feature mapping (EVA-JP-v1.2 → POC), missing features (if any), performance benchmarks

#### [REFACTOR-06-002] Run E2E test suite on Greenfield POC
**Sprint**: REFACTOR-S23 | **Size**: L | **Status**: planned | **Assignee**: @agent:validation-agent

Framework: Playwright (patterns from 31-eva-faces)

Tasks:
1. Copy Playwright test patterns from 31-eva-faces/tests/e2e/
2. Build E2E tests for Greenfield POC critical flows:
   - User authentication: Login (H1 handshake via useActingSession) → Logout
   - Chat: Send message → Stream response → View history
   - Search: Query → Filter results → Pagination
   - Upload: Select file → Upload to Blob Storage → View status
   - Admin: Manage users (RBAC-protected) → View logs
3. Run tests against Greenfield POC deployment (staging environment)
4. Performance assertions: Response times (baseline from EVA-JP-v1.2)

Acceptance:
- [ ] All E2E tests pass on Greenfield POC
- [ ] Response times meet or exceed EVA-JP-v1.2 baseline (p95 chat latency <= 2s)
- [ ] Zero critical bugs (P0/P1)

### Epic 15: Quality Gates

#### [REFACTOR-06-003] Run Veritas audit on Greenfield POC
**Sprint**: REFACTOR-S23 | **Size**: M | **Status**: planned | **Assignee**: @agent:github-copilot

Command:
```bash
node src/cli.js audit --repo C:\AICOE\eva-foundry\53-refactor\output
```

Target Metrics (High-Quality POC like 51-ACA):
- MTI Score: >= 80 (vs EVA-JP-v1.2 baseline ~50)
- Test Coverage: >= 80% (pytest for backend, Vitest for frontend)
- Gaps: Zero missing implementation for planned features
- Quality Gates: All pass (Veritas trust gates + custom gates)

Acceptance:
- [ ] MTI >= 80 (PASS - high-quality POC like 51-ACA)
- [ ] Test coverage >= 80% (PASS - backend pytest + frontend Vitest)
- [ ] Zero high-severity gaps (WARN on medium/low acceptable for POC)

#### [REFACTOR-06-004] Run security scans on Greenfield POC
**Sprint**: REFACTOR-S23 | **Size**: M | **Status**: planned | **Assignee**: @agent:validation-agent

Scans:
1. **OWASP ZAP**: Web application security testing (XSS, CSRF, SQL injection)
2. **Bandit**: Python security linter (backend routers)
3. **npm audit**: Node.js dependency vulnerabilities (frontend packages)
4. **Trivy**: Container image scanning (Docker images for App Service deployment)
5. **Secrets**: Git history scan for leaked secrets (no hardcoded keys in code)

Acceptance:
- [ ] Zero high-severity vulnerabilities (CRITICAL for POC)
- [ ] Zero secrets in code or Git history (all secrets in Key Vault)
- [ ] All dependencies patched to latest stable versions

### Epic 16: Performance & Cost Validation

#### [REFACTOR-06-005] Run performance benchmarks on Greenfield POC
**Sprint**: REFACTOR-S23 | **Size**: M | **Status**: planned | **Assignee**: @agent:validation-agent

Benchmarks (Locust or k6):
1. Load test: Chat endpoint 100 concurrent users, 10 minutes sustained
2. Latency: P50, P95, P99 for all endpoints (chat, search, upload)
3. Throughput: Requests per second (Greenfield POC vs EVA-JP-v1.2 baseline)
4. Resource utilization: CPU, memory (App Insights monitoring)

Target Performance:
- Chat latency p95 <= 2s (EVA-JP-v1.2 baseline: ~2.5s)
- Search latency p95 <= 1s (EVA-JP-v1.2 baseline: ~1.5s)
- Upload throughput >= 10 files/minute

Acceptance:
- [ ] Latency P95 meets or beats EVA-JP-v1.2 baseline
- [ ] Throughput meets or beats EVA-JP-v1.2 baseline
- [ ] Resource usage <= 80% (CPU, memory on App Service Plan)

#### [REFACTOR-06-006] Calculate infrastructure cost
**Sprint**: REFACTOR-S23 | **Size**: S | **Status**: planned | **Assignee**: @agent:github-copilot

Infrastructure Cost (POC Deployment):

**Uses Existing Resources** (Zero new cost):
1. **Cosmos DB**: marco-sandbox-cosmos (existing, $0 new cost)
2. **App Service Plan**: marco-sandbox-asp-backend (existing Linux plan, $0 new cost for adding new App Service)
3. **Storage**: marcosand20260203 (existing, container "refactor-uploads" $0 new cost)
4. **Key Vault**: marcosandkv20260203 (existing, $0 new cost)
5. **App Insights**: marco-sandbox-appinsights (existing, $0 new cost)
6. **Container Registry**: marcosandacr20260203.azurecr.io (existing, $0 new cost)

**Optional New Resources** (if needed beyond POC):
- Postgres Flexible Server B1ms: ~$30/month (if relational model critical)
- Redis Basic: ~$16/month (if in-memory cache insufficient)

**Total POC Cost**: **$0/month** (uses existing sandbox resources only)

Acceptance:
Acceptance:
- [ ] Cost breakdown documented in `docs/cost-analysis.md`
- [ ] Zero new infrastructure required for POC demonstration
- [ ] Optional upgrades documented for production consideration

---

## Backlog (Future Enhancements Beyond POC)

### Epic 17: Production-Ready Features (Post-POC)

**Context**: These stories are BEYOND the Greenfield POC scope. The POC demonstrates high-quality patterns and achieves feature parity with EVA-JP-v1.2. These are optional production enhancements.

- [ ] [REFACTOR-07-001] Add multi-tenant support (isolated data per tenant via Cosmos partition keys)
- [ ] [REFACTOR-07-002] Implement advanced rate limiting (Redis-based per-user quotas)
- [ ] [REFACTOR-07-003] Add caching layer (Redis distributed cache + CDN for static assets)
- [ ] [REFACTOR-07-004] Horizontal scaling (multiple App Service instances with load balancer)
- [ ] [REFACTOR-07-005] Add GraphQL API (alternative to REST for flexible queries)
- [ ] [REFACTOR-07-006] Implement advanced real-time features (WebSocket server for collaboration)
- [ ] [REFACTOR-07-007] Add mobile app (React Native reusing backend API)
- [ ] [REFACTOR-07-008] Production-grade DR (multi-region deployment, automatic failover)
- [ ] [REFACTOR-07-009] Advanced observability (distributed tracing with Jaeger, custom dashboards)

---

## Appendix A: Story Size Guidelines

**XS** (1-2 hours):
- Simple config changes (update .env, add feature flag)
- Documentation updates (README, inline comments)
- Minor bug fixes (typos, small logic errors)

**S** (4-6 hours):
- Small feature additions (add query parameter, new field)
- Copy pattern from source project (31-eva-faces hook, 33-eva-brain-v2 router)
- Add unit tests (single function or component)

**M** (1-2 days):
- Build single module from scratch using patterns (router, page, repository)
- Write integration tests (API endpoint with mock dependencies)
- Implement observability patterns (51-ACA telemetry for one service)

**L** (3-5 days):
- Build complex component with multiple dependencies (chat interface with streaming)
- Implement data layer patterns (repository with cache, async operations)
- Feature with multiple endpoints and tests (full CRUD with validation)

**XL** (1-2 weeks):
- Complete subsystem Greenfield build (entire admin-face with 10 pages)
- Multi-epic orchestration (backend + frontend + data layer for one feature)
- Cross-cutting concerns (authentication, RBAC, observability across all services)

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
