param(
    [string]$Database = "runs/nvidia-nim-v6-gpt-oss-replication-01.sqlite",
    [switch]$Recover
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$spec = Join-Path $projectRoot "workers\nvidia-nim-v6-gpt-oss-replication-01.json"
$databasePath = if ([System.IO.Path]::IsPathRooted($Database)) {
    $Database
} else {
    Join-Path $projectRoot $Database
}
$seedText = "3329,3350,3221,3265,3657,3893,3363,3242,3324,3749,4003,3417,3268,3397,3838"
$conditionText = "full,evidence_only,journal_only,permuted_journal,neutral_journal"
$previousDatabase = $env:THETA_DATABASE
$previousGate = $env:THETA_ENABLE_MODEL_RUNS
$keyWasEntered = $false

if (-not (Test-Path -LiteralPath $theta)) {
    throw "Project Theta is not installed in .venv. Run python -m pip install -e . first."
}
if (-not (Test-Path -LiteralPath $spec)) {
    throw "Frozen replication worker specification is missing at $spec"
}

try {
    Set-Location -LiteralPath $projectRoot
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

    $env:THETA_DATABASE = $databasePath
    $env:THETA_ENABLE_MODEL_RUNS = "YES"

    Write-Host "Project Theta NVIDIA GPT OSS V6 replication 01"
    Write-Host "Database: $databasePath"
    Write-Host "Fresh paired seeds: 15"
    Write-Host "Conditions per seed: 5"
    Write-Host "Maximum hosted requests: 1350"
    Write-Host "Resume mode: $($Recover.IsPresent)"

    & $theta audit --experiment endogenous_agency_v6 --seeds $seedText
    if ($LASTEXITCODE -ne 0) {
        throw "Replication schedule audit failed. No model request was sent."
    }
    & $theta doctor --adapter nvidia_nim --db "runs/nvidia-nim-replication-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "NVIDIA NIM preflight failed. No model request was sent."
    }

    $workerArguments = @("worker", "--spec", $spec)
    if ($Recover) { $workerArguments += "--recover" }
    & $theta @workerArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Replication paused or failed. Completed jobs remain preserved in $databasePath"
    }

    & $theta audit --experiment endogenous_agency_v6 --seeds $seedText `
        --conditions $conditionText --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Post-run replication audit failed. Results must not be interpreted."
    }
    & $theta report --db $databasePath
    Write-Host "NVIDIA GPT OSS V6 replication 01 completed."
}
finally {
    if ($null -eq $previousDatabase) {
        Remove-Item Env:THETA_DATABASE -ErrorAction SilentlyContinue
    }
    else { $env:THETA_DATABASE = $previousDatabase }
    if ($null -eq $previousGate) {
        Remove-Item Env:THETA_ENABLE_MODEL_RUNS -ErrorAction SilentlyContinue
    }
    else { $env:THETA_ENABLE_MODEL_RUNS = $previousGate }
    if ($keyWasEntered) { Remove-Item Env:NVIDIA_API_KEY -ErrorAction SilentlyContinue }
    Set-Location -LiteralPath $previousLocation
}
