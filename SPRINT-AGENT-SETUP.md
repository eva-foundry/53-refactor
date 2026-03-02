# Sprint Agent Setup -- Complete

**Date**: March 2, 2026  
**Project**: 53-refactor  
**Status**: ✅ READY FOR TESTING

---

## Infrastructure Created

### Core Sprint Automation Files

1. **`.github/scripts/sprint_agent.py`** (1249 lines)
   - Adapted from 51-ACA reference implementation
   - Full sprint execution runner with data model integration
   - GitHub Models API integration (gpt-4o-mini)
   - Evidence generation and telemetry tracking
   - Progress comments to GitHub issues

2. **`.github/scripts/sprint_context.py`** (202 lines)
   - Unified telemetry tracking for sprint execution
   - Correlation ID management: `REFACTOR-S{NN}-{YYYYMMDD}-{uuid[:8]}`
   - Timeline tracking (6 points): created, submitted, response, applied, tested, committed
   - LM call tracking: tokens_in, tokens_out, cost_usd, duration_ms
   - Sprint metrics: files_created, files_modified, test_count, lint_issues
   - Context persistence: `.eva/sprints/{sprint_id}-{uuid}-context.json`

3. **`.github/scripts/evidence_generator.py`** (136 lines)
   - Generate immutable evidence receipts for story completion
   - Universal fields: test_result, lint_result, duration_ms, tokens_used, files_changed
   - Type-specific fields: validation data, LM telemetry
   - Evidence persistence: `.eva/evidence/{story_id}-{phase}-{timestamp}.json`

4. **`.github/SPRINT_ISSUE_TEMPLATE.md`** (complete sprint guide)
   - Sprint manifest format (JSON embedded in issue body)
   - Field definitions and examples
   - Workflow behavior documentation
   - Telemetry schema reference
   - Evidence schema specification

---

## Configuration

### Project-Specific Settings

- **Project ID**: `53-refactor`
- **Correlation ID Format**: `REFACTOR-S{NN}-{YYYYMMDD}-{uuid[:8]}`
- **Data Model URL**: `https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io`
- **Actor**: `sprint-agent:53-refactor`
- **Model**: `gpt-4o-mini` (GitHub Models API, free tier)
- **Story ID Pattern**: `REFACTOR-{EPIC}-{NNN}` (e.g., REFACTOR-03-001)

### Environment Variables (GitHub Actions)

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Auto-provided
  REFACTOR_DATA_MODEL_URL: https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io
```

### Graceful Degradation

The sprint_agent.py has optional dependencies with fallback behavior:
- **SprintContext**: Available (created) ✅
- **state_lock**: Not available (ACA-specific) → Warning printed, execution continues
- **phase_verifier**: Not available (ACA-specific) → Warning printed, execution continues
- **requests**: Required for data model integration (install via pip)

---

## Adaptations from 51-ACA

### Changes Made

1. **Correlation ID**: `ACA-S{NN}` → `REFACTOR-S{NN}`
2. **Environment Variable**: `ACA_DATA_MODEL_URL` → `REFACTOR_DATA_MODEL_URL`
3. **Project ID**: `"51-ACA"` → `"53-refactor"`
4. **Actor**: `"sprint-agent"` → `"sprint-agent:53-refactor"`
5. **Story Tags**: `ACA-NN-NNN` → `REFACTOR-NN-NNN`
6. **Sprint ID Prefix**: `51-ACA-sprint-{id}` → `53-refactor-sprint-{id}`
7. **Project Name**: "Azure Cost Advisor SaaS" → "AI Agent Refactoring & Modernization"
8. **Model**: Kept `gpt-4o-mini` (GitHub Models API, free tier)

### Removed Features

- **Parallel Execution**: ThreadPoolExecutor infrastructure removed (simpler sequential execution)
- **ADO Bidirectional Sync**: Kept data model sync only
- **State Lock**: Idempotency guard disabled (optional ACA feature)
- **Phase Verifier**: Checkpoint validation disabled (optional ACA feature)

### Kept Features

- ✅ Data model integration (GET/PUT to `/model/wbs/{story_id}`, `/model/sprints/{sprint_id}`)
- ✅ GitHub Models API (gpt-4o-mini via `https://models.inference.ai.azure.com`)
- ✅ Evidence generation (Veritas-compatible receipts)
- ✅ Telemetry tracking (tokens, cost, duration, files changed)
- ✅ GitHub issue comments (progress + summary)
- ✅ DPDCA phase execution (D: Discover, P: Plan, D2: Do, C: Check, A: Act)

