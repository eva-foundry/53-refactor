#!/usr/bin/env python3
"""
seed-greenfield-stories.py
Exports generated stories to JSON and seeds to data model WBS layer.
"""

import json
from datetime import datetime
import requests
import sys

def generate_stories():
    """Generate comprehensive Greenfield WBS with 115 stories."""
    
    stories = {
        "project": "53-refactor",
        "phase": "Phase-2-3",
        "generated": datetime.now().isoformat(),
        "epics": [
            {
                "epic_id": "EPIC-11",
                "epic_name": "Backend Greenfield - Core Routers",
                "stories": [
                    {"id": "REFACTOR-03-001", "title": "Build chat router scaffold with Agent Framework", "size": "M", "pattern": "33-eva-brain-v2/routes/chat.py", "components": ["RAGChainRouter", "SessionManager", "PromptTemplate"]},
                    {"id": "REFACTOR-03-002", "title": "Implement chat endpoint GET /v1/chat/{session_id}/history", "size": "M", "pattern": "33-eva-brain-v2/routes/chat.py#L45", "components": ["SessionRepository", "MessageHistoryFormatter"]},
                    {"id": "REFACTOR-03-003", "title": "Implement chat endpoint POST /v1/chat with streaming response", "size": "L", "pattern": "33-eva-brain-v2/routes/chat.py#L78", "components": ["AgentExecutor", "TokenCounter", "StreamHandler"]},
                    {"id": "REFACTOR-03-004", "title": "Implement session management (create, read, delete)", "size": "M", "pattern": "33-eva-brain-v2/routes/chat.py#L120", "components": ["SessionStore", "SessionValidator"]},
                    {"id": "REFACTOR-03-005", "title": "Build search router with Azure AI Search", "size": "M", "pattern": "33-eva-brain-v2/routes/search.py", "components": ["SearchClient", "QueryParser", "ResultsFormatter"]},
                    {"id": "REFACTOR-03-006", "title": "Implement search endpoint GET /v1/search with filters", "size": "M", "pattern": "33-eva-brain-v2/routes/search.py#L30", "components": ["FilterBuilder", "PaginationHandler"]},
                    {"id": "REFACTOR-03-007", "title": "Implement search endpoint POST /v1/search with semantic search", "size": "L", "pattern": "33-eva-brain-v2/routes/search.py#L60", "components": ["EmbeddingClient", "VectorSearch"]},
                    {"id": "REFACTOR-03-008", "title": "Build upload router with Blob Storage", "size": "M", "pattern": "33-eva-brain-v2/routes/upload.py", "components": ["BlobClient", "FileValidator", "StorageManager"]},
                    {"id": "REFACTOR-03-009", "title": "Implement upload endpoint POST /v1/upload", "size": "M", "pattern": "33-eva-brain-v2/routes/upload.py#L25", "components": ["MultipartHandler", "VirusScanner"]},
                    {"id": "REFACTOR-03-010", "title": "Implement upload status endpoint GET /v1/upload/{file_id}/status", "size": "S", "pattern": "33-eva-brain-v2/routes/upload.py#L55", "components": ["StatusTracker"]},
                ]
            },
            {
                "epic_id": "EPIC-12",
                "epic_name": "Backend Greenfield - Auth & RBAC",
                "stories": [
                    {"id": "REFACTOR-03-011", "title": "Build roles router scaffold", "size": "M", "pattern": "28-rbac/middleware.py", "components": ["RoleManager", "PermissionChecker"]},
                    {"id": "REFACTOR-03-012", "title": "Implement GET /v1/roles/list endpoint", "size": "S", "pattern": "28-rbac/routes.py#L10", "components": ["RoleRepository"]},
                    {"id": "REFACTOR-03-013", "title": "Implement POST /v1/roles/acting-as (H1 handshake)", "size": "M", "pattern": "28-rbac/routes.py#L25", "components": ["ActorValidator", "SessionWriter", "HeaderExtractor"]},
                    {"id": "REFACTOR-03-014", "title": "Implement GET /v1/roles/current endpoint", "size": "S", "pattern": "28-rbac/routes.py#L45", "components": ["CurrentRoleResolver"]},
                    {"id": "REFACTOR-03-015", "title": "Apply RBAC middleware to all protected routes", "size": "M", "pattern": "28-rbac/middleware.py#L90", "components": ["RBACDecorator", "TokenValidator"]},
                    {"id": "REFACTOR-03-016", "title": "Build admin router scaffold", "size": "M", "pattern": "33-eva-brain-v2/routes/admin.py", "components": ["AdminController"]},
                    {"id": "REFACTOR-03-017", "title": "Implement GET /admin/users endpoint", "size": "M", "pattern": "33-eva-brain-v2/routes/admin.py#L15", "components": ["UserRepository", "UserFormatter"]},
                    {"id": "REFACTOR-03-018", "title": "Implement POST /admin/users/{id} endpoint", "size": "M", "pattern": "33-eva-brain-v2/routes/admin.py#L40", "components": ["UserValidator", "AuditLogger"]},
                    {"id": "REFACTOR-03-019", "title": "Implement GET /admin/audit endpoint", "size": "M", "pattern": "33-eva-brain-v2/routes/admin.py#L60", "components": ["AuditRepository", "AuditFilter"]},
                    {"id": "REFACTOR-03-020", "title": "Implement OpenTelemetry auth tracing", "size": "M", "pattern": "51-ACA/observability/auth_tracer.py", "components": ["AuthSpan", "TokenTracer"]},
                ]
            },
            {
                "epic_id": "EPIC-13",
                "epic_name": "Frontend Greenfield - Admin Face",
                "stories": [
                    {"id": "REFACTOR-04-001", "title": "Initialize admin-face project with React 19 + Vite", "size": "M", "pattern": "31-eva-faces/admin-face", "components": ["ViteConfig", "PackageJson"]},
                    {"id": "REFACTOR-04-002", "title": "Copy shared hooks from 31-eva-faces", "size": "S", "pattern": "31-eva-faces/shared/hooks", "components": ["useAuth", "useActingSession", "useApi"]},
                    {"id": "REFACTOR-04-003", "title": "Copy shared utils from 31-eva-faces", "size": "S", "pattern": "31-eva-faces/shared/utils", "components": ["api-client", "formatters", "validators"]},
                    {"id": "REFACTOR-04-004", "title": "Copy shared types from 31-eva-faces", "size": "S", "pattern": "31-eva-faces/shared/types", "components": ["User", "Session", "ApiResponse"]},
                    {"id": "REFACTOR-04-005", "title": "Build AppLayout component with nav and header", "size": "M", "pattern": "31-eva-faces/shared/layouts", "components": ["NavBar", "Header", "Footer"]},
                    {"id": "REFACTOR-04-006", "title": "Create UserManagement page scaffold", "size": "M", "pattern": "31-eva-faces/admin-face/src/pages", "components": ["UserListPanel", "UserDetailsPanel"]},
                    {"id": "REFACTOR-04-007", "title": "Implement UserManagement list with DataTable component", "size": "M", "pattern": "31-eva-faces/shared/components#DataTable", "components": ["UserTable", "SortHandler", "FilterHandler"]},
                    {"id": "REFACTOR-04-008", "title": "Create ConfigPanel page for admin settings", "size": "M", "pattern": "31-eva-faces/admin-face/src/pages", "components": ["ConfigForm", "SettingsValidator"]},
                    {"id": "REFACTOR-04-009", "title": "Create AuditLog page for RBAC audit trail", "size": "M", "pattern": "31-eva-faces/admin-face/src/pages", "components": ["AuditTable", "DateRangeFilter"]},
                    {"id": "REFACTOR-04-010", "title": "Create RoleManager page for role/permission settings", "size": "L", "pattern": "31-eva-faces/admin-face/src/pages", "components": ["RoleEditor", "PermissionMatrix"]},
                ]
            },
            {
                "epic_id": "EPIC-14",
                "epic_name": "Frontend Greenfield - Chat Face",
                "stories": [
                    {"id": "REFACTOR-04-011", "title": "Initialize chat-face project with React 19 + Vite", "size": "M", "pattern": "31-eva-faces/chat-face", "components": ["ViteConfig", "PackageJson"]},
                    {"id": "REFACTOR-04-012", "title": "Create ChatInterface page scaffold", "size": "M", "pattern": "31-eva-faces/chat-face/src/pages", "components": ["MessagePanel", "InputPanel"]},
                    {"id": "REFACTOR-04-013", "title": "Implement message list with streaming support", "size": "L", "pattern": "31-eva-faces/chat-face/src/components#MessageList", "components": ["MessageRenderer", "StreamHandler", "TokenCounter"]},
                    {"id": "REFACTOR-04-014", "title": "Implement chat input component with file upload", "size": "M", "pattern": "31-eva-faces/chat-face/src/components#ChatInput", "components": ["InputField", "FileSelector", "SendButton"]},
                    {"id": "REFACTOR-04-015", "title": "Create HistoryPanel page for chat history", "size": "M", "pattern": "31-eva-faces/chat-face/src/pages", "components": ["HistoryList", "HistorySearch"]},
                    {"id": "REFACTOR-04-016", "title": "Create FileViewer component for uploaded documents", "size": "M", "pattern": "31-eva-faces/chat-face/src/components", "components": ["DocumentPreview", "PageNavigator"]},
                    {"id": "REFACTOR-04-017", "title": "Create SettingsDrawer for chat preferences", "size": "M", "pattern": "31-eva-faces/chat-face/src/components", "components": ["PreferenceForm", "ThemeToggle"]},
                    {"id": "REFACTOR-04-018", "title": "Implement useChat hook for state management", "size": "M", "pattern": "31-eva-faces/chat-face/src/hooks", "components": ["ChatState", "MessageHandler"]},
                    {"id": "REFACTOR-04-019", "title": "Create session management (new, load, save, delete)", "size": "M", "pattern": "31-eva-faces/chat-face/src/hooks", "components": ["SessionStorage", "SessionValidator"]},
                    {"id": "REFACTOR-04-020", "title": "Implement real-time chat updates via WebSocket", "size": "L", "pattern": "31-eva-faces/chat-face/src/hooks", "components": ["WebSocketClient", "MessageSync"]},
                ]
            },
            {
                "epic_id": "EPIC-15",
                "epic_name": "Frontend Greenfield - Portal Face",
                "stories": [
                    {"id": "REFACTOR-04-021", "title": "Initialize portal-face project with React 19 + Vite", "size": "M", "pattern": "31-eva-faces/portal-face", "components": ["ViteConfig", "PackageJson"]},
                    {"id": "REFACTOR-04-022", "title": "Create landing page with hero + CTA", "size": "M", "pattern": "31-eva-faces/portal-face/src/pages", "components": ["HeroSection", "CallToAction"]},
                    {"id": "REFACTOR-04-023", "title": "Create PublicSearch page (no auth required)", "size": "M", "pattern": "31-eva-faces/portal-face/src/pages", "components": ["SearchBar", "ResultsList"]},
                    {"id": "REFACTOR-04-024", "title": "Create About page with product info", "size": "S", "pattern": "31-eva-faces/portal-face/src/pages", "components": ["ContentPanel"]},
                    {"id": "REFACTOR-04-025", "title": "Create Documentation page with API reference", "size": "M", "pattern": "31-eva-faces/portal-face/src/pages", "components": ["DocNav", "CodeBlock"]},
                ]
            },
            {
                "epic_id": "EPIC-16",
                "epic_name": "Data Layer Greenfield - Cosmos Containers",
                "stories": [
                    {"id": "REFACTOR-05-001", "title": "Design Cosmos container schema (jobs)", "size": "M", "pattern": "51-ACA/data/cosmos_schemas.py", "components": ["JobSchema", "IndexDefinition"]},
                    {"id": "REFACTOR-05-002", "title": "Design Cosmos container schema (sessions)", "size": "M", "pattern": "51-ACA/data/cosmos_schemas.py", "components": ["SessionSchema", "TTLPolicy"]},
                    {"id": "REFACTOR-05-003", "title": "Design Cosmos container schema (documents)", "size": "M", "pattern": "51-ACA/data/cosmos_schemas.py", "components": ["DocumentSchema"]},
                    {"id": "REFACTOR-05-004", "title": "Design Cosmos container schema (audit_log)", "size": "M", "pattern": "51-ACA/data/cosmos_schemas.py", "components": ["AuditSchema", "PartitionStrategy"]},
                    {"id": "REFACTOR-05-005", "title": "Design Cosmos container schema (cache_tokens)", "size": "S", "pattern": "51-ACA/data/cosmos_schemas.py", "components": ["CacheSchema", "TTLExpiry"]},
                    {"id": "REFACTOR-05-006", "title": "Implement Cosmos repository pattern for jobs", "size": "M", "pattern": "33-eva-brain-v2/data/repositories.py", "components": ["JobRepository", "CosmosClient"]},
                    {"id": "REFACTOR-05-007", "title": "Implement Cosmos repository pattern for sessions", "size": "M", "pattern": "33-eva-brain-v2/data/repositories.py", "components": ["SessionRepository", "CacheLayer"]},
                    {"id": "REFACTOR-05-008", "title": "Implement Cosmos repository pattern for documents", "size": "M", "pattern": "33-eva-brain-v2/data/repositories.py", "components": ["DocumentRepository", "StorageLink"]},
                    {"id": "REFACTOR-05-009", "title": "Implement Cosmos repository pattern for audit_log", "size": "M", "pattern": "33-eva-brain-v2/data/repositories.py", "components": ["AuditRepository", "QueryBuilder"]},
                    {"id": "REFACTOR-05-010", "title": "Create Cosmos database initialization script", "size": "S", "pattern": "51-ACA/scripts/init_cosmos.py", "components": ["ContainerCreator", "IndexBuilder"]},
                ]
            },
            {
                "epic_id": "EPIC-17",
                "epic_name": "Observability Greenfield - OpenTelemetry & Instrumentation",
                "stories": [
                    {"id": "REFACTOR-06-001", "title": "Setup OpenTelemetry SDK for FastAPI", "size": "M", "pattern": "51-ACA/observability/otel_setup.py", "components": ["TracerProvider", "MeterProvider"]},
                    {"id": "REFACTOR-06-002", "title": "Instrument chat router with trace spans", "size": "M", "pattern": "51-ACA/observability/router_instrumentation.py", "components": ["ChatSpan", "AttributeTagger"]},
                    {"id": "REFACTOR-06-003", "title": "Instrument search router with trace spans", "size": "M", "pattern": "51-ACA/observability/router_instrumentation.py", "components": ["SearchSpan", "QueryCounter"]},
                    {"id": "REFACTOR-06-004", "title": "Instrument auth middleware with tracing", "size": "M", "pattern": "51-ACA/observability/auth_instrumentation.py", "components": ["AuthSpan", "TokenTracer"]},
                    {"id": "REFACTOR-06-005", "title": "Setup Application Insights exporter", "size": "M", "pattern": "51-ACA/observability/appinsights_exporter.py", "components": ["AppInsightsExporter"]},
                    {"id": "REFACTOR-06-006", "title": "Create structured logging middleware", "size": "M", "pattern": "51-ACA/observability/logging.py", "components": ["LogFormatter", "LogWriter"]},
                    {"id": "REFACTOR-06-007", "title": "Instrument Cosmos DB operations with metrics", "size": "M", "pattern": "51-ACA/observability/cosmos_metrics.py", "components": ["CosmosMetrics", "RUCounter"]},
                    {"id": "REFACTOR-06-008", "title": "Setup distributed tracing with W3C context", "size": "M", "pattern": "51-ACA/observability/w3c_context.py", "components": ["ContextPropagator"]},
                    {"id": "REFACTOR-06-009", "title": "Create health check endpoint with telemetry", "size": "S", "pattern": "51-ACA/observability/health.py", "components": ["HealthCheck"]},
                    {"id": "REFACTOR-06-010", "title": "Create monitoring dashboard JSON for App Insights", "size": "M", "pattern": "51-ACA/observability/dashboard.json", "components": ["DashboardConfig"]},
                ]
            },
            {
                "epic_id": "EPIC-18",
                "epic_name": "Security Greenfield - RBAC, Secrets, Validation",
                "stories": [
                    {"id": "REFACTOR-07-001", "title": "Setup Key Vault integration for secrets", "size": "M", "pattern": "28-rbac/secrets.py", "components": ["KeyVaultClient", "SecretFetcher"]},
                    {"id": "REFACTOR-07-002", "title": "Implement secret rotation handler", "size": "M", "pattern": "28-rbac/secrets.py", "components": ["RotationManager"]},
                    {"id": "REFACTOR-07-003", "title": "Setup Entra ID token validation", "size": "M", "pattern": "28-rbac/auth.py", "components": ["TokenValidator", "ClaimsExtractor"]},
                    {"id": "REFACTOR-07-004", "title": "Implement API request validation with Pydantic", "size": "M", "pattern": "33-eva-brain-v2/validation/schemas.py", "components": ["RequestValidator", "SchemaBuilder"]},
                    {"id": "REFACTOR-07-005", "title": "Implement rate limiting middleware", "size": "M", "pattern": "51-ACA/security/rate_limit.py", "components": ["RateLimiter", "TokenBucket"]},
                    {"id": "REFACTOR-07-006", "title": "Setup CORS policy for 3-face frontend", "size": "S", "pattern": "33-eva-brain-v2/security/cors.py", "components": ["CORSConfig"]},
                    {"id": "REFACTOR-07-007", "title": "Implement input sanitization for chat queries", "size": "M", "pattern": "51-ACA/security/sanitization.py", "components": ["InputSanitizer"]},
                    {"id": "REFACTOR-07-008", "title": "Setup HTTPS/TLS enforcement", "size": "S", "pattern": "51-ACA/security/http.py", "components": ["HTTPSConfig"]},
                    {"id": "REFACTOR-07-009", "title": "Implement audit logging for sensitive operations", "size": "M", "pattern": "28-rbac/audit.py", "components": ["AuditLogger", "EventWriter"]},
                    {"id": "REFACTOR-07-010", "title": "Create security policy documentation", "size": "M", "pattern": "51-ACA/docs/security.md", "components": ["PolicyDoc"]},
                ]
            },
            {
                "epic_id": "EPIC-19",
                "epic_name": "Testing Greenfield - Unit, Integration, E2E",
                "stories": [
                    {"id": "REFACTOR-08-001", "title": "Setup pytest fixtures for backend testing", "size": "M", "pattern": "51-ACA/tests/conftest.py", "components": ["CosmosFixture", "ClientFixture"]},
                    {"id": "REFACTOR-08-002", "title": "Write unit tests for chat router", "size": "L", "pattern": "51-ACA/tests/test_routes.py", "components": ["ChatTests"]},
                    {"id": "REFACTOR-08-003", "title": "Write unit tests for search router", "size": "L", "pattern": "51-ACA/tests/test_routes.py", "components": ["SearchTests"]},
                    {"id": "REFACTOR-08-004", "title": "Write unit tests for roles/auth", "size": "L", "pattern": "51-ACA/tests/test_auth.py", "components": ["AuthTests"]},
                    {"id": "REFACTOR-08-005", "title": "Write integration tests for Cosmos repository", "size": "L", "pattern": "51-ACA/tests/test_integration.py", "components": ["CosmosTests"]},
                    {"id": "REFACTOR-08-006", "title": "Setup Playwright fixtures for frontend testing", "size": "M", "pattern": "31-eva-faces/tests/playwright.config.ts", "components": ["PlaywrightConfig"]},
                    {"id": "REFACTOR-08-007", "title": "Write E2E tests for admin-face flows", "size": "L", "pattern": "31-eva-faces/tests/e2e/admin.spec.ts", "components": ["AdminFlowTests"]},
                    {"id": "REFACTOR-08-008", "title": "Write E2E tests for chat-face flows", "size": "L", "pattern": "31-eva-faces/tests/e2e/chat.spec.ts", "components": ["ChatFlowTests"]},
                    {"id": "REFACTOR-08-009", "title": "Write feature parity tests (EVA-JP-v1.2 vs Greenfield)", "size": "XL", "pattern": "51-ACA/tests/test_parity.py", "components": ["ParityTests"]},
                    {"id": "REFACTOR-08-010", "title": "Setup coverage reporting and thresholds", "size": "M", "pattern": "51-ACA/pytest.ini", "components": ["CoverageConfig"]},
                ]
            },
            {
                "epic_id": "EPIC-20",
                "epic_name": "Documentation Greenfield - OpenAPI, ADRs, Runbooks",
                "stories": [
                    {"id": "REFACTOR-09-001", "title": "Generate OpenAPI schema for backend API", "size": "M", "pattern": "33-eva-brain-v2/docs/openapi.json", "components": ["OpenAPIGen"]},
                    {"id": "REFACTOR-09-002", "title": "Create API documentation website (MkDocs)", "size": "L", "pattern": "51-ACA/docs/mkdocs.yml", "components": ["MkDocsConfig", "APIPages"]},
                    {"id": "REFACTOR-09-003", "title": "Write ADRs for all architecture decisions", "size": "L", "pattern": "53-refactor/docs/adr/", "components": ["ADRTemplate"]},
                    {"id": "REFACTOR-09-004", "title": "Create deployment runbook for App Service", "size": "M", "pattern": "51-ACA/docs/deployment.md", "components": ["DeploymentGuide"]},
                    {"id": "REFACTOR-09-005", "title": "Create troubleshooting guide with common issues", "size": "M", "pattern": "51-ACA/docs/troubleshooting.md", "components": ["TroubleshootingGuide"]},
                    {"id": "REFACTOR-09-006", "title": "Create developer setup guide", "size": "M", "pattern": "51-ACA/docs/dev-setup.md", "components": ["SetupGuide"]},
                    {"id": "REFACTOR-09-007", "title": "Create architecture diagram (Mermaid)", "size": "M", "pattern": "53-refactor/docs/architecture.md", "components": ["ArchDiagram"]},
                    {"id": "REFACTOR-09-008", "title": "Create data flow diagram for RAG pipeline", "size": "M", "pattern": "53-refactor/docs/data-flow.md", "components": ["FlowDiagram"]},
                    {"id": "REFACTOR-09-009", "title": "Write performance optimization guide", "size": "M", "pattern": "51-ACA/docs/optimization.md", "components": ["OptimizationGuide"]},
                    {"id": "REFACTOR-09-010", "title": "Create cost tracking and FinOps guide", "size": "M", "pattern": "51-ACA/docs/finops.md", "components": ["FinOpsGuide"]},
                ]
            },
            {
                "epic_id": "EPIC-21",
                "epic_name": "Integration Greenfield - External Services, APIs",
                "stories": [
                    {"id": "REFACTOR-10-001", "title": "Integrate with Azure OpenAI chat completions", "size": "M", "pattern": "33-eva-brain-v2/integrations/openai.py", "components": ["OpenAIClient"]},
                    {"id": "REFACTOR-10-002", "title": "Integrate with Azure AI Search", "size": "M", "pattern": "33-eva-brain-v2/integrations/ai_search.py", "components": ["SearchClient"]},
                    {"id": "REFACTOR-10-003", "title": "Integrate with Azure Blob Storage", "size": "M", "pattern": "33-eva-brain-v2/integrations/blob_storage.py", "components": ["BlobClient"]},
                    {"id": "REFACTOR-10-004", "title": "Integrate with Azure Cosmos DB SDK", "size": "M", "pattern": "33-eva-brain-v2/integrations/cosmos_db.py", "components": ["CosmosClient"]},
                    {"id": "REFACTOR-10-005", "title": "Integrate with Azure Key Vault", "size": "S", "pattern": "28-rbac/integrations/key_vault.py", "components": ["KeyVaultClient"]},
                    {"id": "REFACTOR-10-006", "title": "Integrate with Entra ID (token validation)", "size": "M", "pattern": "28-rbac/integrations/entra_id.py", "components": ["EntraIDValidator"]},
                    {"id": "REFACTOR-10-007", "title": "Integrate with Application Insights", "size": "M", "pattern": "51-ACA/integrations/app_insights.py", "components": ["AppInsightsExporter"]},
                    {"id": "REFACTOR-10-008", "title": "Setup webhook integration for async notifications", "size": "L", "pattern": "33-eva-brain-v2/integrations/webhooks.py", "components": ["WebhookHandler"]},
                    {"id": "REFACTOR-10-009", "title": "Integrate with external RAG service (if needed)", "size": "M", "pattern": "33-eva-brain-v2/integrations/rag_service.py", "components": ["RAGClient"]},
                    {"id": "REFACTOR-10-010", "title": "Setup event grid for async workflows", "size": "L", "pattern": "33-eva-brain-v2/integrations/event_grid.py", "components": ["EventGridHandler"]},
                ]
            },
            {
                "epic_id": "EPIC-22",
                "epic_name": "Deployment & DevOps",
                "stories": [
                    {"id": "REFACTOR-11-001", "title": "Create Dockerfile for FastAPI backend", "size": "M", "pattern": "51-ACA/Dockerfile", "components": ["DockerConfig"]},
                    {"id": "REFACTOR-11-002", "title": "Create Docker Compose for local development", "size": "M", "pattern": "51-ACA/docker-compose.yml", "components": ["ComposePython", "ComposeCosmosEmulator"]},
                    {"id": "REFACTOR-11-003", "title": "Setup CI/CD pipeline (GitHub Actions)", "size": "L", "pattern": "51-ACA/.github/workflows/", "components": ["BuildWorkflow", "TestWorkflow", "DeployWorkflow"]},
                    {"id": "REFACTOR-11-004", "title": "Create Bicep IaC for App Service deployment", "size": "L", "pattern": "51-ACA/infra/app-service.bicep", "components": ["AppServiceBicep"]},
                    {"id": "REFACTOR-11-005", "title": "Create Bicep IaC for Cosmos DB containers", "size": "M", "pattern": "51-ACA/infra/cosmos.bicep", "components": ["CosmosBicep"]},
                    {"id": "REFACTOR-11-006", "title": "Setup automated backup strategy", "size": "M", "pattern": "51-ACA/scripts/backup.sh", "components": ["BackupScript"]},
                    {"id": "REFACTOR-11-007", "title": "Create post-deployment health check script", "size": "S", "pattern": "51-ACA/scripts/health-check.sh", "components": ["HealthCheckScript"]},
                    {"id": "REFACTOR-11-008", "title": "Setup monitoring alerts in Application Insights", "size": "M", "pattern": "51-ACA/scripts/setup-alerts.ps1", "components": ["AlertConfig"]},
                    {"id": "REFACTOR-11-009", "title": "Create cost tracking dashboard", "size": "M", "pattern": "51-ACA/scripts/cost-dashboard.py", "components": ["CostDashboard"]},
                    {"id": "REFACTOR-11-010", "title": "Setup log rotation and retention policy", "size": "S", "pattern": "51-ACA/scripts/log-retention.ps1", "components": ["LogPolicy"]},
                ]
            },
        ],
    }
    
    return stories

