param(
    [string]$Database = "runs/nvidia-nim-v6-ultra-conformance.sqlite"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$config = Join-Path $projectRoot "configs\nvidia-nim-v6-ultra-development.json"
$databasePath = Join-Path $projectRoot $Database
$previousGate = $env:THETA_ENABLE_MODEL_RUNS
$keyWasEntered = $false

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

    Write-Host "Project Theta Nemotron Ultra competence run"
    Write-Host "Database: $databasePath"
    & $theta audit --experiment endogenous_agency_v6 --seeds 3101
    if ($LASTEXITCODE -ne 0) { throw "Schedule audit failed." }
    & $theta run --config $config --experiment endogenous_agency_v6 --seeds 3101 `
        --conditions full --max-runs 1 --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "Nemotron Ultra competence run failed." }
    & $theta audit --experiment endogenous_agency_v6 --seeds 3101 `
        --conditions full --db $databasePath
    if ($LASTEXITCODE -ne 0) { throw "Post-run audit failed." }
}
finally {
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else { $env:THETA_ENABLE_MODEL_RUNS = $previousGate }
    if ($keyWasEntered) { Remove-Item Env:NVIDIA_API_KEY -ErrorAction SilentlyContinue }
}
