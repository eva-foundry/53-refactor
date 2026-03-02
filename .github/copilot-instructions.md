# GitHub Copilot Instructions -- EVA Refactor Factory

**Template Version**: 3.5.0
**Last Updated**: 2026-03-02 16:43 ET
**Project**: 53-refactor -- AI-Driven Legacy Modernization at Scale
**Path**: `C:\AICOE\eva-foundry\53-refactor\`
**Stack**: Python (FastAPI agents), React (TypeScript), Node.js (GitHub Actions), SQL (PostgreSQL)

> This file is the Copilot operating manual for this repository.
> PART 1 is universal -- identical across all EVA Foundation projects.
> PART 2 is project-specific -- customise the placeholders before use.

---

## PART 1 -- UNIVERSAL RULES
> Applies to every EVA Foundation project. Do not modify. See workspace copilot-instructions for latest version.

---

### 1. Session Bootstrap (run in this order, every session)

Before answering any question or writing any code:

1. **Establish $base** (ACA primary -- run the bootstrap block in Section 3.1 first):
   - ACA (24x7, Cosmos-backed, no auth): `https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io`
   - Local dev fallback only: `http://localhost:8010`
   - `$base` must be set before any model query in this session.

2. **Read this project's governance docs** (in order):
   - `README.md` -- identity, stack, quick start
   - `PLAN.md` -- phases, current phase, next tasks
   - `STATUS.md` -- last session snapshot, open blockers
   - `ACCEPTANCE.md` -- DoD checklist, quality gates (if exists)
   - Latest `docs/YYYYMMDD-plan.md` and `docs/YYYYMMDD-findings.md` (if exists)

3. **Read the skills index** (if `.github/copilot-skills/` exists):
   - List files: `Get-ChildItem .github/copilot-skills/ -Filter "*.skill.md" | Select-Object Name`
   - Read `00-skill-index.skill.md` or the first skill matching the current task's trigger phrase
   - Each skill has a `triggers:` YAML block -- match it to the user's intent

4. **Query the data model** for this project's record:
   ```powershell
   Invoke-RestMethod "$base/model/projects/53-refactor" | Select-Object id, maturity, notes
   ```

5. **Produce a Session Brief** -- one paragraph: active phase, last test count, next task, open blockers.
   Do not skip this. Do not start implementing before the brief is written.

---

### 2. DPDCA Execution Loop

> **See workspace copilot-instructions** section "The EVA Factory Architecture" for the complete DPDCA loop explanation.
> This is data-driven AI-enabled Software Engineering, not code vibes.

Every session runs this cycle. Do not skip steps.

```
Discover  --> Query data model (WBS, services, endpoints) + veritas audit (MTI, gaps)
Plan      --> gen-sprint-manifest.py: filter undone stories, size, generate manifest
Do        --> Agent writes code using data model context (exact schemas, routes, locations)
Check     --> pytest (exit 0) + veritas MTI gate (>= 30 Sprint 2, >= 70 Sprint 3+)
Act       --> PUT status=done to WBS, reseed veritas-plan.json, reflect-ids.py updates PLAN.md
Loop      --> return to Discover for next sprint
```

**Execution Rule**: Make the change. Do not propose, narrate, or ask for permission on a step you can determine yourself. If uncertain about scope, ask one clarifying question then proceed.

**Why Deterministic**: Data model provides EXACT route paths, auth requirements, request/response schemas, file locations. Zero hallucination. One HTTP call beats 10 file reads.

---

### 2.1. Azure Best Practices Reference

When working on Azure infrastructure, always consult the workspace-level Azure best practices library before making design decisions or implementing Azure resources.

