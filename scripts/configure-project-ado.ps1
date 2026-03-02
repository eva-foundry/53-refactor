#!/usr/bin/env pwsh
# Configure Project 53 with dedicated ADO project

param(
    [string]$DataModelUrl = 'https://marco-eva-data-model.livelyflower-7990bc7b.canadacentral.azurecontainerapps.io'
)

# Get current record
$proj = Invoke-RestMethod "$DataModelUrl/model/projects/53-refactor"
$prev_rv = $proj.row_version

Write-Host "[INFO] Current row_version: $prev_rv"

# Update with dedicated ADO project
$body = @{
    id = '53-refactor'
    label = 'EVA Refactor Factory'
    project_name = 'EVA Refactor Factory'
    ado_project_name = 'EVA-Refactor'
    ado_epic_id = '33'
    ado_team = 'EVA-Refactor Team'
    project_url = 'https://dev.azure.com/marcopresta/EVA-Refactor'
    service = '53-refactor'
    maturity = 'idea'
    notes = 'Dedicated Azure DevOps project for greenfield legacy modernization POC. Not mixed with eva-poc.'
    is_active = $true
} | ConvertTo-Json -Depth 10

Write-Host "[INFO] Updating project 53 with dedicated ADO configuration..."

$result = Invoke-RestMethod "$DataModelUrl/model/projects/53-refactor" `
    -Method PUT `
    -ContentType 'application/json' `
    -Body $body `
    -Headers @{'X-Actor' = 'agent:copilot'}

Write-Host "[PASS] Project 53 updated"
Write-Host ""
Write-Host "---- ADO Configuration ----"
$result | Select-Object id, ado_project_name, ado_epic_id, ado_team, project_url | Format-List
Write-Host ""
Write-Host "Row version incremented: $prev_rv -> $($result.row_version)"
