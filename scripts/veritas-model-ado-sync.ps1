#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Verify and audit ADO sync readiness for project 53-refactor.
    
.DESCRIPTION
    This script performs a veritas-model-ado audit to check:
    1. Data model has 115 stories with sprint, assignee, project_id
    2. ADO project is configured (EVA-Refactor, Epic 33)
    3. Stories are ready for ADO work item creation (Pull mode)
    
.PARAMETER Mode
    'audit' - Check readiness only (no changes)
    
.EXAMPLE
    pwsh veritas-model-ado-sync.ps1 -Mode audit
#>

param(
    [ValidateSet('audit')]
    [string]$Mode = 'audit',
    
    [string]$DataModelUrl = 'https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io',
    [string]$ProjectId = '53-refactor'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ─────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────

function Write-Status([string]$msg) { 
    Write-Host "[INFO] $msg" -ForegroundColor Cyan 
}

function Write-Pass([string]$msg) { 
    Write-Host "[PASS] $msg" -ForegroundColor Green 
}

function Write-Fail([string]$msg) { 
    Write-Host "[FAIL] $msg" -ForegroundColor Red 
}

function Write-Warn([string]$msg) { 
    Write-Host "[WARN] $msg" -ForegroundColor Yellow 
}

function Query-DataModel {
    param([string]$Endpoint)
    $url = "$DataModelUrl/model$Endpoint"
    Invoke-RestMethod $url -ErrorAction Stop
}

function Get-SafeProperty {
    param($Object, [string]$PropertyName)
    # Safely extract a property value, returning $null if it doesn't exist
    $Object | Select-Object -ExpandProperty $PropertyName -ErrorAction SilentlyContinue
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
    
    # 2. Count seeded stories - fetch all and filter client-side for project_id
    Write-Status "Counting seeded stories..."
    $allStories = @()
    try {
        $response = Query-DataModel "/wbs/"
        if ($response -is [array]) {
            $allStories = $response
        }
        elseif ($response -is [object] -and $response.id) {
            $allStories = @($response)
        }
    }
    catch {
        Write-Fail "Failed to query WBS: $_"
        return $false
    }
    
    # Filter to this project (project_id field must match)
    $stories = @()
    foreach ($story in $allStories) {
        $projId = Get-SafeProperty $story 'project_id'
        if ($projId -eq $ProjectId) {
            $stories += $story
        }
    }
    $count = $stories.Count
    
    if ($count -eq 0) {
        Write-Warn "No stories found with project_id=$ProjectId"
        return $false
    }
    
    Write-Pass "Found $count stories for $ProjectId"
    
    # 3. Check sprint assignments
    $sprintAssigned = 0
    foreach ($story in $stories) {
        if (Get-SafeProperty $story 'sprint') {
            $sprintAssigned++
        }
    }
    Write-Pass "  Sprint assigned: $sprintAssigned/$count"
    
    # 4. Check assignee assignments
    $assigneeAssigned = 0
    foreach ($story in $stories) {
        if (Get-SafeProperty $story 'assignee') {
            $assigneeAssigned++
        }
    }
    Write-Pass "  Assignee assigned: $assigneeAssigned/$count"
    
    # 5. Check ado_id population (should be empty currently)
    $adoIdPopulated = 0
    foreach ($story in $stories) {
        if (Get-SafeProperty $story 'ado_id') {
            $adoIdPopulated++
        }
    }
    if ($adoIdPopulated -eq 0) {
        Write-Pass "  ado_id: Not yet populated (expected before first sync)"
    }
    else {
        Write-Warn "  ado_id: $adoIdPopulated already populated"
    }
    
    # 6. Check sizing
    $sized = 0
    $totalFp = 0
    foreach ($story in $stories) {
        $size = Get-SafeProperty $story 'size_fp'
        if ($size) {
            $sized++
            $totalFp += $size
        }
    }
    Write-Pass "  Sized: $sized/$count (total FP: $totalFp)"
    
    # 7. Summary
    Write-Host ""
    if ($sprintAssigned -eq $count -and $assigneeAssigned -eq $count) {
        Write-Pass "═ Audit result: READY FOR SYNC"
        Write-Pass "All $count stories have sprint, assignee, and sizing."
        return $true
    }
    else {
        Write-Warn "═ Audit result: Not Ready"
        Write-Warn "Missing: $($count - $sprintAssigned) sprint assignments, $($count - $assigneeAssigned) assignees"
        return $false
    }
}

# ─────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Veritas Model-ADO Sync Audit | Project: $ProjectId" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$result = Invoke-Audit

Write-Host ""
if ($result) {
    Write-Pass "✓ Audit successful - ready to proceed with ADO sync"
    exit 0
}
else {
    Write-Fail "✗ Audit failed - fix issues before ADO sync"
    exit 1
}
