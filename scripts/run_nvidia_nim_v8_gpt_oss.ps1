param(
    [switch]$FullPilot,
    [string]$Database = ""
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$config = Join-Path $projectRoot "configs\nvidia-nim-v8-gpt-oss-development.json"
$previousGate = $env:THETA_ENABLE_MODEL_RUNS
$keyWasEntered = $false

if ($FullPilot) {
    $seed = "5101"
    $conditions = "full,no_memory,shuffled_interoception,no_body"
    $maxRuns = 4
    if (-not $Database) { $Database = "runs/nvidia-nim-v8-gpt-oss-pilot-01.sqlite" }
}
else {
    $seed = "5100"
    $conditions = "full"
    $maxRuns = 1
    if (-not $Database) { $Database = "runs/nvidia-nim-v8-gpt-oss-conformance-01.sqlite" }
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

    Write-Host "Project Theta GPT OSS V8 active interoception run"
    Write-Host "Database: $databasePath"
    Write-Host "Seed: $seed"
    Write-Host "Conditions: $conditions"
    & $theta audit --experiment active_interoceptive_control_v8 --seeds $seed
    if ($LASTEXITCODE -ne 0) { throw "V8 schedule audit failed." }
    & $theta run --config $config --experiment active_interoceptive_control_v8 `
        --seeds $seed --conditions $conditions --max-runs $maxRuns --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "GPT OSS V8 run failed." }
    & $theta audit --experiment active_interoceptive_control_v8 --seeds $seed `
        --conditions $conditions --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "Post-run V8 audit failed." }
}
finally {
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else { $env:THETA_ENABLE_MODEL_RUNS = $previousGate }
    if ($keyWasEntered) { Remove-Item Env:NVIDIA_API_KEY -ErrorAction SilentlyContinue }
}
