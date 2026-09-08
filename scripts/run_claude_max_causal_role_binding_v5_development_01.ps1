param([switch]$Recover)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = Join-Path $projectRoot "runs\claude-max-causal-role-binding-v5-development-01.sqlite"
$specPath = Join-Path $projectRoot "workers\claude-max-causal-role-binding-v5-development-01.json"
$seeds = "9103,9209,9311"
$conditions = "full,unbound_binding,continuity_reset,permuted_continuity,register_hidden,raw_role_memory_hidden"
$previousDatabase = $env:THETA_DATABASE
$previousGate = $env:THETA_ENABLE_MODEL_RUNS

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv."
}

try {
    Set-Location -LiteralPath $projectRoot
    $env:THETA_ENABLE_MODEL_RUNS = "YES"
    $env:THETA_DATABASE = $databasePath

    Write-Host "Project Theta causal role binding v5 development pilot"
    Write-Host "Fresh development seeds: $seeds"
    Write-Host "Frozen conditions: $conditions"
    Write-Host "Maximum completed runs: 18"
    Write-Host "Maximum subscription prompts: 216"
    Write-Host "Backend claim: Claude Code routed system, not an isolated Sonnet model"
    Write-Host "Console API route: blocked"

    & $theta audit --experiment causal_role_binding_v5 --seeds $seeds
    if ($LASTEXITCODE -ne 0) {
        throw "Schedule and shortcut audit failed. No model prompt was sent."
    }

    & $theta doctor --adapter claude_code --db "runs\claude-max-causal-role-binding-v5-development-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max preflight failed. No model prompt was sent."
    }

    $arguments = @("worker", "--spec", $specPath)
    if ($Recover) {
        $arguments += "--recover"
    }
    & $theta @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Development pilot paused or failed. Completed runs remain preserved."
    }

    & $theta audit `
        --experiment causal_role_binding_v5 `
        --seeds $seeds `
        --conditions $conditions `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Execution audit failed. Results must not be interpreted."
    }

    & $theta report --db $databasePath
    Write-Host "Development pilot completed. It is not confirmatory evidence."
}
finally {
    if ($null -eq $previousDatabase) {
        Remove-Item Env:THETA_DATABASE -ErrorAction SilentlyContinue
    }
    else {
        $env:THETA_DATABASE = $previousDatabase
    }
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else {
        $env:THETA_ENABLE_MODEL_RUNS = $previousGate
    }
    Set-Location -LiteralPath $previousLocation
}
