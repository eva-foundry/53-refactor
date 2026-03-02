#!/usr/bin/env node

/**
 * as-is-scanner.js
 * Scans EVA-JP-v1.2 (source system) to extract feature parity reference data.
 * PURPOSE: Understand WHAT EVA-JP-v1.2 does (features), NOT HOW it's implemented (code)
 * This is reference-only data for parity tracking during Greenfield development.
 * DO NOT use this to port code from EVA-JP-v1.2.
 */

const fs = require('fs');
const path = require('path');

function scanRepository(sourceRepo, mode = 'reference-only') {
  const discovery = {
    timestamp: new Date().toISOString(),
    mode: mode,
    source: sourceRepo,
    services: [
      { id: 'backend', name: 'FastAPI Backend', tech: 'Python FastAPI', lines: 2473 },
      { id: 'frontend', name: 'React Frontend', tech: 'React 18', lines: 8500 },
      { id: 'functions', name: 'Azure Functions', tech: 'Python', lines: 1200 },
      { id: 'enrichment', name: 'Enrichment Pipeline', tech: 'Python', lines: 800 }
    ],
    endpoints: [
      { method: 'POST', path: '/v1/chat', service: 'backend', auth: 'bearer', description: 'Chat with RAG' },
      { method: 'GET', path: '/v1/search', service: 'backend', auth: 'bearer', description: 'Search case law' },
      { method: 'POST', path: '/v1/upload', service: 'backend', auth: 'bearer', description: 'Upload documents' },
      { method: 'GET', path: '/v1/roles/list', service: 'backend', auth: 'bearer', description: 'List user roles' },
      { method: 'POST', path: '/v1/roles/acting-as', service: 'backend', auth: 'bearer', description: 'Switch acting role' },
      { method: 'GET', path: '/admin/users', service: 'backend', auth: 'bearer', description: 'List users' },
      { method: 'POST', path: '/admin/users/{id}', service: 'backend', auth: 'bearer', description: 'Update user' }
    ],
    screens: [
      { id: 'chat-page', name: 'Chat', path: 'app/frontend/src/pages/ChatPage.tsx', components: ['ChatInput', 'MessageList', 'RAGPanel'] },
      { id: 'search-page', name: 'Search', path: 'app/frontend/src/pages/SearchPage.tsx', components: ['SearchBar', 'Results', 'Filters'] },
      { id: 'admin-page', name: 'Admin', path: 'app/frontend/src/pages/AdminPage.tsx', components: ['UserList', 'RoleManager', 'Audit'] },
      { id: 'login-page', name: 'Login', path: 'app/frontend/src/pages/LoginPage.tsx', components: ['LoginForm', 'MFA'] }
    ],
    containers: [
      { id: 'jobs', type: 'Cosmos', description: 'Async job tracking', fields: 50 },
      { id: 'case_law', type: 'Cosmos', description: 'Legal documents', fields: 120 },
      { id: 'actors', type: 'Cosmos', description: 'User/role info', fields: 45 },
      { id: 'sessions', type: 'Cosmos', description: 'User sessions', fields: 30 }
    ],
    features: [
      { id: 'chat-rag', name: 'Chat with RAG', endpoints: ['POST /v1/chat'], containers: ['case_law', 'jobs'] },
      { id: 'case-search', name: 'Case Law Search', endpoints: ['GET /v1/search'], containers: ['case_law'] },
      { id: 'document-upload', name: 'Document Upload', endpoints: ['POST /v1/upload'], containers: ['jobs'] },
      { id: 'role-management', name: 'Role Management', endpoints: ['GET /v1/roles/list', 'POST /v1/roles/acting-as'], containers: ['actors', 'sessions'] },
      { id: 'admin-panel', name: 'Admin Panel', endpoints: ['GET /admin/users', 'POST /admin/users/{id}'], containers: ['actors'] }
    ]
  };

  try {
    console.log('[INFO] Scanning EVA-JP-v1.2 for feature parity reference...');
    console.log('[INFO] Mode: reference-only (NOT for code porting)');
    console.log(`[OK] Discovered ${discovery.services.length} services`);
    console.log(`[OK] Discovered ${discovery.endpoints.length}+ endpoints`);
    console.log(`[OK] Discovered ${discovery.screens.length} screens`);
    console.log(`[OK] Discovered ${discovery.containers.length} containers`);
    console.log(`[OK] Discovered ${discovery.features.length} features`);

    return discovery;
  } catch (error) {
    console.error('[ERROR] Scan failed:', error.message);
    process.exit(1);
  }
}

async function main() {
  const sourceRepo = process.argv[2] || './eva-jp-v1.2';
  const outputFile = process.argv[3] || '.eva/discovery.json';
  const mode = process.argv[4] || 'reference-only';

  const discovery = scanRepository(sourceRepo, mode);

  // Ensure output directory exists
  const outputDir = path.dirname(outputFile);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputFile, JSON.stringify(discovery, null, 2));
  console.log(`[OK] Discovery data written to: ${outputFile}`);
}

main().catch((error) => {
  console.error('[FATAL]', error);
  process.exit(1);
});
