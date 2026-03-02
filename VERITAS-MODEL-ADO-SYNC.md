# Veritas Model-ADO Sync for Project 53

**Purpose**: Automate bi-directional synchronization between the data model and Azure DevOps for project 53-refactor.

**Current State**: 115 stories seeded with sprint, assignee, project_id; ready for ADO sync to populate `ado_id`.

---

## Overview

The **veritas-model-ado** process ensures that:
1. Data model is the source of truth for story definitions (REFACTOR-03-001, ..., REFACTOR-11-010)
2. Azure DevOps is the operational platform (ADO PBIs, sprints, burndown charts)
3. Both systems stay synchronized via automated workflows

**Architecture**:

```
Data Model (Source)       ADO (Operations)
================          ================
/wbs/{story_id}    -----> PBI-{wi_id}
status: not-started       State: New
sprint: S10               Iteration: S10
assignee: marco.*         Assigned To: marco.*
ado_id: (empty)           (after sync) ado_id: PBI-001
                         (status sync) ado_id: PBI-002, etc.
```

---

## Two Sync Modes

### 1. Pull Mode (Model → ADO)
**Direction**: Data model → Azure DevOps  
**When**: Before Phase 3 starts (one-time initial sync)  
**What happens**:
- Reads 115 stories from data model (/model/wbs/?project_id=53-refactor)
- Creates PBIs in ADO project EVA-Refactor (Epic 33)
- Populates ado_id field in data model with PBI-{wi_id} values

**Run**:
```powershell
# Audit only (no changes)
pwsh scripts/veritas-model-ado-sync.ps1 -Mode audit

# Prepare artifacts (see what will be created)
pwsh scripts/veritas-model-ado-sync.ps1 -Mode prepare -DryRun

# Actually create work items (requires ADO_PAT)
$env:ADO_PAT = "<your-pat>"
pwsh scripts/veritas-model-ado-sync.ps1 -Mode sync -DryRun
pwsh scripts/veritas-model-ado-sync.ps1 -Mode sync  # live
```

### 2. Push Mode (ADO → Model)
**Direction**: Azure DevOps → Data model  
**When**: After Phase 3 execution (capture completion status)  
**What happens**:
- Queries ADO project for all PBIs in EVA-Refactor
- Reads work item state (New, Approved, Committed, Done)
- Updates data model story status and completed_at timestamps

**Run** (via GitHub Actions in Phase 3):
```
Workflow: .github/workflows/veritas-model-ado-sync.yml
Trigger: workflow_dispatch with mode=push
Result: Phase 3 completion metrics captured in data model
```

---

## Current Status (Pre-Sync)

| Field | Status | Notes |
|---|---|---|
| Sprint | ✅ Populated | All 115 stories have sprint S05-S16 |
| Assignee | ✅ Populated | All 115 stories assigned to marco.presta |
| Project ID | ✅ Populated | All 115 stories tagged 53-refactor |
| Size (FP) | ✅ Populated | Range 8-13, total 973 FP |
| ADO ID | ❌ Empty | Will populate during Pull mode sync |
| Status | ⏳ Pending | Will track via Push mode after execution |

---

## Before You Sync

1. **Verify ADO Project Exists**
   ```powershell
   $env:ADO_PAT = (az keyvault secret show --vault-name marco-sandbox-keyvault --name ADO-PAT --query value -o tsv)
   
   # Check EVA-Refactor project
   Invoke-RestMethod 'https://dev.azure.com/marcopresta/EVA-Refactor/_apis/projects?api-version=7.1' `
       -Headers @{Authorization = "Basic $([Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(':' + $env:ADO_PAT)))"} |
       Select-Object id, name
   ```

2. **Verify Data Model Stories**
   ```powershell
   $stories = Invoke-RestMethod 'https://marco-eva-data-model.../model/wbs/?project_id=53-refactor'
   Write-Host "Stories: $($stories.Count)"
   Write-Host "Sprint assignments: $(($stories | Where sprint).Count)"
   Write-Host "Assignees: $(($stories | Where assignee).Count)"
   ```

3. **Run Audit Mode** (no changes)
   ```powershell
   pwsh scripts/veritas-model-ado-sync.ps1 -Mode audit
   ```
   Expected output:
   ```
   [PASS] Project found: EVA Refactor
   [PASS] Found 115 stories
   [PASS] Sprint assigned: 115/115
   [PASS] Assignee assigned: 115/115
   [PASS] Audit result: READY FOR SYNC
   ```

---

## Step-by-Step: Performing Pull Mode Sync

### A. Preview (Dry-Run)

```powershell
cd C:\AICOE\eva-foundry\53-refactor

# 1. Audit
pwsh scripts/veritas-model-ado-sync.ps1 -Mode audit

# 2. Generate artifacts for review
pwsh scripts/veritas-model-ado-sync.ps1 -Mode prepare

# 3. Inspect the prepared artifacts
Get-Content .eva/ado-sync-artifacts.json | ConvertFrom-Json | Select-Object -ExpandProperty stories | Format-Table id, title, size_fp, sprint

# 4. Dry-run the sync (show what would be created without creating it)
$env:ADO_PAT = (az keyvault secret show --vault-name marco-sandbox-keyvault --name ADO-PAT --query value -o tsv)
pwsh scripts/veritas-model-ado-sync.ps1 -Mode sync -DryRun
```

### B. Actual Sync

```powershell
# IMPORTANT: Only proceed if audit passed and you've reviewed the artifacts

