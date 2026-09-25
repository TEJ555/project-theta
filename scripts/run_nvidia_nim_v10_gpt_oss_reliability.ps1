param(
    [string]$Database = "runs/nvidia-nim-v10-gpt-oss-reliability-01.sqlite"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$config = Join-Path $projectRoot "configs\nvidia-nim-v10-gpt-oss-reliability.json"
$analysis = Join-Path $projectRoot "scripts\analyze_v10_reliability.py"
$seeds = "6300,6301,6302,6303,6304,6305"
$previousGate = $env:THETA_ENABLE_MODEL_RUNS
$keyWasEntered = $false
$databasePath = Join-Path $projectRoot $Database
$analysisPath = [System.IO.Path]::ChangeExtension($databasePath, ".analysis.json")

if (Test-Path -LiteralPath $databasePath) {
    throw "The frozen V10 database already exists. Refusing to replace or duplicate it."
}

try {
    if (-not $env:NVIDIA_API_KEY) {
        $secureKey = Read-Host "Paste a fresh NVIDIA API key (input is hidden)" -AsSecureString
        $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
        try {
            $env:NVIDIA_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
            $keyWasEntered = $true
        }
        finally {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
        }
    }
    if (-not $env:NVIDIA_API_KEY) { throw "No NVIDIA API key was supplied." }
    $env:THETA_ENABLE_MODEL_RUNS = "YES"

    Write-Host "Project Theta GPT OSS V10 reliability study"
    Write-Host "Database: $databasePath"
    Write-Host "Frozen seeds: $seeds"
    Write-Host "Maximum calls: 1056"
    & $theta audit --experiment multi_body_reliability_v10 --seeds $seeds
    if ($LASTEXITCODE -ne 0) { throw "V10 schedule audit failed." }
    & $theta run --config $config --experiment multi_body_reliability_v10 `
        --seeds $seeds --conditions full --max-runs 6 --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "GPT OSS V10 reliability study failed." }
    & $theta audit --experiment multi_body_reliability_v10 --seeds $seeds `
        --conditions full --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "Post-run V10 execution audit failed." }
    & $python $analysis $databasePath --output $analysisPath
    if ($LASTEXITCODE -ne 0) { throw "V10 frozen analysis failed." }
}
finally {
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else { $env:THETA_ENABLE_MODEL_RUNS = $previousGate }
    if ($keyWasEntered) { Remove-Item Env:NVIDIA_API_KEY -ErrorAction SilentlyContinue }
}
