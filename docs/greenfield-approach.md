# Greenfield Architecture Approach - Project 53-refactor

**Date**: March 2, 2026  
**Strategy**: Build from scratch using proven patterns (NOT code migration)  
**Target**: React 19 + Agent Framework + Cosmos DB | Zero new infrastructure cost

---

## Frontend Architecture (3-Face Design)

### Decision: React 19 + Fluent UI v9 + Vite

**Why Greenfield**:
- EVA-JP-v1.2 frontend: Mixed Fluent UI v8/v9, monolithic, ~40% test coverage
- Greenfield: Clean React 19 + Fluent UI v9, modular 3-face design (admin/chat/portal)
- **Quality improvement**: Target 80% test coverage from day 1

### Pattern Source: 31-eva-faces

**Copy-Paste-Allowed**:
- `31-eva-faces/shared/hooks`: useAuth, useActingSession, useApi
- `31-eva-faces/shared/utils`: api-client (axios wrapper), formatters, validators
- `31-eva-faces/shared/types`: User, Session, ApiResponse, ActionResult
- `31-eva-faces/shared/layouts`: AppLayout (nav, header, sidebar, footer)
- `31-eva-faces/shared/components`: CommonDialog, ConfirmButton, DataTable, ErrorBoundary

**3-Face Structure**:
```
admin-face/
  src/
    pages/     (UserManagement, ConfigPanel, AuditLog, RoleManager, ...)
    hooks/     (local to admin)
    styles/    (admin theming)

chat-face/
  src/
    pages/     (ChatInterface, HistoryPanel, FileViewer, ...)
    hooks/     (useChat, useMessageHistory, ...)
    styles/    (chat theming)

portal-face/
  src/
    pages/     (Landing, PublicSearch, About, ...)
    hooks/     (local to portal)
    styles/    (portal theming)

shared/
  hooks/       (shared across all faces)
  utils/
  types/
  layouts/
```

**Bootstrap Component** (from 31-eva-faces):
```typescript
// Copy from 31-eva-faces/admin-face/src/hooks/useActingSession.ts
// Handles H1 handshake via POST /v1/roles/acting-as with X-Actor-OID header
// Falls back to DEV_BYPASS on error, persists session to sessionStorage
```

---

## Backend Architecture (Modular Routers)

### Decision: FastAPI + Microsoft Agent Framework

**Why Greenfield**:
- EVA-JP-v1.2 backend: Monolithic app.py (2473 lines), 4 custom RAG approaches, no async/await
- Greenfield: Modular routers from day 1, unified Agent Framework RAG, async/await throughout
- **Quality improvement**: Testable components, observable, extensible

### Pattern Source: 33-eva-brain-v2

**Modular Routers** (from 33-eva-brain-v2):
```python
# 33-eva-brain-v2/services/eva-brain-api/app/routes/

chat.py
  - POST /v1/chat (with Agent Framework RAG)
  - GET /v1/chat/{session_id}/history
  - DELETE /v1/chat/{session_id}
  
search.py
  - GET /v1/search (with Azure AI Search)
  - POST /v1/search (with filters)
  
upload.py
  - POST /v1/upload (with Blob Storage)
  - GET /v1/upload/{file_id}/status
  
roles.py  (from 28-rbac)
  - GET /v1/roles/list
  - POST /v1/roles/acting-as (H1 handshake)
  - GET /v1/roles/current
  
admin.py
  - GET /admin/users
  - POST /admin/users/{id}
  - GET /admin/audit
```

**Middleware Stack** (from 28-rbac):
```python
# Every route protected with RBAC middleware
@app.post("/v1/chat")
@rbac_required(roles=["user", "admin"])  # from 28-rbac/middleware.py
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    ...
```

**Observability** (from 51-ACA):
```python
# Every endpoint instrumented with OpenTelemetry
from opentelemetry import trace, metrics

tracer = trace.get_tracer(__name__)

@app.post("/v1/chat")
async def chat(request: ChatRequest):
    with tracer.start_as_current_span("chat_endpoint") as span:
        span.set_attribute("request.size", len(request.query))
        # ... implementation
```

---

## Data Layer Architecture

### Decision: Use Existing Cosmos DB (Zero New Cost)

**Resource**: `marco-sandbox-cosmos` in EsDAICoE-Sandbox (canadacentral)

