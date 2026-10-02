param(
    [string]$Database = "runs/nvidia-nim-v10-gpt-oss-reliability-01.sqlite",
    [switch]$Recover
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "nvidia_key.ps1")
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$spec = Join-Path $projectRoot "workers\nvidia-nim-v10-gpt-oss-reliability.json"
$analysis = Join-Path $projectRoot "scripts\analyze_v10_reliability.py"
$seeds = "6300,6301,6302,6303,6304,6305"
$previousDatabase = $env:THETA_DATABASE
$previousGate = $env:THETA_ENABLE_MODEL_RUNS
$keyWasLoadedByLauncher = $false
$locationPushed = $false
$databasePath = if ([System.IO.Path]::IsPathRooted($Database)) {
    $Database
} else {
    Join-Path $projectRoot $Database
}
$analysisPath = [System.IO.Path]::ChangeExtension($databasePath, ".analysis.json")

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv. Run python -m pip install -e . first."
}
if (-not (Test-Path -LiteralPath $spec)) {
    throw "Frozen V10 worker specification is missing at $spec"
}

if ((Test-Path -LiteralPath $databasePath) -and -not $Recover) {
    throw "The frozen V10 database already exists. Use -Recover only after confirming no worker is active."
}
if ($Recover -and -not (Test-Path -LiteralPath $databasePath)) {
    throw "Recovery was requested, but the V10 database does not exist. Start without -Recover."
}

try {
    Push-Location -LiteralPath $projectRoot
    $locationPushed = $true
    $keyWasLoadedByLauncher = Import-ProjectThetaNvidiaApiKey
    if (-not $env:NVIDIA_API_KEY) { throw "No NVIDIA API key was supplied." }
    $env:THETA_ENABLE_MODEL_RUNS = "YES"

    Write-Host "Project Theta GPT OSS V10 reliability study"
    Write-Host "Database: $databasePath"
    Write-Host "Frozen seeds: $seeds"
    Write-Host "Maximum calls: 1056"
    Write-Host "Recovery mode: $($Recover.IsPresent)"
    & $theta audit --experiment multi_body_reliability_v10 --seeds $seeds
    if ($LASTEXITCODE -ne 0) { throw "V10 schedule audit failed." }
    & $theta doctor --adapter nvidia_nim --db "runs/nvidia-nim-v10-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) { throw "NVIDIA NIM preflight failed. No model request was sent." }
    $env:THETA_DATABASE = $databasePath
    $workerArguments = @("worker", "--spec", $spec)
    if ($Recover) { $workerArguments += "--recover" }
    & $theta @workerArguments
    if ($LASTEXITCODE -ne 0) { throw "GPT OSS V10 reliability study failed." }
    & $theta audit --experiment multi_body_reliability_v10 --seeds $seeds `
        --conditions full --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "Post-run V10 execution audit failed." }
    & $python $analysis $databasePath --output $analysisPath
    if ($LASTEXITCODE -ne 0) { throw "V10 frozen analysis failed." }
}
finally {
    if ($locationPushed) { Pop-Location }
    if ($null -eq $previousDatabase) {
        Remove-Item Env:THETA_DATABASE -ErrorAction SilentlyContinue
    }
    else { $env:THETA_DATABASE = $previousDatabase }
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else { $env:THETA_ENABLE_MODEL_RUNS = $previousGate }
    if ($keyWasLoadedByLauncher) { Remove-Item Env:NVIDIA_API_KEY -ErrorAction SilentlyContinue }
}
