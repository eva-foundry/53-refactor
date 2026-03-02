# Project 53: EVA Refactor Factory

**AI-Driven Legacy Modernization at Scale**

## Vision

Project 53-refactor is an autonomous refactoring factory that transforms legacy applications into modern, cloud-native architectures using the complete Veritas-Model-ADO workflow. It scans existing codebases, generates comprehensive modernization plans, and executes the refactor autonomously through GitHub Actions workflows with full traceability and quality gates.

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

### To-Be Architecture (Modern)
**Location**: `C:\AICOE\eva-foundry\31-eva-faces` (admin-face, chat-face, portal-face) + `C:\AICOE\eva-foundry\33-eva-brain-v2` (eva-brain-api)

**Tech Stack** (Proposed):
- **Frontend**: React 19 + Fluent UI v9 + Vite + TypeScript (retain)
  - Modular: 3 separate faces (admin, chat, portal) vs monolithic
  - Shared components via 43-eva-spark design system
  - Improved state management: Zustand + React Query
- **Backend**: FastAPI + Microsoft Agent Framework + Azure AI Foundry
  - Decompose monolithic app.py (2500 lines) → Modular routers
  - Agent-based RAG: Replace approaches/ with Agent Framework agents
  - Structured outputs: Pydantic v2 strict typing
  - Observability: OpenTelemetry + Application Insights
- **Storage**: Azure Postgres Flexible Server (replace Cosmos) + Azure Redis (caching)
- **Functions**: Refactor enrichment → Event-driven (Azure Event Grid + Dead Letter Queue)
- **IaC**: Bicep → Terraform (better state management, multi-cloud ready)
- **Security**: RBAC Layer 28, Key Vault integration, managed identities
- **Quality**: MTI >= 70, test coverage >= 80%, E2E tests with Playwright

### Migration Paths (AI-Recommended)

**Option 1: Incremental Refactor (Low Risk, 6 months)**
- Phase 1: Backend decomposition (app.py → 10 route modules)
- Phase 2: Frontend modularization (monolith → 3 faces)
- Phase 3: Data layer migration (Cosmos → Postgres + Redis)
- Phase 4: Observability upgrade (custom logs → OpenTelemetry)

**Option 2: Greenfield Rewrite (High Risk, 3 months)**
- Clone architecture from 31-eva-faces + 33-eva-brain-v2
- Port business logic module-by-module
- Run both systems in parallel (blue/green deployment)
- Cut over when feature parity confirmed

**Option 3: Hybrid (Medium Risk, 4 months)** [RECOMMENDED]
- Keep frontend React 18 (upgrade minor versions only)
- Refactor backend completely (app.py → Agent Framework agents)
- Migrate data incrementally (dual-write Cosmos + Postgres)
- Decommission Cosmos after validation

## Autonomous Execution Workflow

### GitHub Actions: `refactor-workflow.yml`

```yaml
name: Autonomous Refactor Execution
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
      - name: Run Veritas Discovery
        run: node scripts/as-is-scanner.js --source C:\AICOE\EVA-JP-v1.2
      - name: Upload Discovery Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: discovery-results
          path: .eva/discovery.json
  
  plan:
    needs: discover
    runs-on: ubuntu-latest
    steps:
      - name: Generate Migration Plan
        run: python scripts/migration-planner.py --strategy hybrid
      - name: Seed WBS to Data Model
        run: python scripts/seed-from-plan.py --sync-ado
      - name: Generate Sprint Manifest
        run: python scripts/gen-sprint-manifest.py --sprint ${{ inputs.sprint_id }}
  
  execute:
    needs: plan
    runs-on: ubuntu-latest
    strategy:
      matrix:
        story: ${{ fromJson(needs.plan.outputs.stories) }}
    steps:
      - name: Execute Story ${{ matrix.story.id }}
        uses: ./.github/workflows/sprint-agent.yml
        with:
          story_id: ${{ matrix.story.id }}
          legacy_source: C:\AICOE\EVA-JP-v1.2
          target_repo: 53-refactor/output
  
  validate:
    needs: execute
    runs-on: ubuntu-latest
    steps:
      - name: Run Veritas Audit
        run: node scripts/veritas-audit.js --warn-only
      - name: Feature Parity Check
        run: python scripts/feature-parity-test.py --old EVA-JP-v1.2 --new output
      - name: Quality Gates
        run: |
          pytest --cov=output --cov-fail-under=80
          if veritas_mti < 70; then exit 1; fi
```

