$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = Join-Path $projectRoot "runs\endogenous-agency-v6-local-validation-01.sqlite"
$pooledDatabasePath = Join-Path $projectRoot "runs\endogenous-agency-v6-pooled-baseline-01.sqlite"
$primarySeeds = (2100..2199) -join ","
$pooledSeeds = (2300..2499) -join ","

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv."
}

try {
    Set-Location -LiteralPath $projectRoot
    & $theta audit --experiment endogenous_agency_v6 --seeds $primarySeeds
    if ($LASTEXITCODE -ne 0) {
        throw "V6 schedule audit failed."
    }
    & $theta run `
        --experiment endogenous_agency_v6 `
        --seeds $primarySeeds `
        --conditions "full,evidence_only,journal_only,permuted_journal,neutral_journal" `
        --config "configs\endogenous-agency-v6-local.json" `
        --db $databasePath `
        --max-runs 500
    if ($LASTEXITCODE -ne 0) {
        throw "V6 local validation failed."
    }
    & $theta run `
        --experiment endogenous_agency_v6 `
        --seeds $pooledSeeds `
        --conditions "journal_only" `
        --config "configs\endogenous-agency-v6-local.json" `
        --model "pooled-correlation-baseline-v1" `
        --db $pooledDatabasePath `
        --max-runs 200
    if ($LASTEXITCODE -ne 0) {
        throw "V6 pooled-correlation baseline failed."
    }
    & $theta audit `
        --experiment endogenous_agency_v6 `
        --seeds $primarySeeds `
        --conditions "full,evidence_only,journal_only,permuted_journal,neutral_journal" `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "V6 execution audit failed."
    }
    & $theta report --db $databasePath --db $pooledDatabasePath
}
finally {
    Set-Location -LiteralPath $previousLocation
}
