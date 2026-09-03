param([switch]$Recover)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$previousDatabase = $env:THETA_DATABASE
$previousGate = $env:THETA_ENABLE_MODEL_RUNS

$studies = @(
    @{
        Name = "temporal-binding-v2-replication"
        Experiment = "temporal_binding_v2"
        Seeds = "2861,2971,3083,3191,3301,3413"
        Conditions = "full,no_persistence,no_recurrence"
        Database = "runs/claude-max-temporal-binding-v2-replication-01.sqlite"
        Spec = "workers/claude-max-temporal-binding-v2-replication-01.json"
    },
    @{
        Name = "self-model-binding-v3-pilot"
        Experiment = "self_model_binding_v3"
        Seeds = "3527"
        Conditions = "full,no_self_model,no_workspace"
        Database = "runs/claude-max-self-model-binding-v3-pilot-01.sqlite"
        Spec = "workers/claude-max-self-model-binding-v3-pilot-01.json"
    }
)

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv."
}

try {
    Set-Location -LiteralPath $projectRoot
    $env:THETA_ENABLE_MODEL_RUNS = "YES"

    Write-Host "Project Theta temporal replication and self-model v3 pilot 01"
    Write-Host "Maximum completed runs: 21"
    Write-Host "Maximum subscription prompts: 828"
    Write-Host "Console API route: blocked"
    Write-Host "Resume mode: $($Recover.IsPresent)"

    foreach ($study in $studies) {
        & $theta audit --experiment $study.Experiment --seeds $study.Seeds
        if ($LASTEXITCODE -ne 0) {
            throw "Schedule audit failed for $($study.Name). No model prompt was sent."
        }
    }

    & $theta doctor --adapter claude_code --db "runs/claude-max-temporal-self-v3-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max preflight failed. No model prompt was sent."
    }

    foreach ($study in $studies) {
        $databasePath = Join-Path $projectRoot $study.Database
        $env:THETA_DATABASE = $databasePath
        $arguments = @("worker", "--spec", (Join-Path $projectRoot $study.Spec))
        if ($Recover) {
            $arguments += "--recover"
        }
        & $theta @arguments
        if ($LASTEXITCODE -ne 0) {
            throw "$($study.Name) paused or failed. Completed runs remain preserved."
        }
        & $theta audit `
            --experiment $study.Experiment `
            --seeds $study.Seeds `
            --conditions $study.Conditions `
            --db $databasePath
        if ($LASTEXITCODE -ne 0) {
            throw "Execution audit failed for $($study.Name). Results must not be interpreted."
        }
    }

    $reportArguments = @("report")
    foreach ($study in $studies) {
        $reportArguments += @("--db", (Join-Path $projectRoot $study.Database))
    }
    & $theta @reportArguments
    Write-Host "Project Theta temporal replication and self-model v3 pilot 01 completed."
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

