#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Verify and populate veritas-model-ado sync for project 53-refactor.
    
.DESCRIPTION
    This script:
    1. Pulls the 115 seeded stories from the data model
    2. Checks ADO project configuration (EVA-Refactor, Epic 33)
    3. Prepares a batch of work items to create in ADO
    4. Syncs the ado_id back to the data model
    
.PARAMETER Mode
    'audit' - Check readiness only (no changes)
    'prepare' - Generate ADO artifacts (no changes to ADO)
    'sync' - Actually create work items and populate ado_id
    
.PARAMETER DryRun
    If specified, show what would happen but don't make changes
    
.EXAMPLE
    pwsh veritas-model-ado-sync.ps1 -Mode audit
    pwsh veritas-model-ado-sync.ps1 -Mode prepare -DryRun
    pwsh veritas-model-ado-sync.ps1 -Mode sync -DryRun
#>

param(
    [ValidateSet('audit', 'prepare', 'sync')]
    [string]$Mode = 'audit',
    
    [switch]$DryRun,
    
    [string]$DataModelUrl = 'https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io',
    [string]$ProjectId = '53-refactor',
    [string]$AdoOrg = 'https://dev.azure.com/marcopresta',
    [string]$AdoProject = 'EVA-Refactor',
    [string]$AdoPat = $env:ADO_PAT
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ─────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────

function Write-Status([string]$msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Pass([string]$msg) { Write-Host "[PASS] $msg" -ForegroundColor Green }
function Write-Fail([string]$msg) { Write-Host "[FAIL] $msg" -ForegroundColor Red }
function Write-Warn([string]$msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }

function Query-DataModel {
    param(
        [string]$Endpoint
    )
    try {
        $url = "$DataModelUrl/model$Endpoint"
        Invoke-RestMethod $url -ErrorAction Stop
    } catch {
        Write-Fail "Data model query failed: $_"
        throw
    }
}

function Invoke-AdoRest {
    param(
        [string]$method,
        [string]$endpoint,
        [object]$body
    )
    
    if (-not $AdoPat) {
        Write-Fail "ADO_PAT is required for ADO sync. Set `$env:ADO_PAT"
        throw 'ADO_PAT not configured'
    }
    
    $base64Pat = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$AdoPat"))
    $headers = @{
        Authorization = "Basic $base64Pat"
        'Content-Type' = 'application/json'
    }
    
    $url = "$AdoOrg/$AdoProject/_apis$endpoint"
    
    $params = @{
        Uri = $url
        Method = $method
        Headers = $headers
    }
    
    if ($body) {
        $params['Body'] = $body | ConvertTo-Json -Depth 10
    }
    
    Invoke-RestMethod @params
}

# ─────────────────────────────────────────────────────────────────────────
# AUDIT MODE: Check readiness without making changes
# ─────────────────────────────────────────────────────────────────────────

function Invoke-Audit {
    Write-Status "Starting veritas-model-ado audit..."
    
    # 1. Verify data model has project 53
    Write-Status "Checking data model project configuration..."
    $proj = Query-DataModel "/projects/$ProjectId"
    if (-not $proj.id) {
        Write-Fail "Project $ProjectId not found in data model"
        return $false
    }
    Write-Pass "Project found: $($proj.label)"
    Write-Pass "  ADO Project: $($proj.ado_project_name)"
    Write-Pass "  ADO Epic: $($proj.ado_epic_id)"
    
    # 2. Count seeded stories
    Write-Status "Counting seeded stories..."
    $stories = Query-DataModel "/wbs/?project_id=$ProjectId"
    if ($stories -is [array]) {
        $count = $stories.Count
    } elseif ($stories.id) {
        $count = 1
        $stories = @($stories)
    } else {
        $count = 0
    }
    Write-Pass "Found $count stories for $ProjectId"
    
    # 3. Check sprint assignments
    $sprintAssigned = @($stories | Where-Object { $_.sprint }).Count
    Write-Pass "  Sprint assigned: $sprintAssigned/$count"
    
    # 4. Check assignee assignments
    $assigneeAssigned = @($stories | Where-Object { $_.assignee }).Count
    Write-Pass "  Assignee assigned: $assigneeAssigned/$count"
    
    # 5. Check ado_id population (should be empty currently)
    $adoIdPopulated = @($stories | Where-Object { $_.ado_id }).Count
    if ($adoIdPopulated -eq 0) {
        Write-Pass "  ado_id: Not yet populated (expected before first sync)"
    } else {
        Write-Warn "  ado_id: $adoIdPopulated already populated (may cause duplicates)"
    }
    
    # 6. Check sizing
    $sized = @($stories | Where-Object { $_.size_fp }).Count
    Write-Pass "  Sized: $sized/$count (total FP: $($stories.size_fp | Measure-Object -Sum | Select-Object -ExpandProperty Sum))"
    
    # 7. Summary
    if ($sprintAssigned -eq $count -and $assigneeAssigned -eq $count) {
        Write-Pass "Audit result: READY FOR SYNC (all fields populated)"
        return $true
    } else {
        Write-Warn "Audit result: Partial readiness - missing $($count - $sprintAssigned) sprint or $($count - $assigneeAssigned) assignee assignments"
        return $false
    }
}

# ─────────────────────────────────────────────────────────────────────────
# PREPARE MODE: Generate artifacts for manual review
# ─────────────────────────────────────────────────────────────────────────

function Invoke-Prepare {
    Write-Status "Preparing ADO work item artifacts..."
    
    # Fetch stories from data model
    $stories = Query-DataModel "/wbs/?project_id=$ProjectId"
    if ($stories -isnot [array]) { $stories = @($stories) }
    
    # Build artifact structure
    $artifacts = @{
        project_id = $ProjectId
        ado_project = $AdoProject
        story_count = $stories.Count
        prepared_at = (Get-Date -Format 'o')
        stories = @()
    }
    
    foreach ($story in $stories) {
        $artifacts.stories += @{
            id = $story.id
            title = $story.title
            description = $story.description
            size_fp = $story.size_fp
            sprint = $story.sprint
            assignee = $story.assignee
            epic = $story.phase
        }
    }
    
    # Write to file
    $outFile = ".eva/ado-sync-artifacts.json"
    $artifacts | ConvertTo-Json -Depth 10 | Set-Content $outFile
    
    Write-Pass "Artifacts prepared: $outFile ($($artifacts.stories.Count) stories)"
    Write-Status "Example first story:"
    $artifacts.stories[0] | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor DarkGray
    
    return $true
}

# ─────────────────────────────────────────────────────────────────────────
# SYNC MODE: Create work items in ADO and populate ado_id
# ─────────────────────────────────────────────────────────────────────────

function Invoke-Sync {
    Write-Status "Starting model → ADO sync..."
    
    if ($DryRun) {
        Write-Warn "DRY RUN MODE - no changes will be made"
    }
    
    # 1. Run audit first
    $auditPassed = Invoke-Audit
    if (-not $auditPassed) {
        Write-Fail "Audit failed - cannot proceed with sync"
        return $false
    }
    
    # 2. Fetch stories
    $stories = Query-DataModel "/wbs/?project_id=$ProjectId"
    if ($stories -isnot [array]) { $stories = @($stories) }
    
    # 3. Attempt to create each story in ADO
    $created = 0
    $failed = 0
    $skipped = 0
    
    foreach ($story in $stories) {
        if ($story.ado_id) {
            Write-Warn "Story $($story.id) already has ado_id=$($story.ado_id) - skipping"
            $skipped++
            continue
        }
        
        # Create work item payload
        $wiPayload = @(
            @{
                op = 'add'
                path = '/fields/System.Title'
                value = "[$($story.id)] $($story.title)"
            }
            @{
                op = 'add'
                path = '/fields/System.Description'
                value = $story.description
            }
            @{
                op = 'add'
                path = '/fields/Microsoft.VSTS.Scheduling.StoryPoints'
                value = $story.size_fp
            }
            @{
                op = 'add'
                path = '/fields/System.IterationPath'
                value = "$AdoProject\$($story.sprint)"
            }
            @{
                op = 'add'
                path = '/fields/System.AssignedTo'
                value = $story.assignee
            }
            @{
                op = 'add'
                path = '/fields/System.Tags'
                value = "eva-story;$($story.id)"
            }
        )
        
        if ($DryRun) {
            Write-Status "DRY RUN: Would create PBI for $($story.id)"
            $created++
        } else {
            try {
                $wi = Invoke-AdoRest -method POST -endpoint '/wit/workitems?api-version=7.1&%24template=Bug' -body $wiPayload
                if ($wi.id) {
                    Write-Pass "Created PBI-$($wi.id) for $($story.id)"
                    
                    # Update data model with ado_id
                    $updateBody = @{ ado_id = "PBI-$($wi.id)" } | ConvertTo-Json
                    Query-DataModel "/wbs/$($story.id)" | ForEach-Object {
                        $_.ado_id = "PBI-$($wi.id)"
                        Invoke-RestMethod "$DataModelUrl/model/wbs/$($story.id)" `
                            -Method PUT `
                            -ContentType 'application/json' `
                            -Body ($_ | ConvertTo-Json -Depth 10) `
                            -Headers @{'X-Actor' = 'agent:copilot'} | Out-Null
                    }
                    
                    $created++
                } else {
                    Write-Fail "Failed to create PBI for $($story.id): $($wi | ConvertTo-Json | Select-Object -First 200)"
                    $failed++
                }
            } catch {
                Write-Fail "Error creating PBI for $($story.id): $_"
                $failed++
            }
        }
    }
    
    # Summary
    Write-Status "Sync complete:"
    Write-Pass "  Created: $created"
    Write-Fail "  Failed: $failed"
    Write-Warn "  Skipped: $skipped"
    
    return $failed -eq 0
}

# ─────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Veritas Model-ADO Sync | $Mode mode" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$result = switch ($Mode) {
    'audit' { Invoke-Audit }
    'prepare' { Invoke-Prepare }
    'sync' { Invoke-Sync }
}

if ($result) {
    Write-Host ""
    Write-Pass "Operation completed successfully"
    exit 0
} else {
    Write-Host ""
    Write-Fail "Operation failed"
    exit 1
}
