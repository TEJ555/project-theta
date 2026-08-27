param(
    [string]$Database = "runs/claude-max-smoke.sqlite"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = Join-Path $projectRoot $Database

if (-not (Test-Path $theta)) {
    throw "Project Theta is not installed in .venv. Run python -m pip install -e . first."
}

$parent = Split-Path -Parent $databasePath
New-Item -ItemType Directory -Force -Path $parent | Out-Null
if (Test-Path $databasePath) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($databasePath)
    $extension = [System.IO.Path]::GetExtension($databasePath)
    $index = 2
    do {
        $candidate = Join-Path $parent "$stem-$index$extension"
        $index += 1
    } while (Test-Path $candidate)
    $databasePath = $candidate
}

Write-Host "Claude Max subscription smoke test"
Write-Host "Database: $databasePath"
Write-Host "Maximum subscription prompts: 1"
Write-Host "API key required: no"

$previousGate = $env:THETA_ENABLE_MODEL_RUNS
try {
    $env:THETA_ENABLE_MODEL_RUNS = "YES"
    & $theta doctor --adapter claude_code --db "runs/claude-max-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max preflight failed. No model prompt was sent."
    }
    & $theta run `
        --config (Join-Path $projectRoot "configs\claude-max-smoke.json") `
        --experiment navigation_demo `
        --seeds 997 `
        --conditions full `
        --max-runs 1 `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max smoke test failed. The database has been preserved."
    }
}
finally {
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else {
        $env:THETA_ENABLE_MODEL_RUNS = $previousGate
    }
}

Write-Host "Claude Max subscription smoke test completed."