## Agents

### 1. Discovery Agent (`agents/discovery-agent.yml`)
- Scans EVA-JP-v1.2 codebase
- Extracts services, endpoints, screens, containers
- Builds dependency graph
- Identifies technical debt
- Outputs: `.eva/discovery.json` + Data Model records

### 2. Planning Agent (`agents/planning-agent.yml`)
- Analyzes as-is state from Data Model
- Recommends technology stack migration
- Generates WBS with epics, features, stories
- Estimates effort and risk
- Outputs: `PLAN.md` with 500+ stories

### 3. Execution Agent (`agents/execution-agent.yml`)
- Reads old code via Data Model (endpoint schemas, business logic)
- Generates new code using patterns from 31-eva-faces, 33-eva-brain-v2
- Writes tests (pytest + Playwright)
- Creates pull request with evidence
- Tags code with EVA-STORY IDs

### 4. Validation Agent (`agents/validation-agent.yml`)
- Compares old vs new: API contracts, feature parity
- Runs test suite: unit, integration, E2E
- Calculates MTI score
- Generates evidence receipt
- Blocks merge if quality gates fail

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
AI-generates modernization WBS:
```bash
python scripts/migration-planner.py --strategy hybrid --output PLAN.md
# Reads: Data Model (as-is state)
# Generates: PLAN.md with 500+ stories
# Categories:
#   - Backend Decomposition (100 stories)
#   - Frontend Modularization (80 stories)
#   - Data Migration (60 stories)
#   - Observability (40 stories)
#   - Security Hardening (30 stories)
#   - Testing & Validation (120 stories)
#   - Documentation (70 stories)
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

### Risk 2: Data Migration Failures
**Likelihood**: Medium | **Impact**: High
**Mitigation**:
- Dual-write strategy: Write to both Cosmos and Postgres
- Read-only from Postgres for 2 weeks (validation period)
- Automated data reconciliation script
- Backup Cosmos data before migration

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
- VS Code with GitHub Copilot
- Access to Data Model API (37-data-model)
- Access to ADO eva-poc project
- Azure subscription (for deployment)
- EVA-JP-v1.2 source code at `C:\AICOE\EVA-JP-v1.2`

### Bootstrap Project 53
```powershell
# Step 1: Run Veritas discovery on EVA-JP-v1.2
cd C:\AICOE\eva-foundry\48-eva-veritas
node src/cli.js audit --repo C:\AICOE\EVA-JP-v1.2

# Step 2: Run as-is scanner (populates data model)
cd C:\AICOE\eva-foundry\53-refactor
node scripts/as-is-scanner.js --source C:\AICOE\EVA-JP-v1.2

# Step 3: Generate migration plan with AI
python scripts/migration-planner.py --strategy hybrid --output PLAN.md

# Step 4: Seed WBS to data model
cd C:\AICOE\eva-foundry\37-data-model
python scripts/seed-from-plan.py --plan C:\AICOE\eva-foundry\53-refactor\PLAN.md --project 53-refactor

# Step 5: Trigger first sprint (manual)
gh workflow run refactor-workflow.yml -f sprint_id=REFACTOR-S01

# Step 6: Monitor progress
# Open 38-ado-poc ADO Dashboard: https://dev.azure.com/marcopresta/eva-poc
```

## Relationship to Other Projects

- **31-eva-faces**: Frontend modernization target (3-face architecture)
- **33-eva-brain-v2**: Backend modernization target (Agent Framework patterns)
- **37-data-model**: Central repository for as-is + to-be state
- **38-ado-poc**: Orchestration plane (sprint execution, ADO sync)
- **40-eva-control-plane**: Evidence collection (refactor audit trail)
- **43-eva-spark**: Shared design system (component library)
- **48-eva-veritas**: Quality gates (MTI scoring, gap detection)
- **51-ACA**: Reference implementation for autonomous sprint execution

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
