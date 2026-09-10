param(
    [string]$Database = "runs/nvidia-nim-v6-development-01.sqlite"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = Join-Path $projectRoot $Database
$seed = "3101"
$conditions = "full,evidence_only,journal_only,permuted_journal,neutral_journal"
$model = "nvidia/nemotron-3.5-lightning-30b-a3b"

if (-not (Test-Path $theta)) {
    throw "Project Theta is not installed in .venv. Run python -m pip install -e `".[nvidia]`" first."
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
$previousKey = $env:NVIDIA_API_KEY
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
    if (-not $env:NVIDIA_API_KEY) {
        throw "No NVIDIA API key was supplied."
    }

    $env:THETA_ENABLE_MODEL_RUNS = "YES"
    Write-Host "Project Theta NVIDIA NIM V6 development pilot"
    Write-Host "Database: $databasePath"
    Write-Host "Model: $model"
    Write-Host "Seed: $seed"
    Write-Host "Conditions: $conditions"
    Write-Host "Deterministic execution order: full,evidence_only,neutral_journal,permuted_journal,journal_only"
    Write-Host "Maximum hosted requests: 90"

    & $theta audit --experiment endogenous_agency_v6 --seeds $seed
    if ($LASTEXITCODE -ne 0) {
        throw "V6 schedule audit failed. No model request was sent."
    }
    & $theta doctor --adapter nvidia_nim --db "runs/nvidia-nim-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "NVIDIA NIM preflight failed. No model request was sent."
    }
    & $theta run `
        --config (Join-Path $projectRoot "configs\nvidia-nim-v6-development.json") `
        --experiment endogenous_agency_v6 `
        --seeds $seed `
        --conditions $conditions `
        --max-runs 5 `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "NVIDIA NIM V6 pilot failed. The partial database has been preserved."
    }
    & $theta audit `
        --experiment endogenous_agency_v6 `
        --seeds $seed `
        --conditions $conditions `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Post-run protocol audit failed. Results must not be interpreted."
    }
}
finally {
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else {
        $env:THETA_ENABLE_MODEL_RUNS = $previousGate
    }
    if ($keyWasEntered) {
        Remove-Item Env:NVIDIA_API_KEY -ErrorAction SilentlyContinue
    }
    elseif ($null -ne $previousKey) {
        $env:NVIDIA_API_KEY = $previousKey
    }
}

Write-Host "NVIDIA NIM V6 pilot completed."
