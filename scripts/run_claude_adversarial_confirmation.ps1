param(
    [string]$Database = "runs/claude-adversarial-confirmation.sqlite",
    [double]$StudyBudgetUsd = 0.95
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
$seed = 209
$conditions = @("sham_body", "full", "shuffled_interoception")
$conditionReserveUsd = 0.32
$previousApiKey = $env:ANTHROPIC_API_KEY
$previousModelGate = $env:THETA_ENABLE_MODEL_RUNS
$secureKey = $null
$credential = $null
$plainKey = $null

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta virtual environment was not found at $theta"
}
if ($StudyBudgetUsd -le 0 -or $StudyBudgetUsd -gt 0.95) {
    throw "StudyBudgetUsd must be greater than zero and no more than 0.95. Nothing was charged."
}
if (Test-Path -LiteralPath $databasePath) {
    if ($PSBoundParameters.ContainsKey("Database")) {
        throw "Confirmation database already exists at $databasePath. Nothing was charged."
    }
    $suffix = 2
    do {
        $databasePath = Join-Path $projectRoot "runs/claude-adversarial-confirmation-$suffix.sqlite"
        $suffix += 1
    } while (Test-Path -LiteralPath $databasePath)
    Write-Host "Previous confirmation database preserved. New results will use $databasePath"
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

    Write-Host "Confirmation database: $databasePath"
    Write-Host "Frozen seed: $seed"
    Write-Host "Frozen condition order: $($conditions -join ', ')"
    Write-Host "Confirmation API budget: `$$($StudyBudgetUsd.ToString('0.00')) USD"

    & $theta audit --seeds $seed
    if ($LASTEXITCODE -ne 0) {
        throw "Schedule audit failed. No model run was started."
    }
    & $theta doctor --adapter anthropic --db "runs/claude-live-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude preflight failed. No confirmation was started."
    }

    $completed = 0
    foreach ($condition in $conditions) {
        if ($completed -gt 0) {
            $reportText = (& $theta report --db $databasePath --json) -join "`n"
            if ($LASTEXITCODE -ne 0) {
                throw "Could not read cumulative cost. Confirmation stopped conservatively."
            }
            $spent = [double](($reportText | ConvertFrom-Json).estimated_api_cost_usd)
            if (($spent + $conditionReserveUsd) -gt $StudyBudgetUsd) {
                Write-Host "Budget stop before $condition. Estimated spend: `$$($spent.ToString('0.0000')) USD"
                break
            }
        }

        Write-Host "Starting $condition ($($completed + 1) of $($conditions.Count))"
        & $theta run `
            --config "configs/claude-adversarial-confirmation.json" `
            --conditions $condition `
            --seeds $seed `
            --max-runs 1 `
            --db $databasePath
        if ($LASTEXITCODE -ne 0) {
            throw "Confirmation failed in $condition. Preserved data will not be retried automatically."
        }
        $completed += 1
    }

    & $theta report --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Confirmation completed but report generation failed."
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
