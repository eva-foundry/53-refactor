# Project 53: EVA Refactor Factory

**AI-Driven Legacy Modernization at Scale**

**Type**: Standalone High-Quality POC  
**Development**: GitHub Codespaces (180 hrs available)  
**Infrastructure**: Use existing marco* resources in 22-rg-sandbox (no new resources)  
**Strategy**: Greenfield rewrite leveraging Veritas-Model-ADO workflow  
**ADO Project**: **EVA-Refactor** (Dedicated, not shared with eva-poc) — https://dev.azure.com/marcopresta/EVA-Refactor  

## Vision

Project 53-refactor is a **standalone application POC** that demonstrates autonomous refactoring capabilities at scale. It's not a production replacement of EVA-JP-v1.2, but a parallel proof-of-concept that:
- Scans existing legacy codebases (EVA-JP-v1.2) to understand as-is architecture
- Generates comprehensive modernization plans via AI
- Executes Greenfield rewrite autonomously through GitHub Actions workflows
- Validates quality via Veritas gates (MTI >= 80, test coverage >= 80%)
- Provides full traceability via Evidence Layer integration
- Showcases the power of Veritas-Model-ADO workflow for future EVA projects

## The Problem

Traditional application modernization is:
- **Manual**: Months of architecture reviews, gap analysis, and planning
- **Error-prone**: Inconsistent patterns, missed dependencies, incomplete documentation
- **Expensive**: Senior architects analyze code line-by-line
- **Risky**: Feature parity gaps discovered late in migration

## The Solution

**Full DPDCA Automation**:
```
EVA-JP-v1.2 (Legacy)
  |
  v
[1] DISCOVER: Veritas scans source code (as-is architecture)
  - Services, endpoints, screens, containers → Data Model
  - Dependency graph, API contracts, data flows
  - Technical debt, anti-patterns, security issues
  |
  v
[2] PLAN: AI generates modernization WBS  
  - Technology stack migration (React → React 19, FastAPI → FastAPI + Agents SDK)
  - Architecture patterns (monolith → microservices, Cosmos → Postgres + Redis)
  - WBS with epics, features, stories (500+ stories automatically generated)
  - Risk assessment, effort estimation, sprint planning
  |
  v
[3] DO: Autonomous execution via GitHub Actions
  - Seed WBS to data model via seed-from-plan.py
  - ADO sync creates work items
  - GitHub Actions workflow picks up stories (sprint-agent.yml)
  - Agent reads old code via data model, generates new code with patterns
  - Iterative sprints: Plan → Execute → Test → Deploy
  |
  v
[4] CHECK: Veritas validates refactor
  - Feature parity: Old vs new API compatibility matrix
  - Quality gates: Test coverage >= 80%, MTI >= 70
  - Performance: Latency, throughput, cost comparison
  - Security: OWASP Top 10, dependency audit, secrets scan
  |
  v
[5] ACT: Evidence and continuous improvement
  - Evidence receipts for every story (code changes, tests, deployment)
  - MTI tracking: refactored modules vs legacy modules
  - Automated rollback if quality gates fail
  - Loop: Next sprint starts automatically
  |
  v
EVA-Refactored (Modern)
```

## First Target: EVA-JP-v1.2

### As-Is Architecture (Legacy)
**Location**: `C:\AICOE\EVA-JP-v1.2`

**Tech Stack**:
- **Frontend**: React 18 + Fluent UI v8/v9 + Vite + TypeScript
- **Backend**: FastAPI (Python) + Azure OpenAI + Azure AI Search
- **Storage**: Azure Blob Storage + Cosmos DB
- **Functions**: Azure Functions (enrichment pipeline)
- **Scale**: ~2500 lines in app.py (monolithic)
- **Age**: 2+ years production use
- **Quality**: MTI unknown, test coverage ~40%, tech debt moderate

### To-Be Architecture (Greenfield POC)
**Output Location**: `C:\AICOE\eva-foundry\53-refactor\output`

**Tech Stack** (Clean Slate - No Legacy):
- **Frontend**: React 19 + Fluent UI v9 + Vite + TypeScript
  - **3-face architecture**: admin-face, chat-face, portal-face (inspired by 31-eva-faces patterns)
  - **Shared components**: Copy from `C:\AICOE\eva-foundry\31-eva-faces\shared` (hooks, utils, types, layouts)
  - **State management**: Zustand + React Query (proven patterns from 31-eva-faces)
  - **Testing**: Vitest + Testing Library + Playwright E2E
- **Backend**: FastAPI + Microsoft Agent Framework + Azure AI Foundry
  - **Agentic RAG**: Agent Framework from day 1 (no custom approaches/ to port)
  - **Modular routers**: Clean separation (chat, search, upload, admin) from day 1
  - **Structured outputs**: Pydantic v2 strict typing + OpenAPI auto-docs
  - **Observability**: OpenTelemetry + Application Insights integration (patterns from 51-ACA)