**Greenfield Schema** (NOT ported from EVA-JP-v1.2):

| Container | Purpose | Partition Key | TTL | Rows (EST) |
|-----------|---------|---------------|-----|-----------|
| `jobs` | Async job tracking | `/job_id` | 24h | ~10K |
| `sessions` | User session cache | `/user_id` | 1h | ~5K |
| `documents` | Uploaded documents | `/user_id` | None | ~1K |
| `audit_log` | RBAC audit trail | `/user_id` | 90d | ~1M |
| `cache_tokens` | Embedding cache | `/hash` | 7d | ~100K |

**Why clean schema**:
- EVA-JP-v1.2 has 8+ containers with legacy fields
- Greenfield: 5 containers, designed for performance (indices on common queries)
- Lower RU/s consumption

---

## Infrastructure Architecture

### Decision: Deploy to Existing App Service Plan (ZERO New Cost)

**Existing Resources** (in `marco-sandbox` resource group):

| Resource | Type | Capacity | Reuse |
|----------|------|----------|-------|
| `marco-sandbox-asp-backend` | App Service Plan | Premium P1v2 | Add new App Service |
| `marcosandacr20260203` | Container Registry | Basic | Push Docker images |
| `marcosandkv20260203` | Key Vault | Standard | Store secrets |
| `marco-sandbox-appinsights` | App Insights | Pay-as-you-go | Log traces |
| `marco-sandbox-cosmos` | Cosmos DB | 1000 RU/s | Use 5 new containers |

**Deployment**:
```
marco-sandbox-asp-backend (existing)
  ├── eva-brain-v2-app (existing)
  └── eva-refactor-app (NEW - same plan, no new cost)

marcosandacr20260203 (existing)
  └── eva/refactor:v1.0 (NEW image)
```

**Total Cost**: **$0/month** (all existing resources)

---

## Quality Gates (Greenfield -> 80 MTI)

| Gate | Measure | Target | Baseline |
|------|---------|--------|----------|
| **Test Coverage** | pytest unit + integration + E2E | >= 80% | 42% (EVA-JP) |
| **MTI Score** | Veritas modernization index | >= 80 | 62 (EVA-JP) |
| **Code Quality** | Complexity, duplication, debt | LCC < 5 | 7.8 (EVA-JP) |
| **Performance** | P95 latency, throughput | < 200ms, > 100 req/s | TBD |
| **Security** | OWASP Top 10, hardcoded secrets | 0 violations | Multiple |
| **Documentation** | API schemas, ADRs, runbooks | 100% coverage | 40% |

---

## Key Principles

1. **NO Code Porting**: Build from scratch, use patterns only from proven refs
2. **Copy-Paste Allowed**: Direct use of hooks, utils, types from 31-eva-faces, 33-eva-brain-v2, 28-rbac
3. **Zero New Infrastructure**: Deploy to existing resources
4. **Async-First**: All operations async/await (no blocking I/O)
5. **Observable-First**: OpenTelemetry instrumentation in every router
6. **Test-First**: 80% coverage target, pytest fixtures from 51-ACA
7. **Feature Parity**: Map EVA-JP-v1.2 features to Greenfield implementations

---

## Pattern Reference Map

| Component | Reference Project | Source File |
|-----------|-------------------|------------|
| Frontend Hooks | 31-eva-faces | shared/hooks/ |
| Frontend Utils | 31-eva-faces | shared/utils/ |
| Frontend Types | 31-eva-faces | shared/types/ |
| Chat Router | 33-eva-brain-v2 | routes/chat.py |
| Search Router | 33-eva-brain-v2 | routes/search.py |
| Upload Router | 33-eva-brain-v2 | routes/upload.py |
| RBAC Middleware | 28-rbac | middleware.py |
| Observability | 51-ACA | observability/ |
| Test Patterns | 51-ACA | tests/ |

---

## Success Criteria

- [ ] Greenfield frontend: React 19 + 3-face design, 80% coverage
- [ ] Greenfield backend: FastAPI + Agent Framework, modular routers, 80% coverage
- [ ] Feature parity: All EVA-JP-v1.2 features reimplemented
- [ ] MTI improvement: 62 → 80 (29% gain)
- [ ] Zero new infrastructure cost
- [ ] All code from scratch (patterns + copy-paste allowed, no porting)
