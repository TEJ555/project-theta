param(
    [string]$Database = "runs/claude-max-independent-replication-01.sqlite",
    [switch]$Recover
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$spec = Join-Path $projectRoot "workers\claude-max-independent-replication-01.json"
$pilotDatabase = Join-Path $projectRoot "runs\claude-max-independent-pilot-01.sqlite"
$databasePath = if ([System.IO.Path]::IsPathRooted($Database)) {
    $Database
} else {
    Join-Path $projectRoot $Database
}
$seedText = "607,719,823,937,1049"
$conditionText = "matched_sham,full,shuffled_interoception"
$previousDatabase = $env:THETA_DATABASE
$previousGate = $env:THETA_ENABLE_MODEL_RUNS

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv. Run python -m pip install -e . first."
}
if (-not (Test-Path -LiteralPath $spec)) {
    throw "Frozen replication worker specification is missing at $spec"
}

try {
    Set-Location -LiteralPath $projectRoot
    $env:THETA_DATABASE = $databasePath
    $env:THETA_ENABLE_MODEL_RUNS = "YES"

    Write-Host "Claude Max Independent Theta replication 01"
    Write-Host "Database: $databasePath"
    Write-Host "Fresh seeds: $seedText"
    Write-Host "Conditions per seed: $conditionText"
    Write-Host "Maximum new subscription prompts: 900"
    Write-Host "Console API key route: blocked"
    Write-Host "Resume mode: $($Recover.IsPresent)"

    & $theta audit --experiment independent_theta --seeds $seedText
    if ($LASTEXITCODE -ne 0) {
        throw "Replication schedule audit failed. No model prompt was sent."
    }
    & $theta doctor --adapter claude_code --db "runs/claude-max-replication-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max preflight failed. No model prompt was sent."
    }

    $workerArguments = @("worker", "--spec", $spec)
    if ($Recover) {
        $workerArguments += "--recover"
    }
    & $theta @workerArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Replication paused or failed. Completed jobs remain preserved in $databasePath"
    }

    & $theta audit `
        --experiment independent_theta `
        --seeds $seedText `
        --conditions $conditionText `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Post-run replication audit failed. Results must not be interpreted."
    }

    if (Test-Path -LiteralPath $pilotDatabase) {
        Write-Host "Fresh replication report"
        & $theta report --db $databasePath
        Write-Host "Context report including the earlier diagnostic pilot"
        & $theta report --db $pilotDatabase --db $databasePath
    }
    Write-Host "Claude Max replication completed."
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