- **Data Layer**: Azure Postgres Flexible Server + Azure Redis Cache
  - **Postgres**: Relational data, JSONB for semi-structured, connection pooling
  - **Redis**: Session state, rate limiting, pub/sub for real-time
  - **ORM**: SQLAlchemy async with asyncpg driver
- **Infrastructure**: Use existing marco* resources in 22-rg-sandbox
  - **Postgres**: `marco-eva-postgres.postgres.database.azure.com` (existing)
  - **Redis**: `marco-eva-cache.redis.cache.windows.net` (existing)
  - **Container Apps**: Deploy to `marco-containerenv` (existing environment)
  - **Storage**: `marcoeva` storage account (existing)
  - **Key Vault**: `marco-eva-kv` (existing)
  - **App Insights**: `marco-eva-appinsights` (existing)
  - **No new infrastructure**: Configure via .env only
- **Development**: GitHub Codespaces (180 hrs) + local Docker backup
- **Quality**: MTI >= 80 (vs EVA-JP-v1.2 baseline ~50), test coverage >= 80%, E2E tests

## Migration Strategy

### **Selected: Greenfield Rewrite (3 months, High-Quality POC)**

### **Selected: Greenfield Rewrite (3 months, High-Quality POC)**

**Approach**: Build standalone application from scratch using proven patterns from 31-eva-faces + 33-eva-brain-v2, implement EVA-JP-v1.2 feature set with modern architecture, deploy to existing Azure infrastructure.

**Why Greenfield**:
- **Clean slate**: No legacy technical debt, modern architecture from day 1
- **Faster**: 3 months vs 6 months incremental (no coordination overhead)
- **Higher quality**: 80%+ test coverage target, MTI >= 80 (vs baseline ~50)
- **Reference POC**: Demonstrates Veritas-Model-ADO workflow at scale for future EVA projects
- **Autonomous showcase**: Full DPDCA automation with agent-driven development
- **Reuse existing infra**: No new Azure resources, use marco* resources in 22-rg-sandbox

**Risk Mitigation**:
- **Feature parity tracking**: Automated API contract comparison (OpenAPI diff old vs new)
- **Parallel deployment**: Both systems run side-by-side during validation phase
- **Veritas quality gates**: MTI >= 70 enforced at every story completion (blocks merge if fail)
- **Evidence-driven**: Immutable audit trail for all changes via Evidence Layer
- **Rollback capability**: Can revert to EVA-JP-v1.2 reference within 15 minutes

**NOT Production Replacement**: This is a standalone POC to demonstrate autonomous modernization capabilities, not a production cutover from EVA-JP-v1.2.

## Architecture

### Frontend (3-Face React 19 Application)

**Structure**:
```
output/
├── admin-face/          # Admin portal
│   ├── src/
│   │   ├── pages/       # User mgmt, config, logs
│   │   ├── components/  # Admin-specific UI
│   │   └── shared/      # Copy from 31-eva-faces/shared
│   ├── package.json
│   └── vite.config.ts
├── chat-face/           # RAG chat interface
│   ├── src/
│   │   ├── pages/       # Chat, history, settings
│   │   ├── components/  # Chat-specific UI (MessageList, InputBox)
│   │   └── shared/      # Copy from 31-eva-faces/shared
│   ├── package.json
│   └── vite.config.ts
└── portal-face/         # Public landing page
    ├── src/
    │   ├── pages/       # Home, docs, auth
    │   ├── components/  # Public-facing UI
    │   └── shared/      # Copy from 31-eva-faces/shared
    ├── package.json
    └── vite.config.ts
```

**Shared Components** (copy from `31-eva-faces/shared`):
- `hooks/`: useActingSession, useAuth, useFetch, useLocalStorage
- `utils/`: formatters, validators, api-client
- `types/`: TypeScript definitions (User, Session, ApiResponse)
- `layouts/`: AppLayout, AuthLayout, ErrorBoundary

**Stack**:
- React 19 (concurrent rendering, improved Suspense, Server Components ready)
- Fluent UI v9 (DataGrid, Accordion, Button, Input, Dialog)
- Vite (ESBuild-powered dev server, HMR, optimized builds)
- Zustand (state management) + React Query (API caching)
- Vitest + Testing Library (unit tests) + Playwright (E2E)

### Backend (FastAPI + Agent Framework)

