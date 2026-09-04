param([switch]$Recover)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = Join-Path $projectRoot "runs\claude-max-self-model-binding-v3-confirmation-tranche-01.sqlite"
$specPath = Join-Path $projectRoot "workers\claude-max-self-model-binding-v3-confirmation-tranche-01.json"
$seeds = "3631,3733,3847,3943,4051"
$conditions = "full,no_self_model,no_workspace"
$previousDatabase = $env:THETA_DATABASE
$previousGate = $env:THETA_ENABLE_MODEL_RUNS

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv."
}

try {
    Set-Location -LiteralPath $projectRoot
    $env:THETA_ENABLE_MODEL_RUNS = "YES"
    $env:THETA_DATABASE = $databasePath

    Write-Host "Project Theta self-model binding v3 confirmation tranche 01"
    Write-Host "Fresh matched seeds: $seeds"
    Write-Host "Maximum completed runs: 15"
    Write-Host "Maximum subscription prompts: 900"
    Write-Host "Console API route: blocked"
    Write-Host "Resume mode: $($Recover.IsPresent)"

    & $theta audit --experiment self_model_binding_v3 --seeds $seeds
    if ($LASTEXITCODE -ne 0) {
        throw "Schedule audit failed. No model prompt was sent."
    }

    & $theta doctor --adapter claude_code --db "runs\claude-max-self-model-v3-confirmation-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max preflight failed. No model prompt was sent."
    }

    $arguments = @("worker", "--spec", $specPath)
    if ($Recover) {
        $arguments += "--recover"
    }
    & $theta @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Confirmation tranche paused or failed. Completed runs remain preserved."
    }

    & $theta audit `
        --experiment self_model_binding_v3 `
        --seeds $seeds `
        --conditions $conditions `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Execution audit failed. Results must not be interpreted."
    }

    & $theta report --db $databasePath
    Write-Host "Project Theta self-model binding v3 confirmation tranche 01 completed."
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
