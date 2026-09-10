param(
    [string]$Database = "runs/ollama-v6-development-01.sqlite"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = Join-Path $projectRoot $Database
$seed = "3101"
$conditions = "full,evidence_only,journal_only,permuted_journal,neutral_journal"
$model = "qwen3:8b"

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv. Run python -m pip install -e . first."
}
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    throw "Ollama is not installed. Install it from https://ollama.com/download/windows"
}

$installedModels = & ollama list
if ($LASTEXITCODE -ne 0) {
    throw "Ollama is installed but its local service is not responding. Start Ollama and retry."
}
if (-not ($installedModels -match '^qwen3:8b\s')) {
    throw "The local model is missing. Run: ollama pull qwen3:8b"
}

$parent = Split-Path -Parent $databasePath
New-Item -ItemType Directory -Force -Path $parent | Out-Null
if (Test-Path -LiteralPath $databasePath) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($databasePath)
    $extension = [System.IO.Path]::GetExtension($databasePath)
    $index = 2
    do {
        $candidate = Join-Path $parent "$stem-$index$extension"
        $index += 1
    } while (Test-Path -LiteralPath $candidate)
    $databasePath = $candidate
}

$previousGate = $env:THETA_ENABLE_MODEL_RUNS
try {
    $env:THETA_ENABLE_MODEL_RUNS = "YES"
    Write-Host "Project Theta local Ollama V6 development pilot"
    Write-Host "Database: $databasePath"
    Write-Host "Model: $model"
    Write-Host "Seed: $seed"
    Write-Host "Conditions: $conditions"
    Write-Host "Maximum local decisions: 90"
    Write-Host "Provider API requests: 0"

    & $theta audit --experiment endogenous_agency_v6 --seeds $seed
    if ($LASTEXITCODE -ne 0) {
        throw "V6 schedule audit failed. No model decision was requested."
    }
    & $theta run `
        --config (Join-Path $projectRoot "configs\ollama-v6-development.json") `
        --experiment endogenous_agency_v6 `
        --seeds $seed `
        --conditions $conditions `
        --max-runs 5 `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Local Ollama V6 pilot failed. The partial database has been preserved."
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
}

Write-Host "Local Ollama V6 pilot completed."