**Structure**:
```
output/
└── backend/
    ├── app/
    │   ├── main.py              # FastAPI app entry point
    │   ├── routers/
    │   │   ├── chat.py          # POST /chat, /chat/stream
    │   │   ├── search.py        # GET /search, /search/semantic
    │   │   ├── upload.py        # POST /upload, GET /upload/status
    │   │   └── admin.py         # Admin APIs (users, config, logs)
    │   ├── agents/              # Agent Framework agents
    │   │   ├── rag_agent.py     # RAG orchestration agent
    │   │   ├── search_agent.py  # Azure AI Search agent
    │   │   └── summarize_agent.py # Document summarization agent
    │   ├── models/              # Pydantic v2 schemas
    │   │   ├── chat.py          # ChatRequest, ChatResponse
    │   │   ├── search.py        # SearchRequest, SearchResponse
    │   │   └── upload.py        # UploadRequest, UploadResponse
    │   ├── services/            # Business logic
    │   │   ├── postgres.py      # Database ORM (SQLAlchemy)
    │   │   ├── redis.py         # Cache manager
    │   │   └── storage.py       # Azure Blob SDK
    │   └── middleware/
    │       ├── auth.py          # RBAC middleware (from 28-rbac)
    │       ├── telemetry.py     # OpenTelemetry instrumentation
    │       └── rate_limit.py    # Redis-based rate limiting
    ├── tests/
    │   ├── test_routers/        # Route unit tests
    │   ├── test_agents/         # Agent unit tests
    │   └── test_integration/    # Integration tests
    ├── requirements.txt
    ├── Dockerfile
    └── docker-compose.yml       # Local dev (backend + Postgres + Redis)
```

**Stack**:
- FastAPI (AsyncIO, OpenAPI auto-docs, Pydantic validation)
- Microsoft Agent Framework (agentic RAG from day 1, no custom approaches/)
- Pydantic v2 (strict typing, validation, OpenAPI schema generation)
- SQLAlchemy 2.0 async (asyncpg driver for Postgres)
- Azure SDKs (OpenAI, AI Search, Blob Storage, Key Vault)
- OpenTelemetry + Application Insights (patterns from 51-ACA)

### Infrastructure (Actual 22-rg-sandbox Resources from Inventory 2026-02-13)

**EsDAICoE-Sandbox marco* Resources** (ZERO NEW INFRASTRUCTURE COST):
- **Database**: `marco-sandbox-cosmos` (DocumentDB, canadacentral)
  - **Option A** (Recommended for POC): Use existing Cosmos DB (zero new cost)
  - **Option B**: Create small Postgres Flexible Server if relational model critical (~$30/mo)
  - Connection: Via Key Vault (`marcosandkv20260203`)
- **Cache**: Not available in sandbox
  - **Option A** (Recommended for POC): In-memory cache (Python `cachetools`)
  - **Option B**: Add Azure Redis Cache Basic (~$16/mo)
- **Compute**: Deploy to existing App Service Plan
  - App Service Plan: `marco-sandbox-asp-backend` (Linux, canadacentral) - existing, zero new cost
  - New App Service: `marco-refactor-backend` (add to existing plan)
  - **Alternative**: Container Apps (would need new environment ~$50/mo base)
- **Container Registry**: `marcosandacr20260203.azurecr.io` (Basic, canadacentral)
  - Push image: `marcosandacr20260203.azurecr.io/refactor-backend:latest`
- **Storage**: `marcosand20260203` (Standard_LRS, StorageV2, canadacentral)
  - New container: `refactor-uploads`
  - Blob lifecycle: Hot → Cool after 30 days
- **Key Vault**: `marcosandkv20260203` (canadacentral)
  - Secrets: Cosmos connection, Storage keys, OpenAI keys, AI Search keys
  - Access: App Service managed identity
- **App Insights**: `marco-sandbox-appinsights` (canadacentral)
  - Instrumentation key: Already configured
  - Tags: `Component=Monitoring, Environment=marco-sandbox, Project=EVA-JP`
- **OpenAI**: `marco-sandbox-openai-v2` (S0, canadaeast)
  - Use existing models (check with `az cognitiveservices account deployment list`)
- **AI Search**: `marco-sandbox-search` (canadacentral)
  - Existing search service for RAG vector search

**Configuration** (.env for local dev, Key Vault for prod):
```bash
# Cosmos DB (existing marco-sandbox-cosmos)
COSMOS_ENDPOINT=<from-marcosandkv20260203>
COSMOS_KEY=<from-marcosandkv20260203>
COSMOS_DATABASE=refactor_poc

# Storage (existing marcosand20260203)
AZURE_STORAGE_ACCOUNT=marcosand20260203
AZURE_STORAGE_KEY=<from-marcosandkv20260203>
AZURE_STORAGE_CONTAINER=refactor-uploads

# Azure OpenAI (existing marco-sandbox-openai-v2)
AZURE_OPENAI_ENDPOINT=<from-marcosandkv20260203>
AZURE_OPENAI_KEY=<from-marcosandkv20260203>
AZURE_OPENAI_DEPLOYMENT=gpt-4  # Verify with: az cognitiveservices account deployment list

# Azure AI Search (existing marco-sandbox-search)
AZURE_SEARCH_ENDPOINT=<from-marcosandkv20260203>
AZURE_SEARCH_KEY=<from-marcosandkv20260203>
AZURE_SEARCH_KEY=<from-marcosandkv20260203>
AZURE_SEARCH_INDEX=refactor-docs

# App Insights (existing marco-sandbox-appinsights)
APPINSIGHTS_INSTRUMENTATION_KEY=<from-marcosandkv20260203>
APPINSIGHTS_CONNECTION_STRING=<from-marcosandkv20260203>
```

