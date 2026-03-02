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
    services: [],
    endpoints: [],
    screens: [],
    containers: [],
    features: [],
  };

  try {
    // Placeholder: In real implementation, would parse:
    // - services/ directory (FastAPI routes, etc.)
    // - frontend/ screens (React components)
    // - models/ (data schemas in Cosmos)
    // - docs/ (existing architecture)

    console.log('[INFO] Scanning EVA-JP-v1.2 for feature parity reference...');
    console.log('[INFO] Mode: reference-only (NOT for code porting)');
    console.log('[INFO] Placeholder: Real scanner would extract:');
    console.log('  - Services: auth, messaging, roles, search, reporting');
    console.log('  - Endpoints: ~150+ REST API routes');
    console.log('  - Screens: ~40+ React components');
    console.log('  - Containers: Cosmos DB schema (jobs, actors, case-law, etc.)');
    console.log('  - Features: Role hierarchy, case law search, acting-as, etc.');

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