---

## Usage

### Command Line (Local Testing)

```powershell
cd C:\AICOE\eva-foundry\53-refactor

# Set environment variables
$env:GITHUB_TOKEN = (gh auth token)
$env:REFACTOR_DATA_MODEL_URL = "https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io"

# Run sprint agent (test with max 3 stories)
python .github\scripts\sprint_agent.py --issue N --repo eva-foundry/53-refactor --max-stories 3
```

### GitHub Actions (Cloud Execution)

1. Create sprint issue with `<!-- SPRINT_MANIFEST ... -->` block
2. Add `sprint-task` label to trigger workflow
3. Workflow parses manifest and executes stories
4. Progress comments posted to issue after each story
5. Final summary comment with metrics (cost, tokens, duration)

---

## Telemetry Collected

### Per-Story Metrics

Tracked by SprintContext and EvidenceGenerator:

- `tokens_in`: Input tokens from LM API call
- `tokens_out`: Output tokens from LM API response
- `cost_usd`: Calculated from model pricing (gpt-4o: $0.03/1K in + $0.06/1K out, gpt-4o-mini: free)
- `duration_ms`: Wall clock time from story start to commit
- `files_created`: Count of new files
- `files_modified`: Count of changed files
- `test_result`: PASS/FAIL from pytest
- `lint_result`: PASS/FAIL from ruff
- `test_count`: Number of tests executed
- `lint_issues`: Number of linting violations

### Per-Sprint Aggregates

- Total stories executed (M/N format)
- Total tokens (input + output across all stories)
- Total cost ($USD, sum of all LM calls)
- Total duration (ms, wall clock from sprint start to end)
- LM call breakdown by phase (P, D2, C)
- Evidence receipts count (N files in .eva/evidence/)

### Timeline Tracking

6 timeline points per story:

1. **created**: Sprint context initialized
2. **submitted**: Story planning phase started
3. **response**: LM API response received
4. **applied**: Code scaffolded and files written
5. **tested**: Tests and linting complete
6. **committed**: Changes committed to git

---

## Verification Checklist

Use this checklist after first sprint run:

### Files Created

- [ ] `.eva/sprints/{sprint_id}-{uuid}-context.json` exists
- [ ] `.eva/evidence/{story_id}-A-{timestamp}.json` exists (1 per story)
- [ ] Context file has: correlation_id, timeline (6 points), lm_summary, metrics, logs
- [ ] Evidence file has: story_id, phase, timestamp, test_result, lint_result, lm_telemetry

### Data Model Updates

Query data model to verify updates:

```powershell
$base = "https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io"

# Check story status
Invoke-RestMethod "$base/model/wbs/REFACTOR-03-001" | Select-Object id, status, start_timestamp, done_timestamp, test_result

# Check sprint status  
Invoke-RestMethod "$base/model/sprints/53-refactor-sprint-05" | Select-Object id, status, start_timestamp, story_count, completion_pct
```

Expected:
- [ ] Story status updated: `in-progress` → `done`
- [ ] Story timestamps: `start_timestamp`, `done_timestamp` populated
- [ ] Story test results: `test_result`, `lint_result` set (PASS/FAIL)
- [ ] Sprint status: `in_progress` → `done` (after last story)
- [ ] Sprint metrics: `completion_pct` = 100, `velocity` calculated

### GitHub Issue Comments

- [ ] Opening comment posted (sprint started, correlation ID, branch, story count)
- [ ] Progress comments posted (1 per story, status emoji ✅/❌, duration, test/lint results)
- [ ] Summary comment posted (done count M/N, total duration, total cost, total tokens, evidence link)

### Telemetry Accuracy

- [ ] LM call tracking: `tokens_in`, `tokens_out` match API response
- [ ] Cost calculation: Matches model pricing (gpt-4o-mini should be $0.00)
- [ ] Duration tracking: `duration_ms` is reasonable (positive non-zero)
- [ ] Test count: Matches pytest output ("N passed")
- [ ] Files changed: Matches git diff output

---

## Next Steps

1. **Test Sprint Issue**
   - Create test issue with 2-3 sample stories (e.g., REFACTOR-03-001, REFACTOR-03-002, REFACTOR-04-001)
   - Use `.github/SPRINT_ISSUE_TEMPLATE.md` example as reference
   - Stories should be simple (create module, add function, write test)

2. **Local Test Run**
   - Execute sprint_agent.py locally with `--max-stories 1`
   - Verify no startup/init errors
   - Confirm telemetry context is saved
   - Check evidence receipt is generated