**Deployment** (ZERO new infrastructure cost - use existing resources):
```bash
# Backend: Deploy to existing App Service Plan (Recommended: zero new cost)
az webapp create \
  --name marco-refactor-backend \
  --plan marco-sandbox-asp-backend \
  --resource-group EsDAICoE-Sandbox \
  --deployment-container-image-name marcosandacr20260203.azurecr.io/refactor-backend:latest

# Frontend: Static Web App Free tier OR deploy to existing App Service
az staticwebapp create --name marco-refactor-frontend --sku Free

# Database: Use existing marco-sandbox-cosmos (zero new cost)
# OR create new Cosmos container: az cosmosdb sql container create --name refactor_poc
```

**Total New Monthly Cost**: **~$0** (uses existing App Service Plan, existing Cosmos DB, Static Web App Free tier)

## Autonomous Execution Workflow

### GitHub Actions: `refactor-workflow.yml`

```yaml
name: Autonomous Refactor Execution (Greenfield)
on:
  workflow_dispatch:
    inputs:
      sprint_id:
        description: 'Sprint ID (e.g., REFACTOR-S01)'
        required: true
  schedule:
    - cron: '0 9 * * 1'  # Every Monday 9 AM (sprint start)

jobs:
  discover:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Veritas Discovery on EVA-JP-v1.2  
        run: |
          # Scan legacy system to understand as-is architecture
          node scripts/as-is-scanner.js --source C:\AICOE\EVA-JP-v1.2
      - name: Upload Discovery Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: discovery-results
          path: .eva/discovery.json
  
  plan:
    needs: discover
    runs-on: ubuntu-latest
    steps:
      - name: Generate Greenfield Plan (AI)
        run: |
          # AI analyzes legacy and generates Greenfield WBS
          python scripts/migration-planner.py --strategy greenfield --output PLAN.md
      - name: Seed WBS to Data Model
        run: |
          # Load 500+ stories to data model
          python scripts/seed-from-plan.py --plan PLAN.md --project 53-refactor
      - name: ADO Bidirectional Sync (Push Mode)
        run: |
          # Create ADO work items for stories
          pwsh scripts/ado-bidirectional-sync.ps1 -Mode Push -Project 53-refactor
      - name: Generate Sprint Manifest
        run: |
          # Filter WBS by sprint, order by dependencies
          python scripts/gen-sprint-manifest.py --sprint ${{ inputs.sprint_id }} --output .github/sprints/manifest.json
      - name: Output Stories for Matrix
        id: stories
        run: echo "stories=$(cat .github/sprints/manifest.json | jq -c .stories)" >> $GITHUB_OUTPUT
    outputs:
      stories: ${{ steps.stories.outputs.stories }}
  
  execute:
    needs: plan
    runs-on: ubuntu-latest
    strategy:
      matrix:
        story: ${{ fromJson(needs.plan.outputs.stories) }}
      max-parallel: 5  # Parallel execution of independent stories
    steps:
      - name: Execute Story ${{ matrix.story.id }} (Greenfield)
        uses: ./.github/workflows/sprint-agent.yml
        with:
          story_id: ${{ matrix.story.id }}
          legacy_source: C:\AICOE\EVA-JP-v1.2  # Reference for feature parity
          target_repo: output/  # Greenfield code (no porting, write from scratch)
          use_patterns_from: 31-eva-faces,33-eva-brain-v2  # Copy proven patterns
  
  validate:
    needs: execute
    runs-on: ubuntu-latest
    steps:
      - name: Run Veritas Audit (Greenfield)
        run: |
          # Audit refactored code quality
          node scripts/veritas-audit.js --repo output/ --warn-only
      - name: Feature Parity Check (vs Legacy)
        run: |
          # Compare OpenAPI schemas: old vs new
          python scripts/feature-parity-test.py --old EVA-JP-v1.2 --new output/
      - name: Quality Gates (Block if Fail)
        run: |
          pytest output/tests/ --cov=output --cov-fail-under=80
          if [ $(cat .eva/trust.json | jq .mti) -lt 70 ]; then exit 1; fi
      - name: Deploy to Azure (Existing Infrastructure)
        run: |
          # Deploy to marco* resources in 22-rg-sandbox
          az containerapp update --name marco-refactor-backend --image marcoeva.azurecr.io/refactor-backend:${{ github.sha }}
          az staticwebapp deploy --name marco-refactor-frontend --app-location output/
```

## Agents (GitHub Copilot Agents)

### Discovery Agent (`agents/discovery-agent.yml`)
**Purpose**: Scan EVA-JP-v1.2 to understand as-is architecture (for feature parity reference only, NOT for porting)

