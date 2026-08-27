param(
    [string]$Database = "runs/claude-max-independent-pilot-01.sqlite"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = Join-Path $projectRoot $Database
$seed = "509"
$conditions = "matched_sham,full,shuffled_interoception"

if (-not (Test-Path $theta)) {
    throw "Project Theta is not installed in .venv. Run python -m pip install -e . first."
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

Write-Host "Claude Max Independent Theta pilot 01"
Write-Host "Database: $databasePath"
Write-Host "Seed: $seed"
Write-Host "Frozen order: $conditions"
Write-Host "Maximum subscription prompts: 180"
Write-Host "Metered API use: blocked"

$previousGate = $env:THETA_ENABLE_MODEL_RUNS
try {
    $env:THETA_ENABLE_MODEL_RUNS = "YES"
    & $theta audit --experiment independent_theta --seeds $seed
    if ($LASTEXITCODE -ne 0) {
        throw "Independent Theta schedule audit failed. No model prompt was sent."
    }
    & $theta doctor --adapter claude_code --db "runs/claude-max-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max preflight failed. No model prompt was sent."
    }
    & $theta run `
        --config (Join-Path $projectRoot "configs\claude-max-independent-03.json") `
        --experiment independent_theta `
        --seeds $seed `
        --conditions $conditions `
        --max-runs 3 `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Claude Max pilot failed. The partial database has been preserved."
    }
    & $theta audit `
        --experiment independent_theta `
        --seeds $seed `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Post-run protocol identity audit failed. Results must not be interpreted."
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

Write-Host "Claude Max pilot completed."