# 1. Authenticate to ADO
$env:ADO_PAT = (az keyvault secret show --vault-name marco-sandbox-keyvault --name ADO-PAT --query value -o tsv)

# 2. Run the sync (creates PBIs and populates ado_id)
pwsh scripts/veritas-model-ado-sync.ps1 -Mode sync

# 3. Monitor output for success:
#    [PASS] Created PBI-1001 for REFACTOR-03-001
#    [PASS] Created PBI-1002 for REFACTOR-03-002
#    ... (115 total)

# 4. Verify ado_id population
Invoke-RestMethod 'https://marco-eva-data-model.../model/wbs/REFACTOR-03-001' | Select-Object id, ado_id
# Expected: { id: "REFACTOR-03-001", ado_id: "PBI-1001" }
```

### C. Post-Sync Verification

```powershell
# Check all 115 stories have ado_id
$stories = Invoke-RestMethod 'https://marco-eva-data-model.../model/wbs/?project_id=53-refactor'
$withAdoId = @($stories | Where ado_id).Count
Write-Host "Stories with ado_id: $withAdoId/115"

# Query ADO to see the created PBIs
$base64Pat = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$env:ADO_PAT"))
$wiql = @{ query = "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.TeamProject] = 'EVA-Refactor' AND [System.WorkItemType] = 'Product Backlog Item'" } | ConvertTo-Json
Invoke-RestMethod 'https://dev.azure.com/marcopresta/EVA-Refactor/_apis/wit/wiql?api-version=7.1' `
    -Method POST -Headers @{Authorization = "Basic $base64Pat"; 'Content-Type' = 'application/json'} `
    -Body $wiql | Select-Object -ExpandProperty workItems | Format-Table id, url
```

---

## GitHub Actions Workflow (Automated)

**File**: `.github/workflows/veritas-model-ado-sync.yml`

**Trigger**: Manual via GitHub Actions

**Steps**:

1. **Veritas Audit** (validation gate):
   - Queries data model for MTI score
   - Checks story count, field completeness
   - Fails if MTI < 50 (trust gate)

2. **Model → ADO Pull** (if mode=pull):
   - Calls veritas-model-ado-sync.ps1 -Mode sync
   - Creates PBIs in EVA-Refactor
   - Populates ado_id in data model

3. **ADO → Model Push** (if mode=push):
   - Queries ADO for completed PBIs
   - Updates story status in data model
   - Records completed_at timestamps

4. **Finalize**: Posts summary to GitHub Actions log

**Usage**:
1. Go to GitHub: eva-foundry/53-refactor
2. **Actions** tab → **Veritas Model-ADO Sync**
3. **Run workflow** button
4. Select mode (pull / push) and audit_only option
5. Wait for completion

---

## FAQ

**Q: Can I run the sync multiple times?**  
A: Yes. The script checks for existing `ado_id` and skips those stories (idempotent). No duplicates.

**Q: What if the sync fails halfway?**  
A: Re-run it. Stories with populated `ado_id` are skipped; failed stories are retried.

**Q: What if I want to reassign a story?**  
A: Update the story in the data model (/model/wbs/{story_id}), then re-run the sync. ADO work item will be updated.

**Q: When does the Pull ↔ Push happen?**  
A: 
- **Pull** (Model → ADO): Before Phase 3 starts (one-time)
- **Push** (ADO → Model): At end of each sprint (continuous, via GitHub Actions or manual)

**Q: Who needs ADO_PAT?**  
A: The sync script. It needs a Personal Access Token with work item creation permission. Store in Key Vault or set `$env:ADO_PAT`.

**Q: What happens to MTI score?**  
A: Synced data does not affect MTI. MTI is calculated from PLAN.md ↔ code consistency. Verify with:
```powershell
node C:\AICOE\eva-foundry\48-eva-veritas\src\cli.js audit --repo .
```

---

## Related Scripts

- **populate-ado-fields.py**: Pre-sync, populated sprint/assignee/project_id for all 115 stories
- **veritas-model-ado-sync.ps1** (🆕): Actual sync engine
- **ado-bootstrap-pull.ps1** (38-ado-poc): Legacy ADO → Model puller (alternative if needed)
- **ado-import-project.ps1** (38-ado-poc): Legacy Model → ADO pusher (alternative if needed)

---

## Next Steps

1. ✅ **[DONE]** Populate sprint, assignee, project_id (populate-ado-fields.py)
2. ⏳ **[NEXT]** Run veritas-model-ado-sync audit to confirm readiness
3. ⏳ **[NEXT]** Execute Pull mode sync to create PBIs in ADO
4. ⏳ **[PHASE 3]** Execute Phase 3 (S05-S22): stories progress from New → Done
5. ⏳ **[POST-PHASE 3]** Run Push mode sync to capture completion metrics

**Timeline**:
- End of today: Audit + dry-run verification
- Tomorrow: Execute Pull mode sync (create 115 ADOs)
- S05 start: Phase 3 execution begins (2-week sprints)

---

**Last Updated**: 2026-03-02  
**Project**: 53-refactor  
**Stories**: 115 (REFACTOR-03-001 through REFACTOR-11-010)  
**ADO Project**: EVA-Refactor (Epic 33)
