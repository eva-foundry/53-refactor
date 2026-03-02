# Sprint Issue Template -- 53-refactor

Use this format when creating a sprint issue. The `<!-- SPRINT_MANIFEST -->` block is
machine-readable. The narrative sections below it are for human review.

Label the issue with `sprint-task` to trigger the Sprint Agent workflow.

---

## How to create a sprint issue

```powershell
# 1. Create the issue
gh issue create --repo eva-foundry/53-refactor \
  --title "[SPRINT-05] Infrastructure & Agent Patterns" \
  --body-file .github/sprints/sprint-05.md \
  --label "sprint-task"

# 2. The workflow fires automatically on the sprint-task label.
# 3. Monitor progress via issue comments (agent posts after each story).
```

---

## Sprint Issue Body Format

The issue body must contain exactly one `<!-- SPRINT_MANIFEST ... -->` block.
All other content is narrative for human readers.

---

**EXAMPLE (PASTE BELOW THIS LINE into a new GitHub issue body):**

```
<!-- SPRINT_MANIFEST
{
  "sprint_id": "SPRINT-05",
  "sprint_title": "Infrastructure & Agent Patterns",
  "target_branch": "sprint/05-infra",
  "epic": "REFACTOR-03",
  "stories": [
    {
      "id": "REFACTOR-03-001",
      "title": "Add telemetry tracking module",
      "wbs": "3.1.1",
      "epic": "Epic 03 -- Infrastructure",
      "files_to_create": [
        "src/telemetry/__init__.py",
        "src/telemetry/tracker.py",
        "tests/test_telemetry.py"
      ],
      "acceptance": [
        "TelemetryTracker class tracks LM calls (tokens, cost, duration)",
        "track_call() method accepts model, tokens_in, tokens_out, cost",
        "get_summary() returns dict with total_calls, total_tokens, total_cost",
        "Tests pass (pytest tests/test_telemetry.py)"
      ],
      "implementation_notes": "Create TelemetryTracker class that tracks LM API calls. Store list of call records with timestamp, model, tokens_in, tokens_out, cost_usd, duration_ms. get_summary() aggregates across all calls. Use dataclasses for call records. Follow 53-refactor file structure."
    },
    {
      "id": "REFACTOR-03-002",
      "title": "Add evidence receipt generator",
      "wbs": "3.1.2",
      "epic": "Epic 03 -- Infrastructure",
      "files_to_create": [
        "src/evidence/__init__.py",
        "src/evidence/generator.py",
        "tests/test_evidence.py"
      ],
      "acceptance": [
        "EvidenceGenerator class generates story completion receipts",
        "generate() returns dict with story_id, phase, timestamp, test_result",
        "persist() writes JSON to .eva/evidence/ directory",
        "Tests pass (pytest tests/test_evidence.py)"
      ],
      "implementation_notes": "Create EvidenceGenerator class. Constructor takes story_id, phase, correlation_id. add_universal_data() accepts test_result, lint_result, duration_ms, tokens_used. generate() returns complete evidence dict. persist() writes to .eva/evidence/{story_id}-{phase}-{timestamp}.json. Use ISO8601 timestamps, JSON serialization."
    },
    {
      "id": "REFACTOR-04-001",
      "title": "Add agent configuration loader",
      "wbs": "4.1.1",
      "epic": "Epic 04 -- Agent Patterns",
      "files_to_create": [
        "src/config/__init__.py",
        "src/config/loader.py",
        "tests/test_config.py"
      ],
      "acceptance": [
        "load_config() reads .env file and returns dict",
        "Handles missing .env file gracefully (returns defaults)",
        "Supports DATA_MODEL_URL, MODEL, GITHUB_TOKEN keys",
        "Tests pass (pytest tests/test_config.py)"
      ],
      "implementation_notes": "Create load_config() function that reads .env using python-dotenv. Return dictionary with keys: DATA_MODEL_URL (default: ACA endpoint), MODEL (default: gpt-4o-mini), GITHUB_TOKEN (default: None). Use os.getenv() with defaults. Handle missing .env gracefully - should not raise errors."
    }
  ]
}
-->

## Sprint SPRINT-05: Infrastructure & Agent Patterns

### Objectives
- Establish core telemetry tracking infrastructure
- Create evidence generation pipeline for audit trail
- Add configuration management for agent workflows

### Stories in Scope
- **REFACTOR-03-001**: Telemetry tracker for LM call monitoring
- **REFACTOR-03-002**: Evidence receipt generator for Veritas integration
- **REFACTOR-04-001**: Configuration loader for agent settings

### Success Criteria
- All 3 stories completed with passing tests
- Evidence receipts generated and persisted
- Telemetry data accurately tracked and aggregated
- Configuration loaded from .env without errors

### Notes
This sprint establishes foundational infrastructure that will be used by all
subsequent sprints. Focus on clean interfaces and comprehensive test coverage.
```

