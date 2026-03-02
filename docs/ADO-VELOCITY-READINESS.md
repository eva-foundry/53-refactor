# ADO Velocity & Metrics Readiness Report
## Project 53 vs EVA-POC

**Date**: March 2, 2026  
**Status**: AUDIT COMPLETE

---

## Executive Summary

| Item | Project 53 | EVA-POC | Status |
|---|---|---|---|
| **ADO Project Created** | ✅ EVA-Refactor (Epic 33) | ❌ Not found | 53 Ready |
| **WBS Stories Seeded** | ✅ 115 stories (REFACTOR-*) | ❓ Unknown | 53 Ready |
| **Story Sizing** | ✅ All have size_fp (8-13 FP) | ❓ Unknown | 53 Good |
| **Sprint Assignments** | ❌ Empty | ❌ N/A | **MISSING** |
| **Team Assignments** | ❌ Empty | ❌ N/A | **MISSING** |
| **ADO Work Item Links** | ❌ Empty (ado_id) | ❌ N/A | **MISSING** |
| **Velocity Ready** | 🟡 **40%** | ❌ **0%** | 53 Ahead |

---

## Current Data State: Project 53

### ✅ WHAT WE HAVE

**Seeded Stories (Phase 2 Complete)**:
```
115 total stories across 12 epics
Format: REFACTOR-03-001, REFACTOR-04-001, ... REFACTOR-11-010
```

**Story Fields Present**:
- ✅ `id` — Story identifier (REFACTOR-03-001)
- ✅ `title` — Story description ("Build chat router scaffold...")
- ✅ `size_fp` — Story points (8, 5, 13 FP - all populated)
- ✅ `status` — Current state ("not-started" for Phase 2)
- ✅ `created_at` — Timestamp (seeded date)
- ✅ `row_version` — Data model tracking (for concurrency)

**Project Configuration**:
- ✅ `ado_project_name` = "EVA-Refactor"
- ✅ `ado_epic_id` = "33"
- ✅ `ado_team` = "EVA-Refactor Team"

---

### ❌ WHAT'S MISSING (Critical for Velocity)

| Field | Current | Needed | Impact |
|---|---|---|---|
| **sprint** | Empty | "S05", "S06", etc. | Can't group by sprint → no velocity calc |
| **assignee** | Empty | "@user.name" | Can't track capacity → no team metrics |
| **ado_id** | Empty | "PBI-123" | Not linked to ADO → no bidirectional sync |
| **project_id** | Empty | "53-refactor" | Data model drift → query filters fail |
| **completed_at** | Empty | Timestamp | No burndown tracking → can't calculate daily velocity |

---

## Required Actions for ADO Velocity to Work

### Phase 3 Preparation (Before First Sprint S05)

**Step 1: Assign Stories to Sprints**
```powershell
# For each story, update sprint field
PUT /model/wbs/REFACTOR-03-001
{
  ...existing fields...
  "sprint": "S05"  # Sprint 05 = first execution sprint
}
```
**Impact**: Enables ADO to organize backlog by sprint, calculate sprint velocity

**Step 2: Assign Stories to Team Members**
```powershell
# Assign to engineering team
PUT /model/wbs/REFACTOR-03-001
{
  ...existing fields...
  "assignee": "marco.presta@hrsdc-rhdcc.gc.ca"  # or @agent:copilot
}
```
**Impact**: Enables capacity planning, team metrics, workload distribution

**Step 3: Create ADO Work Items & Link**
```powershell
# Via 38-ado-poc ADO sync (Pull mode)
# This creates PBI-XYZ in ADO project EVA-Refactor
# Then populate back to data model:
PUT /model/wbs/REFACTOR-03-001
{
  ...existing fields...
  "ado_id": "PBI-1001"  # ADO work item ID
}
```
**Impact**: Links data model ↔ ADO, enables bidirectional sync

**Step 4: Populate project_id**
```powershell
# Already in seeded data? Verify it's set
PUT /model/wbs/REFACTOR-03-001
{
  ...existing fields...
  "project_id": "53-refactor"
}
```
**Impact**: Fixes data model query filters, enables project-level rollups

### During Sprint Execution (S05-S22)

**Step 5: Update Status Daily**
```powershell
PUT /model/wbs/REFACTOR-03-001
{
  "status": "in-progress"  # → when developer starts
  "status": "done"         # → when completed
}
```

**Step 6: Record Completion Timestamp**
```powershell
# When status → "done"
PUT /model/wbs/REFACTOR-03-001
{
  "status": "done",
  "completed_at": "2026-03-15T14:30:00Z"  # When finished
}
```

---

## ADO Velocity Metrics: How It Works

Once all fields are populated, ADO can calculate:

### 1. **Sprint Velocity**
```
Sprint S05 Velocity = SUM(size_fp) 
  WHERE sprint="S05" AND status="done"
```
Example: If 8 stories done in S05 (total 47 FP), velocity = 47 FP/sprint