def seed_to_data_model(base_url, stories_data):
    """Seed generated stories to data model WBS layer."""
    
    seeded_count = 0
    errors = []
    
    for epic in stories_data["epics"]:
        for story in epic["stories"]:
            wbs_record = {
                "id": story["id"],
                "title": story["title"],
                "phase": "Phase-3",
                "size_fp": {"S": 5, "M": 8, "L": 13, "XL": 21}.get(story["size"], 8),
                "status": "not-started",
                "order": None,
                "pattern_source": story["pattern"],
                "is_active": True,
            }
            
            try:
                response = requests.put(
                    f"{base_url}/model/wbs/{story['id']}",
                    json=wbs_record,
                    headers={"X-Actor": "agent:copilot"},
                    timeout=10
                )
                if response.status_code in [200, 201]:
                    seeded_count += 1
                    print(f"[PUT] {story['id']}: {response.status_code}")
                else:
                    errors.append(f"{story['id']}: {response.status_code} - {response.text[:100]}")
            except Exception as e:
                errors.append(f"{story['id']}: {str(e)}")
    
    return seeded_count, errors

def main():
    # Generate stories
    stories = generate_stories()
    
    # Save to JSON file
    output_file = ".eva/greenfield-stories.json"
    try:
        with open(output_file, "w") as f:
            json.dump(stories, f, indent=2)
        print(f"[OK] Saved {len([s for e in stories['epics'] for s in e['stories']])} stories to {output_file}")
    except Exception as e:
        print(f"[FAIL] Could not write to {output_file}: {e}")
        return 1
    
    # Seed to data model
    base_url = "https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io"
    print(f"[INFO] Seeding {len([s for e in stories['epics'] for s in e['stories']])} stories to data model...")
    
    seeded, errors = seed_to_data_model(base_url, stories)
    print(f"[INFO] Seeded {seeded}/{len([s for e in stories['epics'] for s in e['stories']])} stories")
    
    if errors:
        print(f"[WARN] {len(errors)} seeding errors:")
        for err in errors[:5]:
            print(f"  {err}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
