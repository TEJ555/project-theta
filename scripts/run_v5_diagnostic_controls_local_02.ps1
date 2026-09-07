$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
if (-not (Test-Path $theta)) {
    $theta = "theta"
}

$database = Join-Path $projectRoot "runs\causal-role-binding-v5-controls-local-02.sqlite"
$config = Join-Path $projectRoot "configs\causal-role-binding-v5-local.json"
$seeds = (8200..8299) -join ","

Write-Host "Project Theta V5 diagnostic controls validation"
Write-Host "No network or paid-provider calls are used."

& $theta audit --experiment causal_role_binding_v5 --seeds $seeds
if ($LASTEXITCODE -ne 0) {
    throw "V5 schedule audit failed."
}

& $theta run `
    --experiment causal_role_binding_v5 `
    --seeds $seeds `
    --conditions full,permuted_continuity,register_hidden,raw_role_memory_hidden `
    --config $config `
    --db $database `
    --max-runs 400
if ($LASTEXITCODE -ne 0) {
    throw "V5 diagnostic controls validation failed."
}

Write-Host "V5 diagnostic controls validation completed: $database"
