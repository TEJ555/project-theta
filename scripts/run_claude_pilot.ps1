param(
    [string]$Database = "runs/claude-pilot.sqlite"
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
$previousApiKey = $env:ANTHROPIC_API_KEY
$previousModelGate = $env:THETA_ENABLE_MODEL_RUNS
$secureKey = $null
$credential = $null
$plainKey = $null

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta virtual environment was not found at $theta"
}

if (Test-Path -LiteralPath $databasePath) {
    throw "Pilot database already exists at $databasePath. Nothing was charged. Move it or pass -Database with a new filename."
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

    & $theta doctor --adapter anthropic --db "runs/claude-live-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "Claude preflight failed; no pilot was started."
    }

    & $theta run `
        --config "configs/claude-pilot.json" `
        --seeds 11 `
        --max-runs 3 `
        --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Claude pilot failed. Check the preserved database and provider status."
    }

    & $theta report --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Pilot completed but report generation failed."
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
