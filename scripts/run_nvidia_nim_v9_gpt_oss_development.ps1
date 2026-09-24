param(
    [switch]$FullPilot,
    [string]$Database = ""
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$config = Join-Path $projectRoot "configs\nvidia-nim-v9-gpt-oss-development.json"
$previousGate = $env:THETA_ENABLE_MODEL_RUNS
$keyWasEntered = $false

if ($FullPilot) {
    $seed = "6101"
    $conditions = "full,feedback_corrupted,state_corrupted,feedback_and_state_corrupted,explicit_mapping,bridge_absent,bridge_incorrect,raw_history"
    $maxRuns = 8
    if (-not $Database) { $Database = "runs/nvidia-nim-v9-gpt-oss-pilot-01.sqlite" }
}
else {
    $seed = "6100"
    $conditions = "full"
    $maxRuns = 1
    if (-not $Database) { $Database = "runs/nvidia-nim-v9-gpt-oss-conformance-01.sqlite" }
}
$databasePath = Join-Path $projectRoot $Database
if (Test-Path -LiteralPath $databasePath) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($databasePath)
    $extension = [System.IO.Path]::GetExtension($databasePath)
    $index = 2
    do {
        $candidate = Join-Path (Split-Path -Parent $databasePath) "$stem-$index$extension"
        $index += 1
    } while (Test-Path -LiteralPath $candidate)
    $databasePath = $candidate
}

try {
    if (-not $env:NVIDIA_API_KEY) {
        $secureKey = Read-Host "Paste the NVIDIA API key (input is hidden)" -AsSecureString
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

    Write-Host "Project Theta GPT OSS V9 development run"
    Write-Host "Database: $databasePath"
    Write-Host "Seed: $seed"
    Write-Host "Conditions: $conditions"
    & $theta audit --experiment active_interoceptive_control_v9 --seeds $seed
    if ($LASTEXITCODE -ne 0) { throw "V9 schedule audit failed." }
    & $theta run --config $config --experiment active_interoceptive_control_v9 `
        --seeds $seed --conditions $conditions --max-runs $maxRuns --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "GPT OSS V9 run failed." }
    & $theta audit --experiment active_interoceptive_control_v9 --seeds $seed `
        --conditions $conditions --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "Post-run V9 audit failed." }
}
finally {
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else { $env:THETA_ENABLE_MODEL_RUNS = $previousGate }
    if ($keyWasEntered) { Remove-Item Env:NVIDIA_API_KEY -ErrorAction SilentlyContinue }
}
