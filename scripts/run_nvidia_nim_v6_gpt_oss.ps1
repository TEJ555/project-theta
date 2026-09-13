param(
    [switch]$FullPilot,
    [string]$Database = ""
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$seed = "3101"
$model = "openai/gpt-oss-20b"
$config = Join-Path $projectRoot "configs\nvidia-nim-v6-gpt-oss-development.json"

if ($FullPilot) {
    $conditions = "full,evidence_only,journal_only,permuted_journal,neutral_journal"
    $maxRuns = 5
    $maximumRequests = 90
    if (-not $Database) { $Database = "runs/nvidia-nim-v6-gpt-oss-pilot-01.sqlite" }
}
else {
    $conditions = "full"
    $maxRuns = 1
    $maximumRequests = 18
    if (-not $Database) { $Database = "runs/nvidia-nim-v6-gpt-oss-conformance-01.sqlite" }
}

$databasePath = Join-Path $projectRoot $Database
if (-not (Test-Path $theta)) {
    throw "Project Theta is not installed in .venv."
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

$previousGate = $env:THETA_ENABLE_MODEL_RUNS
$keyWasEntered = $false
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
    Write-Host "Project Theta NVIDIA GPT OSS V6 run"
    Write-Host "Database: $databasePath"
    Write-Host "Model: $model"
    Write-Host "Seed: $seed"
    Write-Host "Conditions: $conditions"
    Write-Host "Maximum hosted requests: $maximumRequests"

    & $theta audit --experiment endogenous_agency_v6 --seeds $seed
    if ($LASTEXITCODE -ne 0) { throw "V6 schedule audit failed." }
    & $theta doctor --adapter nvidia_nim --db "runs/nvidia-nim-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) { throw "NVIDIA NIM preflight failed." }
    & $theta run --config $config --experiment endogenous_agency_v6 --seeds $seed `
        --conditions $conditions --max-runs $maxRuns --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "NVIDIA GPT OSS V6 run failed." }
    & $theta audit --experiment endogenous_agency_v6 --seeds $seed `
        --conditions $conditions --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "Post-run protocol audit failed." }
}
finally {
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else { $env:THETA_ENABLE_MODEL_RUNS = $previousGate }
    if ($keyWasEntered) { Remove-Item Env:NVIDIA_API_KEY -ErrorAction SilentlyContinue }
}

Write-Host "NVIDIA GPT OSS V6 run completed."