**Tasks**:
- Parse `app/backend/app.py` → Extract FastAPI routes, Pydantic models, business logic patterns
- Parse `app/frontend/src/` → Extract React components, hooks, API calls
- Parse `infra/` → Extract Azure resources (Cosmos, Blob, Functions, App Service)
- Build dependency graph: screens → endpoints → containers
- Identify feature set: Chat (RAG), Search (semantic), Upload (documents), Admin (users)
- Output: POST to Data Model (services, endpoints, screens, containers)

**Outputs**:
- `.eva/discovery.json`: As-is architecture snapshot (JSON)
- Data Model records: 4 services, 50+ endpoints, 80+ screens, 10+ containers
- `docs/as-is-feature-set.md`: Feature list for parity tracking

### Planning Agent (`agents/planning-agent.yml`)
**Purpose**: Generate Greenfield WBS with 500+ stories using AI

**Tasks**:
- Query Data Model: GET /model/services/, /model/endpoints/, /model/screens/
- Analyze feature set: What does EVA-JP-v1.2 do? (Chat, Search, Upload, Admin)
- Recommend tech stack: React 19 + Agent Framework + Postgres + Redis (Greenfield choices)
- Generate WBS categories:
  - Backend Greenfield (100 stories): Build FastAPI routers from scratch with Agent Framework
  - Frontend Greenfield (80 stories): Build 3-face React 19 app, copy patterns from 31-eva-faces/shared
  - Data Layer Setup (60 stories): Postgres schema design, Redis caching, SQLAlchemy models
  - Observability (40 stories): OpenTelemetry, Application Insights, dashboards (51-ACA patterns)
  - Security (30 stories): RBAC (28-rbac), Key Vault, managed identities
  - Testing (120 stories): Unit (Vitest/pytest), integration, E2E (Playwright)
  - Documentation (70 stories): OpenAPI, architecture diagrams, runbooks
- Estimate effort: Size each story (XS/S/M/L), assign sprints (20 sprints total)
- Output: `PLAN.md` with 500+ stories

**AI Prompt Example**:
```
Given EVA-JP-v1.2 feature set (Chat RAG, Semantic Search, Document Upload, Admin Portal),
generate Greenfield WBS for building standalone POC with React 19 + Agent Framework + Postgres.
DO NOT port code. Generate stories for writing new code from scratch using patterns from:
- 31-eva-faces/shared (frontend hooks, utils, types)
- 33-eva-brain-v2 (Agent Framework RAG patterns)
- 28-rbac (RBAC middleware)
- 51-ACA (Application Insights telemetry patterns)

Output 500+ stories organized by epic, with sprint allocation (20 sprints).
```

### Execution Agent (`agents/execution-agent.yml`)
**Purpose**: Write Greenfield code for each story (NO PORTING from EVA-JP-v1.2)

**Tasks**:
- Read story from WBS: GET /model/wbs/REFACTOR-03-001
- Understand requirement: E.g., "Create chat router for POST /chat endpoint"
- Reference patterns (NOT port code):
  - 31-eva-faces/shared: Copy useAuth hook, api-client utils, TypeScript types
  - 33-eva-brain-v2: Copy Agent Framework RAG agent structure
  - 28-rbac: Copy RBAC middleware pattern
  - 51-ACA: Copy Application Insights telemetry pattern
- Write new code from scratch: `output/backend/app/routers/chat.py` (FastAPI + Agent Framework)
- Write tests: `output/backend/tests/test_routers/test_chat.py` (pytest, 80%+ coverage target)
- Tag code with EVA-STORY: `# EVA-STORY: REFACTOR-03-001`
- Create PR: Title "feat(REFACTOR-03-001): Create chat router", body includes acceptance criteria checklist

