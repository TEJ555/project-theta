param(
    [string]$Database = "runs/claude-replication.sqlite",
    [double]$StudyBudgetUsd = 4.20
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$databasePath = if ([System.IO.Path]::IsPathRooted($Database)) {
    $Database
} else {
    Join-Path $projectRoot $Database
}
$seeds = @(22, 33, 44, 55, 66, 77)
$bundleReserveUsd = 0.84
$previousApiKey = $env:ANTHROPIC_API_KEY
$previousModelGate = $env:THETA_ENABLE_MODEL_RUNS
$secureKey = $null
$credential = $null
$plainKey = $null

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta virtual environment was not found at $theta"
}
if ($StudyBudgetUsd -le 0 -or $StudyBudgetUsd -gt 4.20) {
    throw "StudyBudgetUsd must be greater than zero and no more than 4.20. Nothing was charged."
}
if (Test-Path -LiteralPath $databasePath) {
    if ($PSBoundParameters.ContainsKey("Database")) {
        throw "Replication database already exists at $databasePath. Nothing was charged. Pass -Database with a new filename."
    }
    $suffix = 2
    do {
        $databasePath = Join-Path $projectRoot "runs/claude-replication-$suffix.sqlite"
        $suffix += 1
    } while (Test-Path -LiteralPath $databasePath)
    Write-Host "Previous replication database preserved. New results will use $databasePath"
}

try {
    $secureKey = Read-Host "Paste the Claude Console API key (input is hidden)" -AsSecureString
    $credential = [System.Net.NetworkCredential]::new("theta", $secureKey)
    $plainKey = $credential.Password
    if ([string]::IsNullOrWhiteSpace($plainKey)) {
        throw "No API key was entered. Nothing was charged."
    }

    Set-Location -LiteralPath $projectRoot
    $env:ANTHROPIC_API_KEY = $plainKey
    $env:THETA_ENABLE_MODEL_RUNS = "YES"

    Write-Host "Replication database: $databasePath"
    Write-Host "Frozen seeds: $($seeds -join ', ')"
    Write-Host "Replication API budget: `$$($StudyBudgetUsd.ToString('0.00')) USD"

    & $theta doctor --adapter anthropic --db "runs/claude-live-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude preflight failed; no replication was started."
    }

    $completedBundles = 0
    foreach ($seed in $seeds) {
        if ($completedBundles -gt 0) {
            $reportText = (& $theta report --db $databasePath --json) -join "`n"
            if ($LASTEXITCODE -ne 0) {
                throw "Could not read cumulative cost; replication stopped conservatively."
            }
            $spent = [double](($reportText | ConvertFrom-Json).estimated_api_cost_usd)
            if (($spent + $bundleReserveUsd) -gt $StudyBudgetUsd) {
                Write-Host "Budget stop before seed $seed. Estimated replication spend: `$$($spent.ToString('0.0000')) USD"
                break
            }
        }

        Write-Host "Starting matched seed $seed ($($completedBundles + 1) of $($seeds.Count))"
        & $theta run `
            --config "configs/claude-replication.json" `
            --seeds $seed `
            --max-runs 3 `
            --db $databasePath
        if ($LASTEXITCODE -ne 0) {
            throw "Replication failed at seed $seed. Preserved data will not be retried automatically."
        }
        $completedBundles += 1
    }

    & $theta report --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Replication completed but report generation failed."
    }
}
finally {
    if ($null -eq $previousApiKey) {
        Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    } else {
        $env:ANTHROPIC_API_KEY = $previousApiKey
    }
    if ($null -eq $previousModelGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    } else {
        $env:THETA_ENABLE_MODEL_RUNS = $previousModelGate
    }
    $plainKey = $null
    $credential = $null
    $secureKey = $null
    Set-Location -LiteralPath $previousLocation
}
