param(
    [string]$Database = "runs/independent-theta-validation.sqlite",
    [string]$Seeds = "401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = Join-Path $projectRoot $Database

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

Write-Host "Independent Theta local validation"
Write-Host "Database: $databasePath"
Write-Host "Seeds: $Seeds"
Write-Host "API use: none"

& $theta audit --experiment independent_theta --seeds $Seeds
if ($LASTEXITCODE -ne 0) {
    throw "Schedule audit failed. No validation runs were started."
}

& $theta run `
    --config (Join-Path $projectRoot "configs\independent-theta-scripted.json") `
    --experiment independent_theta `
    --seeds $Seeds `
    --conditions full,matched_sham,shuffled_interoception,no_body `
    --max-runs 80 `
    --db $databasePath
if ($LASTEXITCODE -ne 0) {
    throw "Local validation failed. The partial database has been preserved."
}

Write-Host "Local validation completed."