**Library**: `C:\AICOE\eva-foundry\18-azure-best\` (32 entries covering WAF, security, AI, resiliency, IaC, cost)
**Index**: `C:\AICOE\eva-foundry\18-azure-best\00-index.json`
**Usage**: See workspace copilot-instructions section "Azure Best Practices Reference Library"

**Quick examples for 53-refactor**:
- Designing Azure AI agent backend -> Read `04-ai-workloads/ai-security.md` + `02-well-architected/waf-ai-workload.md`
- RBAC design for refactor tenant isolation -> Read `12-security/rbac.md`
- PostgreSQL migration from Cosmos DB -> Read `02-well-architected/cost-optimization.md` (cost trade-off analysis)
- FastAPI deployment on ACA -> Read `10-compute/azure-functions.md` + `03-architecture-center/api-design.md`

---

### 3. EVA Data Model API -- Mandatory Protocol

> **GOLDEN RULE**: The `model/*.json` files are an internal implementation detail of the API server.
> Agents must never read, grep, parse, or reference them directly -- not even to "check" something.
> The HTTP API is the only interface. One HTTP call beats ten file reads.
> The API self-documents: `GET /model/agent-guide` returns the complete operating protocol.

> **Full reference**: `C:\AICOE\eva-foundry\37-data-model\USER-GUIDE.md` (v2.6)
> The model is the single source of truth. One HTTP call beats 10 file reads.
> Never grep source files for something the model already knows.

#### 3.1  Bootstrap

```powershell
# Primary -- ACA (24x7 Cosmos-backed, no auth required, always up)
$base = "https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io"
$h = Invoke-RestMethod "$base/health" -ErrorAction SilentlyContinue
# Local fallback -- only if ACA is in a rare maintenance window
if (-not $h) {
    $base = "http://localhost:8010"
    $h = Invoke-RestMethod "$base/health" -ErrorAction SilentlyContinue
    if (-not $h) {
        $env:PYTHONPATH = "C:\AICOE\eva-foundry\37-data-model"
        Start-Process "C:\AICOE\.venv\Scripts\python.exe" `
            "-m uvicorn api.server:app --port 8010 --reload" -WindowStyle Hidden
        Start-Sleep 4
    }
}
# Readiness check
$r = Invoke-RestMethod "$base/ready" -ErrorAction SilentlyContinue
if (-not $r.store_reachable) { Write-Warning "Cosmos unreachable -- check COSMOS_URL/KEY" }
# The API self-documents -- read the agent guide before doing anything
Invoke-RestMethod "$base/model/agent-guide"
# One-call state check -- all 32 layer counts + total objects
Invoke-RestMethod "$base/model/agent-summary"
```

**Azure APIM (CI / cloud agents):**
```powershell
$base = "https://marco-sandbox-apim.azure-api.net/data-model"
$hdrs = @{"Ocp-Apim-Subscription-Key" = $env:EVA_APIM_KEY}
Invoke-RestMethod "$base/model/agent-summary" -Headers $hdrs
```

#### 3.2  Query Decision Table

| You want to know... | One-turn API call | FORBIDDEN (costs 10 turns) |
|---|---|---|
| Browse all layers + objects visually | portal-face `/model` (requires `view:model` permission) | grep model/*.json |
| Report: overview / endpoint matrix / edge types | portal-face `/model/report` | build ad-hoc queries |
| All layer counts | `GET /model/agent-summary` | query each layer separately |
| Object by ID | `GET /model/{layer}/{id}` | grep, file_search |
| All objects in a layer | `GET /model/{layer}/` | read source files |
| All ready-to-call endpoints | `GET /model/endpoints/filter?status=implemented` | grep router files |
| All unimplemented stubs | `GET /model/endpoints/filter?status=stub` | grep router files |
| Filter ANY other layer | `GET /model/{layer}/` + `Where-Object` client-side | no server filter on non-endpoint layers |
| What a screen calls | `GET /model/screens/{id}` -> `.api_calls` | read screen source |
| Auth / feature flag for endpoint | `GET /model/endpoints/{id}` -> `.auth`, `.auth_mode`, `.feature_flag` | grep auth middleware |
| Where is the route handler | `GET /model/endpoints/{id}` -> `.implemented_in`, `.repo_line` | file_search |
| Cosmos container schema | `GET /model/containers/{id}` -> `.fields`, `.partition_key` | read Cosmos config |
| What breaks if container changes | `GET /model/impact/?container=X` | trace imports manually |
| Relationship graph | `GET /model/graph/?node_id=X&depth=2` | read config files |
| Infrastructure resource list | `GET /model/infrastructure/?service={service_name}` | grep MARCO-INVENTORY.md |
| Services list | `GET /model/services/` | manual file searching |
| WBS for this project | `GET /model/wbs/?project_id=53-refactor` | read PLAN.md locally |
| Is the process alive? | `GET /health` -> `.status`, `.store`, `.version` | check process list |
| Is Cosmos reachable? | `GET /health` -> `.store` == "cosmos" means Cosmos-backed | ping Cosmos directly |

#### 3.3  PUT Rules -- Read Before Every Write

**Rule 1 -- Capture `row_version` BEFORE mutating**
```powershell
$obj      = Invoke-RestMethod "$base/model/wbs/53-refactor-001"
$prev_rv  = $obj.row_version   # capture BEFORE mutation
$obj.status = "in-progress"
```

**Rule 2 -- Strip audit columns, keep domain fields**
Exclude: `obj_id`, `layer`, `modified_by`, `modified_at`, `created_by`, `created_at`, `row_version`, `source_file`.
`is_active` is a domain field -- keep it.
```powershell
function Strip-Audit ($obj) {
    $obj | Select-Object * -ExcludeProperty `
        obj_id, layer, modified_by, modified_at, created_by, created_at, row_version, source_file
}
```

**Rule 3 -- Use -Depth 10 for nested schemas**
`-Depth 5` silently truncates `request_schema` / `response_schema`. Always use `-Depth 10`.
```powershell
$body = Strip-Audit $obj | ConvertTo-Json -Depth 10
Invoke-RestMethod "$base/model/wbs/53-refactor-001" `
    -Method PUT -ContentType "application/json" -Body $body `
    -Headers @{"X-Actor"="agent:copilot"}
```

**Rule 4 -- PATCH is not supported** -- always PUT the full object (422 otherwise).

**Rule 5 -- Never PUT inside a `pwsh -Command` inline string** -- JSON escaping is mangled.
Write a `.ps1` script file and run it with `pwsh -File`. This is the single most common cause of failed model
writes. If a PUT fails on the first attempt, the first diagnosis is: is the body in an inline string?

---

## PART 2 -- PROJECT-SPECIFIC RULES

---

### Project: 53-refactor -- EVA Refactor Factory

**Purpose**: Standalone POC demonstrating autonomous refactoring of legacy EVA-JP-v1.2 via Veritas-Model-ADO workflow.

**Current Phase**: Phase 1 (DISCOVER + PLAN) -- generating modernization roadmap
**Stack**: FastAPI (agents), React (TypeScript), Node.js (GitHub Actions automation), PostgreSQL
**Infrastructure**: marco* resources from 22-rg-sandbox (no new Azure resources)

---

### PART 2.1: Commands & Quick Start

**Test Execution**:
```bash
# Run all tests (pytest)
pytest tests/ -v --tb=short

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_agents.py -v
```

**Development Server** (FastAPI agents backend):
```bash
# Local dev
uvicorn src.api.server:app --reload --port 8000

# With debug logs
FAST API_DEBUG=1 uvicorn src.api.server:app --reload --port 8000
```

**GitHub Actions Workflow** (sprint automation):
```bash
# Dry-run: verify the workflow would execute correctly
gh workflow run sprint-agent.yml --ref main --input dry_run=true

# Live execution: run the sprint
gh workflow run sprint-agent.yml --ref main
```

**Veritas Audit** (quality validation):
```powershell
# Full audit (MTI score, coverage, gaps)
node "C:\AICOE\eva-foundry\48-eva-veritas\src\cli.js" audit-repo --repo "C:\AICOE\eva-foundry\53-refactor"

# Dependency audit (cross-project impact)
node "C:\AICOE\eva-foundry\48-eva-veritas\src\cli.js" dependency-audit --repo "C:\AICOE\eva-foundry\53-refactor"
```

---

### PART 2.2: Project Structure

```
53-refactor/
  .github/
    copilot-instructions.md  (this file)
    copilot-skills/          (project-specific skills, when created)
    workflows/
      sprint-agent.yml       (GitHub Actions: autonomous execution)
  agents/                    (FastAPI agents + orchestration)
    discovery_agent.py       (scans legacy EVA-JP-v1.2 codebase)
    planning_agent.py        (generates modernization WBS)
    refactor_agent.py        (executes Greenfield rewrite)
  src/                       (API server, schemas, tools)
    api/
      server.py              (FastAPI app, /v1/agents/* endpoints)
      routes.py              (agent endpoints)
    schemas/                 (Pydantic models for agents + data)
  tests/                     (pytest test suite)
    test_agents.py           (unit tests for agents)
    test_api.py              (integration tests for endpoints)
  docs/
    YYYYMMDD-plan.md         (current sprint checklist)
    YYYYMMDD-status.md       (last session snapshot)
    YYYYMMDD-findings.md     (research, blockers, decisions)
  PLAN.md                    (master schedule: Phases 1-5 + sprints)
  STATUS.md                  (latest session summary)
  ACCEPTANCE.md              (DoD checklist + quality gates)
  README.md                  (vision + quick start)
```

---

### PART 2.3: Key Endpoints (Data Model Queries)

**Refactor Project WBS**:
```powershell
# All stories (sprint planning)
Invoke-RestMethod "$base/model/wbs/?project_id=53-refactor" | Select-Object id, title, phase, size_fp, status

# Active (undone) stories
Invoke-RestMethod "$base/model/wbs/?project_id=53-refactor&status=not-done" | Select-Object id, title

# By phase
Invoke-RestMethod "$base/model/wbs/?project_id=53-refactor&phase=1" | Select-Object id, title, size_fp
```

**Refactor Infrastructure** (which marco* resources are allocated):
```powershell
# Resources assigned to refactor (from marco* inventory)
Invoke-RestMethod "$base/model/infrastructure/?service=refactor" | Select-Object id, type, status

# All compute available (ACA, App Service, Functions)
Invoke-RestMethod "$base/model/infrastructure/" | Where-Object { $_.type -in @("container_app","app_service","function_app") }

# Cosmos DB (for schema mapping during refactor)
Invoke-RestMethod "$base/model/containers/" | Select-Object id, partition_key, fields
```

**Legacy EVA-JP-v1.2 Endpoints** (to understand as-is):
```powershell
# All endpoints from legacy service
Invoke-RestMethod "$base/model/endpoints/" | Where-Object { $_.service -eq "eva-jp-api" }

# Screens depending on those endpoints (feature matrix)
Invoke-RestMethod "$base/model/screens/" | Where-Object { $_.api_calls -contains "eva-jp-api" }
```

---

### PART 2.4: Quality Gates (ACCEPTANCE.md)

**Test Coverage**: >= 80% (pytest output)
**Veritas MTI**: >= 70 (Phase 3+)
**Endpoint Compatibility**: Old API == New API (request/response schema match)
**Feature Parity**: 100% of legacy endpoints re-implemented
**Security Audit**: No HIGH/CRITICAL findings (OWASP Top 10)

All gates must **PASS** before merging to main.

---

### PART 2.5: Key Patterns & Anti-Patterns

**Pattern: Veritas-Model-ADO Loop**

The project lives inside the EVA Factory workflow:
```
discovery_agent scans EVA-JP-v1.2 code
  |
  v
queries data model: What endpoints exist? What screens call them? What's the auth model?
  |
  v
planning_agent generates WBS (500+ stories)
  |
  v
seed-from-plan.py loads WBS to data model
  |
  v
ADO sync creates work items (Epic -> Feature -> Story -> Task)
  |
  v
GitHub Actions picks up stories (sprint-agent.yml)
  |
  v
refactor_agent reads code, generates new code, commits with EVA-STORY tag
  |
  v
Veritas validates: MTI >= 70, coverage >= 80%
  |
  v
Status: "done" in WBS, evidence receipt generated
```

**Anti-Pattern: Manual Code Migration**

Never manually copy-paste code from EVA-JP-v1.2. Always:
1. Query data model for as-is schema/endpoints
2. Let refactor_agent generate code from blueprint
3. Veritas validates the output
4. Commit with EVA-STORY tag (evidence traceable)

---

### PART 2.6: Common Blockers & Resolutions

**Blocker: "refactor_agent cannot find endpoint definition"**
- **Cause**: Endpoint not in data model (legacy system not scanned yet)
- **Fix**: Run `discovery_agent` to scan EVA-JP-v1.2 and populate endpoints layer

**Blocker: "WBS has 500+ stories, too many to sprint"**
- **Cause**: Planning_agent generated without size estimation
- **Fix**: Edit PLAN.md to group stories by phase (Phase 1-5), run gen-sprint-manifest.py to filter by phase

**Blocker: "Veritas MTI = 45, needs >= 70"**
- **Cause**: Missing tests or documentation gaps
- **Fix**: Run `veritas audit-repo` to get gap report, add tests/docs per gaps, rerun audit

**Blocker: "Cosmos container schema changed, endpoints reference old schema"**
- **Cause**: Data model inconsistency
- **Fix**: Query `/model/impact/?container=X` to find all affected endpoints, update schema in model

---

### PART 2.7: Debugging

**Enable Agent Traces**:
```bash
# FastAPI agent traces (stdout)
AGENT_TRACE=1 uvicorn src.api.server:app --reload

# GitHub Actions logs
gh run view {RUN_ID} --log  # shows full sprint-agent.yml execution
```

**Inspect Data Model State**:
```powershell
# Check if WBS was seeded correctly
Invoke-RestMethod "$base/model/wbs/?project_id=53-refactor" | Measure-Object
# Output: Count = 500+ (expected for Phase 1 planning)

# Check if endpoints were discovered
Invoke-RestMethod "$base/model/endpoints/" | Where-Object { $_.service -eq "eva-jp-api" } | Measure-Object
# Output: Count > 0 (expected after discovery_agent runs)
```

**Check GitHub Actions Logs**:
```bash
# List recent runs
gh run list --repo eva-foundry/53-refactor

# View latest run log
gh run view --repo eva-foundry/53-refactor --log
```

---

### PART 2.8: Deployment

**Staging** (before main):
```bash
# Run sprint in dry-run mode
gh workflow run sprint-agent.yml --ref develop --input dry_run=true

# Review generated code in branch {sprint_id}
git checkout remotes/origin/{sprint_id}
```

**Production** (main branch):
```bash
# Verify Veritas gates pass
pytest tests/ -v && \
node "C:\AICOE\eva-foundry\48-eva-veritas\src\cli.js" audit-repo --repo .

# Merge to main triggers GitHub Actions production deployment
git push origin develop:main
```

---

### PART 2.9: Related Projects & Resources

**Data Model** (source of truth): [37-data-model](https://github.com/eva-foundry/37-data-model)
**Veritas** (quality gates + traceability): [48-eva-veritas](https://github.com/eva-foundry/48-eva-veritas)
**ADO Integration** (work item sync): [38-ado-poc](https://github.com/eva-foundry/38-ado-poc)
**Foundry** (agent orchestration): [29-foundry](https://github.com/eva-foundry/29-foundry)
**Azure Best Practices** (design guidance): [18-azure-best](https://github.com/eva-foundry/18-azure-best)
**Microsoft Agent Framework** (agents SDK): https://github.com/microsoft/agent-framework

---

**Last Updated**: March 2, 2026 16:43 ET
**Version**: 3.5.0
**Maintained By**: GitHub Copilot (AI Agent)