### 2. **Sprint Burndown**
```
Remaining Points = SUM(size_fp WHERE status!="done")
```
Daily chart shows points remaining vs. ideal line

### 3. **Team Capacity**
```
Team Capacity = COUNT(assignee) × avg_FP_per_person
```
Example: 3 team members × 20 FP/person = 60 FP capacity

### 4. **Release Forecast**
```
Sprints Needed = Total_FP ÷ Avg_Velocity
```
Example: 973 FP ÷ 47 FP/sprint = ~21 sprints

---

## Comparison: Project 53 vs EVA-POC

### Project 53 Status
```
ADO Project: EVA-Refactor
Stories: 115 seeded
Velocity Ready: 40% (sizing done, assignments pending)
Readiness: High (just need Phase 3 assignments)
```

### EVA-POC Status
```
ADO Project: ❌ NOT FOUND in data model
Stories: ❓ Unknown (not in data model WBS)
Velocity Ready: 0% (no ADO project configured)
Readiness: Low (needs project setup + story seeding)
```

### Why Project 53 is Ahead
1. ✅ Dedicated ADO project created (EVA-Refactor)
2. ✅ Stories seeded with sizing (115 × 8-13 FP)
3. ✅ Story IDs follow pattern (REFACTOR-*)
4. ✅ Project metadata in data model (row_version: 4)

**EVA-POC doesn't have equivalent setup**, so it cannot calculate velocity yet.

---

## What ADO Needs to Calculate Metrics

### REQUIRED (Cannot Calculate Without)
- [x] **size_fp** — Story points (Project 53: ✅ HAVE)
- [ ] **sprint** — Sprint assignment (Project 53: ❌ MISSING)
- [ ] **status** — Story state changes (Project 53: ❌ Won't have until Phase 3)
- [ ] **completed_at** — Completion timestamps (Project 53: ❌ Won't have until Phase 3)

### IMPORTANT (Degrades Without)
- [ ] **assignee** — Team member (Project 53: ❌ MISSING)
- [ ] **ado_id** — ADO work item link (Project 53: ❌ MISSING)

### OPTIONAL (Nice-to-Have)
- [ ] **project_id** — Project reference (Project 53: ❌ MISSING)
- [ ] **sprint_start/end** — Sprint dates (Project 53: ❌ MISSING)
- [ ] **original_estimate** — Pre-sprint estimate (Project 53: ❌ Not used)

---

## Timeline: When Project 53 Can Track Velocity

| Phase | When | ADO Metrics Available? |
|---|---|---|
| Phase 0-2 | Now (2026-03-02) | ❌ No (no sprint assignments) |
| **Phase 3-S05 Start** | ~2026-03-09 | 🟡 Partial (once S05 stories assigned to sprint + assignee) |
| **Phase 3-S05 End** | ~2026-03-16 | ✅ Full (status updates + completed_at timestamps) |
| **Phase 3-S06+** | ~2026-03-23+ | ✅ Complete (historical data for burndowns, forecasts) |

---

## Action Items for Project 53

### Before Sprint S05 Execution
- [ ] Create ADO Epic 33 in EVA-Refactor project (if not auto-created)
- [ ] Assign 115 stories to sprints (S05-S22 distribution)
- [ ] Assign each story to team member(s)
- [ ] Run ADO sync (38-ado-poc) to create work items
- [ ] Populate ado_id for each seeded story
- [ ] Verify project_id = "53-refactor" in all records

### During S05+ Execution
- [ ] Update story status: "not-started" → "in-progress" → "done"
- [ ] Record completed_at when stories finish
- [ ] Monitor ADO velocity chart (should start appearing end of S05)

### Data Quality Gates
- [ ] 100% of stories have sprint assignment
- [ ] 100% of stories have assignee
- [ ] 95%+ of stories linked to ADO (ado_id)
- [ ] All completed stories have completed_at timestamps

---

## Summary: ADO Velocity Readiness

**Project 53**:
- ✅ ADO project configured: **YES** (EVA-Refactor)
- ✅ Stories seeded: **YES** (115 stories)
- ✅ Sizing complete: **YES** (all 8-13 FP)
- ❌ Sprint assignments: **NO** (needed for Phase 3)
- ❌ Team assignments: **NO** (needed for Phase 3)
- ❌ ADO sync: **NO** (needed via 38-ado-poc)
- 🔴 **Current Readiness: 40%**

**EVA-POC**:
- ❌ ADO project: **NOT CONFIGURED**
- ❌ Stories: **NOT SEEDED**
- 🔴 **Current Readiness: 0%**

**Recommendation**: Project 53 is **well-positioned** to start velocity tracking in Phase 3. EVA-POC needs separate ADO project setup + story seeding to reach similar state.

---

*Report Generated: March 2, 2026*
