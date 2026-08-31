param(
    [string]$Database = "runs/claude-max-mechanism-ablation-01.sqlite",
    [switch]$Recover
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$spec = Join-Path $projectRoot "workers\claude-max-mechanism-ablation-01.json"
$databasePath = if ([System.IO.Path]::IsPathRooted($Database)) {
    $Database
} else {
    Join-Path $projectRoot $Database
}
$seedText = "1181,1301,1423,1549,1693"
$conditionText = "full,no_memory,no_workspace,no_body"
$previousDatabase = $env:THETA_DATABASE
$previousGate = $env:THETA_ENABLE_MODEL_RUNS

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv. Run python -m pip install -e . first."
}
if (-not (Test-Path -LiteralPath $spec)) {
    throw "Frozen mechanism worker specification is missing at $spec"
}

try {
    Set-Location -LiteralPath $projectRoot
    $env:THETA_DATABASE = $databasePath
    $env:THETA_ENABLE_MODEL_RUNS = "YES"

    Write-Host "Claude Max mechanism ablation 01"
    Write-Host "Database: $databasePath"
    Write-Host "Fresh seeds: $seedText"
    Write-Host "Conditions: $conditionText"
    Write-Host "Maximum new subscription prompts: 1200"
    Write-Host "Console API key route: blocked"
    Write-Host "Resume mode: $($Recover.IsPresent)"

    & $theta audit --experiment independent_theta --seeds $seedText
    if ($LASTEXITCODE -ne 0) {
        throw "Mechanism schedule audit failed. No model prompt was sent."
    }
    & $theta doctor --adapter claude_code --db "runs/claude-max-mechanism-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max preflight failed. No model prompt was sent."
    }

    $workerArguments = @("worker", "--spec", $spec)
    if ($Recover) {
        $workerArguments += "--recover"
    }
    & $theta @workerArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Mechanism study paused or failed. Completed jobs remain preserved in $databasePath"
    }

    & $theta audit `
        --experiment independent_theta `
        --seeds $seedText `
        --conditions $conditionText `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Post-run mechanism audit failed. Results must not be interpreted."
    }

    & $theta report --db $databasePath
    Write-Host "Claude Max mechanism-ablation study completed."
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