3. **Cloud Workflow Setup**
   - Create `.github/workflows/sprint-agent.yml` (adapt from 51-ACA)
   - Set label trigger: `sprint-task`
   - Configure environment variables
   - Test with real GitHub issue

4. **Data Model Verification**
   - Query WBS layer for updated stories
   - Confirm correlation IDs are unique
   - Check evidence layer (if available) for receipts

5. **Documentation**
   - Update README.md with sprint automation instructions
   - Document environment variables required
   - Add troubleshooting section for common errors

---

## Troubleshooting

### "state_lock not available" Warning

**Cause**: 51-ACA-specific idempotency guard module not present in 53-refactor
**Impact**: None (optional feature)
**Action**: Ignore warning, execution continues normally

### "phase_verifier not available" Warning

**Cause**: 51-ACA-specific checkpoint validation module not present
**Impact**: None (optional feature)
**Action**: Ignore warning, execution continues normally

### "requests not available" Warning

**Cause**: `requests` Python package not installed
**Impact**: Data model integration disabled (critical feature)
**Action**: Install requests: `pip install requests`

### Data Model API Connection Error

**Symptoms**: "Data model API call failed: GET /model/wbs/..."
**Cause**: Network issue or incorrect DATA_MODEL_URL
**Action**: 
1. Check URL: `https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io`
2. Test health: `curl https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io/health`
3. Verify ACA is running: Check Azure Portal

### GitHub Models API 401 Unauthorized

**Symptoms**: "Failed to call GitHub Models API: 401"
**Cause**: Invalid or missing GITHUB_TOKEN
**Action**:
1. Local: `$env:GITHUB_TOKEN = (gh auth token)`
2. GitHub Actions: Token is auto-provided by GitHub (no setup needed)

### Evidence Files Not Created

**Symptoms**: `.eva/evidence/` directory is empty
**Cause**: Story execution failed before evidence generation step
**Action**:
1. Check sprint_agent.py output for errors
2. Verify test/lint checks passed (required for evidence)
3. Check git commit succeeded (evidence generated after commit)

---

## Technical Debt / Future Enhancements

### Immediate (Sprint 05)

- [ ] Add retry logic for data model API calls (exponential backoff)
- [ ] Add validation for SPRINT_MANIFEST JSON schema
- [ ] Add dry-run mode (--dry-run flag, no git commits)

### Short-term (Sprint 06-08)

- [ ] Replace inline evidence generation with `evidence_generator.py` import
- [ ] Add parallel story execution (ThreadPoolExecutor, port from 51-ACA)
- [ ] Add ADO bidirectional sync (port from 51-ACA if needed)
- [ ] Add state_lock for idempotency (port from 51-ACA if multi-agent)

### Long-term (Sprint 09+)

- [ ] Add Sonnet architecture review workflow (port from 51-ACA)
- [ ] Add automated rollback on failed sprints
- [ ] Add sprint metrics dashboard (cost trending, velocity, quality)
- [ ] Integrate with EVA-Veritas for continuous MTI scoring

---

## References

- **51-ACA Reference Implementation**: `C:\AICOE\eva-foundry\51-ACA\.github\scripts\sprint_agent.py`
- **Data Model API**: `C:\AICOE\eva-foundry\37-data-model\USER-GUIDE.md`
- **EVA-Veritas Integration**: `C:\AICOE\eva-foundry\48-eva-veritas\README.md`
- **Sprint Issue Template**: `C:\AICOE\eva-foundry\53-refactor\.github\SPRINT_ISSUE_TEMPLATE.md`
- **Workspace Instructions**: `C:\AICOE\.github\copilot-instructions.md` (Rules 6/7/8)

---

## Success Metrics

Track these after Sprint 05 (first production run):

- ✅ All stories completed without manual intervention
- ✅ Evidence receipts generated for every story
- ✅ Data model updated with accurate status/timestamps
- ✅ GitHub issue comments posted with correct telemetry
- ✅ Sprint context saved with complete timeline
- ✅ LM call tracking accurate (tokens, cost match API)
- ✅ No critical errors requiring agent restart

Target: 0 manual interventions, 100% evidence coverage, <5% cost variance vs API actual

---

**Status**: Infrastructure complete and tested (help output, imports, syntax valid)  
**Ready For**: Test sprint issue creation and first local run  
**Blocked By**: None  
**Owner**: GitHub Copilot (cloud agent) + Marco (sprint planning)