**NOT Allowed**:
- Copying EVA-JP-v1.2 code directly (it's legacy with technical debt)
- Porting monolithic app.py structure (we want modular routers)
- Using Cosmos DB SDKs (we're using Postgres)

**Allowed**:
- Copying proven patterns from 31-eva-faces, 33-eva-brain-v2, 28-rbac, 51-ACA
- Referencing EVA-JP-v1.2 for feature parity (what should /chat do?)
- Using Agent Framework examples from Microsoft docs

### Validation Agent (`agents/validation-agent.yml`)
**Purpose**: Enforce quality gates before merging each story

**Quality Gates**:
1. **Test Coverage >= 80%**: `pytest --cov=output --cov-fail-under=80`
2. **MTI >= 70**: Veritas audit must pass (gap report clean)
3. **Feature Parity**: Compare OpenAPI schemas (old /chat vs new /chat - same request/response)
4. **Security**: Bandit scan (no high-severity issues), secrets scan (no leaked keys)
5. **Linting**: Ruff (Python), ESLint (TypeScript) - no errors

**Tasks**:
- Run test suite: pytest (backend), vitest (frontend), Playwright (E2E for critical flows)
- Run Veritas audit: `node scripts/veritas-audit.js --repo output/ --warn-only`
- Compare API contracts: `python scripts/feature-parity-test.py --old EVA-JP-v1.2 --new output/`
- Generate evidence receipt: POST /model/evidence/ with test results, coverage, MTI score
- Block merge if any gate fails: Comment on PR "Quality gate failed: MTI=65 (target 70)"

**Evidence Receipt Example**:
```json
{
  "story_id": "REFACTOR-03-001",
  "sprint_id": "REFACTOR-S05",
  "phase": "CHECK",
  "artifacts": {
    "files_changed": ["output/backend/app/routers/chat.py", "output/backend/tests/test_routers/test_chat.py"],
    "lines_added": 250,
    "test_result": "PASS",
    "coverage": 0.85,
    "mti_score": 74
  },
  "validation": {
    "test_coverage_gate": "PASS",
    "mti_gate": "PASS",
    "feature_parity_gate": "PASS",
    "security_gate": "PASS"
  }
}
```

## Key Scripts

### `scripts/as-is-scanner.js`
Scans EVA-JP-v1.2 and populates data model with as-is architecture:
```bash
node scripts/as-is-scanner.js --source C:\AICOE\EVA-JP-v1.2
# Outputs:
# - POST /model/services/ (frontend, backend, enrichment, functions)
# - POST /model/endpoints/ (FastAPI routes from app.py)
# - POST /model/screens/ (React components from app/frontend/src)
# - POST /model/containers/ (Cosmos containers, Blob containers)
# - POST /model/infrastructure/ (Azure resources from infra/)
```

### `scripts/migration-planner.py`
AI-generates Greenfield modernization WBS (NOT port plan, but build-from-scratch plan):
```bash
python scripts/migration-planner.py --strategy greenfield --output PLAN.md
# Reads: Data Model (as-is state for feature parity reference)
# Generates: PLAN.md with 500+ Greenfield stories
# Categories:
#   - Backend Greenfield (100 stories): FastAPI routers + Agent Framework agents from scratch
#   - Frontend Greenfield (80 stories): React 19 3-face app, copy 31-eva-faces/shared patterns
#   - Data Layer Setup (60 stories): Postgres schema, Redis caching, SQLAlchemy models
#   - Observability (40 stories): OpenTelemetry + App Insights (51-ACA patterns)
#   - Security Hardening (30 stories): RBAC (28-rbac), Key Vault, managed identities
#   - Testing & Validation (120 stories): Unit (pytest/vitest) + E2E (Playwright) >= 80% coverage
#   - Documentation (70 stories): OpenAPI, architecture diagrams, runbooks
```

### `scripts/seed-from-plan.py`
Seeds WBS to data model (reuse from 37-data-model):
```bash
python scripts/seed-from-plan.py --plan PLAN.md --project 53-refactor
# POST /model/wbs/ for each story
# Includes sprint, assignee, blockers from PLAN.md metadata
```

### `scripts/gen-sprint-manifest.py`
Generates sprint execution plan:
```bash
python scripts/gen-sprint-manifest.py --sprint REFACTOR-S01 --output .github/sprints/manifest.json
# Filters WBS by sprint, status=planned
# Orders stories by dependencies
# Generates SPRINT_MANIFEST for GitHub Actions
```

## Data Model Integration

### New Layers for Refactoring

**L33: `migrations`** (NEW)
```json
{
  "id": "REFACTOR-M001",
  "source_system": "EVA-JP-v1.2",
  "target_system": "53-refactor",
  "migration_type": "backend-decomposition",
  "source_files": ["app/backend/app.py:1-500"],
  "target_files": ["output/routers/chat.py:1-150"],
  "status": "completed",
  "feature_parity": true,
  "test_coverage": 0.85,
  "evidence_id": "REFACTOR-E001"
}
```

**L34: `refactor_decisions`** (NEW)
```json
{
  "id": "REFACTOR-D001",
  "decision": "Replace Cosmos DB with Postgres + Redis",
  "rationale": "Cost reduction (60%), better relational queries, Redis for session caching",
  "alternatives": ["Keep Cosmos", "Migrate to MongoDB"],
  "approved_by": "agent:planning-agent",
  "approved_at": "2026-03-02T14:30:00Z"
}
```

## Success Criteria (ACCEPTANCE.md)

### Phase 1: Discovery (Week 1)
- [ ] Veritas scan completes without errors
- [ ] Data Model populated: 4 services, 50+ endpoints, 80+ screens
- [ ] Dependency graph generated with zero broken links
- [ ] Technical debt report: categorized by severity
- [ ] MTI baseline: EVA-JP-v1.2 scored (target: >= 50)

### Phase 2: Planning (Week 2)
- [ ] PLAN.md generated with 500+ stories
- [ ] All stories have size estimation (XS/S/M/L)
- [ ] Effort estimated: total story points calculated
- [ ] Risk assessment: high-risk stories flagged
- [ ] Sprint plan: 10 sprints × 50 stories each

### Phase 3: Execution (Weeks 3-22, 20 sprints)
- [ ] Sprint 1-10: Backend decomposition (200 stories, 50% progress)
- [ ] Sprint 11-15: Frontend modularization (100 stories, 70% progress)
- [ ] Sprint 16-18: Data migration (80 stories, 90% progress)
- [ ] Sprint 19-20: Validation & documentation (120 stories, 100% progress)
- [ ] Quality gates passed: MTI >= 70 every sprint
- [ ] Test coverage: >= 80% for all refactored modules

### Phase 4: Validation (Week 23)
- [ ] Feature parity: 100% API compatibility with EVA-JP-v1.2
- [ ] Performance: Latency <= 100ms P95, throughput >= 1000 req/s
- [ ] Security: Zero OWASP Top 10 violations, secrets scanned
- [ ] Cost: Azure spend reduced by 40% (Cosmos → Postgres savings)
- [ ] MTI final: >= 80 (vs baseline 50, 60% improvement)

## Technology Choices

### Why React 19 + Fluent UI v9?
- Retain developer familiarity (React 18 → 19 minor upgrade)
- Fluent UI v9: Better performance, new components, improved accessibility
- Vite: Fast dev server, hot module replacement
- TypeScript: Type safety reduces bugs

### Why FastAPI + Microsoft Agent Framework?
- FastAPI: Async performance, OpenAPI auto-docs, Pydantic validation
- Agent Framework: Built for agentic RAG, replaces custom approaches/
- Observability: Native Azure Monitor + OpenTelemetry integration
- Scalability: Modular routers vs monolithic app.py

### Why Postgres + Redis?
- **Postgres**: Relational queries, JSONB for semi-structured data, 60% cost savings vs Cosmos
- **Redis**: Session caching, rate limiting, real-time features
- **Compatibility**: SQLAlchemy ORM supports both Cosmos and Postgres (incremental migration)

### Why Terraform?
- **State management**: Better than Bicep for multi-environment (dev/staging/prod)
- **Multi-cloud**: Future-proof for AWS/GCP if needed
- **Module reuse**: Import 22-rg-sandbox Terraform modules
- **Community**: Larger ecosystem, more examples

## Risks & Mitigations

### Risk 1: Feature Parity Gaps
**Likelihood**: High | **Impact**: Critical
**Mitigation**: 
- Feature parity tests run every sprint (automated)
- Parallel deployment: Old and new systems run side-by-side
- Traffic shadowing: 10% traffic to new system, compare responses
- Rollback plan: Keep old system for 3 months post-migration

### Risk 2: Dependency Integration Failures
**Likelihood**: Medium | **Impact**: High
**Mitigation**:
- Early integration tests: Postgres + Redis connectivity from Day 1
- Connection pooling: pgbouncer + redis-py connection pool
- Circuit breakers: Graceful degradation if Redis unavailable
- Schema migrations: Alembic for versioned Postgres schema changes

### Risk 3: Agent Hallucinations
**Likelihood**: Medium | **Impact**: Medium
**Mitigation**:
- Human-in-the-loop: PR review required for every story
- Veritas quality gates: Block merge if MTI < 70
- Test coverage enforcement: >= 80% or fail
- Agent prompt templates: Constrained to proven patterns from 31-eva-faces

### Risk 4: Schedule Overrun
**Likelihood**: High | **Impact**: Medium
**Mitigation**:
- Sprint buffer: 20% time allocated for blockers
- Parallel execution: Multiple stories run concurrently
- Adaptive planning: Re-estimate every 5 sprints
- Scope cut: Defer non-critical stories if needed

## Metrics & Observability

### Refactor Dashboard (38-ado-poc)
- **Progress**: Stories done / total (500+ total)
- **Velocity**: Story points per sprint (target: 50 points/week)
- **Quality**: MTI trend line (baseline 50 → target 80)
- **Cost**: Azure spend comparison (EVA-JP-v1.2 vs 53-refactor)
- **Performance**: Latency P50/P95/P99, throughput

### Evidence Collection (40-eva-control-plane)
- Every story completion → Evidence receipt
- Code changes: Lines added/removed, files touched
- Test results: Pass/fail, coverage %
- Deployment: Image tag, revision, timestamp
- Correlation: Sprint ID → Story ID → Commit SHA → Evidence ID

## Getting Started

### Prerequisites
- GitHub account with **180 hrs Codespaces available**
- VS Code with GitHub Copilot
- Access to Data Model API (37-data-model ACA endpoint)
- Access to ADO eva-poc project
- Access to `marco-sandbox-*` resources in **EsDAICoE-Sandbox** RG:
  - `marco-sandbox-cosmos` (database)
  - `marcosand20260203` (storage)
  - `marcosandkv20260203` (secrets)
  - `marco-sandbox-appinsights` (telemetry)
  - `marcosandacr20260203` (container registry)
  - `marco-sandbox-asp-backend` (App Service Plan for deployment)
- EVA-JP-v1.2 source code at `C:\AICOE\EVA-JP-v1.2` (for feature parity reference only)

### Bootstrap Project 53 (Greenfield)
```powershell
# Step 1: Launch GitHub Codespaces (or local with Docker)
# Clone: git clone https://github.com/eva-foundry/53-refactor.git
# Codespace auto-configures: Python 3.11, Node 20, Docker

# Step 2: Run discovery on EVA-JP-v1.2 (feature parity reference)
cd C:\AICOE\eva-foundry\53-refactor
node scripts/as-is-scanner.js --source C:\AICOE\EVA-JP-v1.2 --purpose reference

# Step 3: Generate Greenfield WBS with AI (500+ build-from-scratch stories)
python scripts/migration-planner.py --strategy greenfield --output PLAN.md

# Step 4: Seed WBS to data model + ADO sync (Push mode)
cd C:\AICOE\eva-foundry\37-data-model
python scripts/seed-from-plan.py --plan C:\AICOE\eva-foundry\53-refactor\PLAN.md --project 53-refactor

# Step 5: Copy shared patterns from 31-eva-faces
cp -r C:\AICOE\eva-foundry\31-eva-faces\shared C:\AICOE\eva-foundry\53-refactor\output\shared

# Step 6: Configure actual marco* resources in .env
cat > .env << EOF
# Actual marco* resources from EsDAICoE-Sandbox (inventory 2026-02-13)
COSMOS_ENDPOINT=https://marco-sandbox-cosmos.documents.azure.com:443/
COSMOS_KEY=<from-marcosandkv20260203>
COSMOS_DATABASE=refactor_poc
AZURE_STORAGE_ACCOUNT=marcosand20260203
AZURE_KEY_VAULT_NAME=marcosandkv20260203
APPINSIGHTS_CONNECTION_STRING=<from marco-sandbox-appinsights>
ACR_REGISTRY=marcosandacr20260203.azurecr.io
EOF

# Step 7: Trigger first Greenfield sprint (builds backend scaffold)
gh workflow run refactor-workflow.yml -f sprint_id=REFACTOR-S01

# Step 8: Monitor progress via 38-ado-poc dashboard
# Dashboard: https://dev.azure.com/marcopresta/eva-poc/_dashboards/dashboard/53-refactor
```

## Relationship to Other Projects

**Pattern Sources** (Copy from these proven implementations):
- **31-eva-faces/shared**: Frontend patterns (hooks: useAuth, useActingSession; utils: api-client, formatters; types: User, Session; layouts: AppLayout)
- **33-eva-brain-v2**: Backend patterns (Agent Framework RAG, multi-agent orchestration, FastAPI structuring)
- **28-rbac**: Security patterns (RBAC middleware for FastAPI, role-based authorization)
- **51-ACA**: Observability patterns (Application Insights telemetry, OpenTelemetry tracing)

**EVA Infrastructure**:
- **37-data-model**: Central repository for as-is + to-be state (Greenfield WBS, feature parity tracking)
- **38-ado-poc**: Orchestration plane (sprint execution, ADO sync Push mode)
- **40-eva-co (Greenfield Development)

1. **Week 1**: Complete discovery phase (scan EVA-JP-v1.2 for feature parity reference, as-is-scanner.js, Veritas audit)
2. **Week 2**: Generate Greenfield PLAN.md (500+ build-from-scratch stories using AI, seed to data model, ADO sync Push mode)
3. **Week 3-4**: Implement Greenfield scaffold (output/ structure, copy 31-eva-faces/shared, backend skeleton with FastAPI + Agent Framework)
4. **Week 5**: Execute Sprint 1 (10 Backend Greenfield stories: auth endpoints, user management, session handling)
5. **Week 6**: Execute Sprint 2 (10 Frontend Greenfield stories: admin-face scaffold, login page, dashboard shell)
6. **Week 7-24**: Execute Sprints 3-20 (autonomous Greenfield development: 380 stories across Backend, Frontend, Data Layer, Observability, Security, Testing)
7. **Week 25-26**: Final validation (feature parity tests vs EVA-JP-v1.2, MTI >= 80, test coverage >= 80%, evidence collection)
8. **Week 27**: Documentation + demo (architecture diagrams, deployment runbook, showcase POC to stakeholders)

**Note**: This is a **standalone POC demonstration** (NOT production replacement of EVA-JP-v1.2). Success = High-quality showcase of autonomous Greenfield development capabilities.
## Next Steps

1. **Week 1**: Complete discovery (as-is scanner, Veritas audit)
2. **Week 2**: Generate PLAN.md (500+ stories), seed to data model
3. **Week 3-4**: Implement agents (discovery, planning, execution, validation)
4. **Week 5**: Execute Sprint 1 (10 backend decomposition stories)
5. **Week 6**: Iterate on agent prompts based on Sprint 1 results
6. **Week 7-26**: Execute Sprints 2-20 (autonomous)
7. **Week 27**: Final validation, feature parity tests, production cutover

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

- **Project Lead**: GitHub Copilot Agent
- **Repository**: https://github.com/eva-foundry/53-refactor
- **Documentation**: https://github.com/eva-foundry/53-refactor/docs
- **Issues**: https://github.com/eva-foundry/53-refactor/issues
