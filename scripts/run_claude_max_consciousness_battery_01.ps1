param([switch]$Recover)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$seedText = "1811,1931,2053,2179,2297"
$previousDatabase = $env:THETA_DATABASE
$previousGate = $env:THETA_ENABLE_MODEL_RUNS

$studies = @(
    @{
        Name = "metacognition"
        Experiment = "adversarial_theta"
        Conditions = "full,sham_body,shuffled_interoception,no_memory"
        Database = "runs/claude-max-consciousness-metacognition-01.sqlite"
        Spec = "workers/claude-max-consciousness-metacognition-01.json"
    },
    @{
        Name = "self-other"
        Experiment = "self_vs_other"
        Conditions = "full,no_self_model,no_workspace"
        Database = "runs/claude-max-consciousness-self-other-01.sqlite"
        Spec = "workers/claude-max-consciousness-self-other-01.json"
    },
    @{
        Name = "temporal"
        Experiment = "temporal_self"
        Conditions = "full,no_persistence,no_recurrence"
        Database = "runs/claude-max-consciousness-temporal-01.sqlite"
        Spec = "workers/claude-max-consciousness-temporal-01.json"
    }
)

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv."
}

try {
    Set-Location -LiteralPath $projectRoot
    $env:THETA_ENABLE_MODEL_RUNS = "YES"

    Write-Host "Project Theta consciousness indicator battery 01"
    Write-Host "New runs: 50"
    Write-Host "Maximum new subscription prompts: 1540"
    Write-Host "Console API route: blocked"
    Write-Host "Resume mode: $($Recover.IsPresent)"

    foreach ($study in $studies) {
        & $theta audit --experiment $study.Experiment --seeds $seedText
        if ($LASTEXITCODE -ne 0) {
            throw "Schedule audit failed for $($study.Name). No model prompt was sent."
        }
    }

    & $theta doctor --adapter claude_code --db "runs/claude-max-consciousness-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max preflight failed. No model prompt was sent."
    }

    foreach ($study in $studies) {
        $databasePath = Join-Path $projectRoot $study.Database
        $env:THETA_DATABASE = $databasePath
        $workerArguments = @("worker", "--spec", (Join-Path $projectRoot $study.Spec))
        if ($Recover) {
            $workerArguments += "--recover"
        }
        & $theta @workerArguments
        if ($LASTEXITCODE -ne 0) {
            throw "$($study.Name) paused or failed. Completed runs remain preserved."
        }
        & $theta audit `
            --experiment $study.Experiment `
            --seeds $seedText `
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
    Write-Host "Project Theta consciousness indicator battery 01 completed."
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

