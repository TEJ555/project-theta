param(
    [string]$Database = "runs/nvidia-nim-v8-gpt-oss-replication-01.sqlite",
    [switch]$Recover
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousLocation = (Get-Location).Path
$theta = Join-Path $projectRoot ".venv\Scripts\theta.exe"
$spec = Join-Path $projectRoot "workers\nvidia-nim-v8-gpt-oss-replication-01.json"
$databasePath = if ([System.IO.Path]::IsPathRooted($Database)) {
    $Database
} else {
    Join-Path $projectRoot $Database
}
$seedText = "5201,5202,5203,5204,5205,5206,5207,5216,5226,5231,5237,5250"
$conditionText = "full,no_memory,shuffled_interoception,no_body"
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

    Write-Host "Project Theta NVIDIA GPT OSS V8 replication 01"
    Write-Host "Database: $databasePath"
    Write-Host "Fresh paired seeds: 12"
    Write-Host "Conditions per seed: 4"
    Write-Host "Maximum hosted requests: 1152"
    Write-Host "Resume mode: $($Recover.IsPresent)"

    & $theta audit --experiment active_interoceptive_control_v8 --seeds $seedText
    if ($LASTEXITCODE -ne 0) {
        throw "Replication schedule audit failed. No model request was sent."
    }
    & $theta doctor --adapter nvidia_nim --db "runs/nvidia-nim-v8-replication-doctor.sqlite"
    if ($LASTEXITCODE -ne 0) {
        throw "NVIDIA NIM preflight failed. No model request was sent."
    }

    $workerArguments = @("worker", "--spec", $spec)
    if ($Recover) { $workerArguments += "--recover" }
    & $theta @workerArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Replication paused or failed. Completed jobs remain preserved in $databasePath"
    }

    & $theta audit --experiment active_interoceptive_control_v8 --seeds $seedText `
        --conditions $conditionText --db $databasePath
    if ($LASTEXITCODE -ne 0) {
        throw "Post-run replication audit failed. Results must not be interpreted."
    }
    & $theta report --db $databasePath
    Write-Host "NVIDIA GPT OSS V8 replication 01 completed."
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
