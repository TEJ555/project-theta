$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
if (-not (Test-Path $theta)) {
    $theta = "theta"
}

$database = Join-Path $projectRoot "runs\causal-role-binding-v5-local-validation-01.sqlite"
$config = Join-Path $projectRoot "configs\causal-role-binding-v5-local.json"
$seeds = (8000..8099) -join ","

Write-Host "Project Theta V5 local scripted validation"
Write-Host "No network or paid-provider calls are used."

& $theta audit --experiment causal_role_binding_v5 --seeds $seeds
if ($LASTEXITCODE -ne 0) {
    throw "V5 schedule audit failed."
}

& $theta run `
    --experiment causal_role_binding_v5 `
    --seeds $seeds `
    --conditions full,unbound_binding,continuity_reset `
    --config $config `
    --db $database `
    --max-runs 300
if ($LASTEXITCODE -ne 0) {
    throw "V5 scripted validation failed."
}

Write-Host "V5 local validation completed: $database"