---

## Field Definitions

### SPRINT_MANIFEST Schema

```typescript
{
  "sprint_id": string,           // Format: "SPRINT-NN"
  "sprint_title": string,        // Human-readable sprint name
  "target_branch": string,       // Git branch for this sprint (optional)
  "epic": string,                // Epic ID (e.g., "REFACTOR-03")
  "stories": [
    {
      "id": string,              // Format: "REFACTOR-NN-NNN"
      "title": string,           // Brief story description
      "wbs": string,             // Work breakdown structure ID
      "epic": string,            // Epic name
      "files_to_create": string[],  // Paths relative to repo root
      "acceptance": string[],    // Acceptance criteria (checkable assertions)
      "implementation_notes": string  // Detailed guidance for LM
    }
  ]
}
```

### Key Fields

- **sprint_id**: Must match pattern `SPRINT-NN` where NN is zero-padded (01, 02, etc.)
- **story id**: Must match pattern `REFACTOR-NN-NNN` (Epic-Story format)
- **files_to_create**: Relative paths from repo root. Agent will create these files.
- **acceptance**: Testable conditions. Agent validates against these post-implementation.
- **implementation_notes**: Detailed context for the LM. Include patterns, examples, edge cases.

---

## Workflow Behavior

1. **Trigger**: Add `sprint-task` label to issue
2. **Parse**: Workflow extracts JSON from `<!-- SPRINT_MANIFEST ... -->` block
3. **Execute**: Agent processes stories sequentially:
   - Query data model for story metadata
   - Call LM API with story context + implementation notes
   - Create files per `files_to_create`
   - Run tests (pytest) and linting (ruff)
   - Update data model with status + telemetry
   - Generate evidence receipt
   - Post progress comment to issue
4. **Complete**: Agent posts summary with:
   - Done count (N/M stories)
   - Total duration (ms)
   - Total cost ($, from LM tokens)
   - Total tokens (in + out)
   - Link to evidence receipts in .eva/evidence/

---

## Telemetry Collected

Per story:
- `tokens_in`, `tokens_out` (from LM API response)
- `cost_usd` (computed from model pricing)
- `duration_ms` (wall clock time)
- `files_created`, `files_modified` (from git diff)
- `test_result` (PASS/FAIL), `lint_result` (PASS/FAIL)
- `test_count` (pytest count)

Per sprint:
- Aggregate: total tokens, total cost, total duration
- LM call breakdown (per phase: P/D/C)
- Evidence receipts (JSON files in .eva/evidence/)
- Context snapshot (JSON file in .eva/sprints/)

---

## Evidence Schema

Evidence receipts are JSON files in `.eva/evidence/` with this structure:

```json
{
  "story_id": "REFACTOR-03-001",
  "phase": "A",
  "timestamp": "2026-03-02T15:30:00Z",
  "correlation_id": "REFACTOR-S05-20260302-a1b2c3d4",
  "sprint_id": "SPRINT-05",
  "test_result": "PASS",
  "lint_result": "PASS",
  "duration_ms": 12450,
  "tokens_used": 8500,
  "files_changed": 3,
  "artifacts": ["src/telemetry/tracker.py", "tests/test_telemetry.py"],
  "lm_telemetry": {
    "model": "gpt-4o-mini",
    "tokens_in": 3200,
    "tokens_out": 5300,
    "cost_usd": 0.0,
    "call_count": 2
  },
  "validation": {
    "test_exit_code": 0,
    "lint_exit_code": 0,
    "test_output_preview": "===== 12 passed in 2.5s =====",
    "lint_output_preview": "All checks passed!"
  }
}
```

---

## Example Sprint Issue Creation

```powershell
# Create sprint 05 for 53-refactor
cd C:\AICOE\eva-foundry\53-refactor

# Create issue (example - edit sprint-05.md first)
gh issue create `
  --repo eva-foundry/53-refactor `
  --title "[SPRINT-05] Infrastructure & Agent Patterns" `
  --body-file .github/sprints/sprint-05.md `
  --label "sprint-task"

# Monitor progress
gh issue view N --repo eva-foundry/53-refactor  # replace N with issue number

# Check evidence after completion
ls .eva/evidence/
cat .eva/evidence/REFACTOR-03-001-A-*.json
```
