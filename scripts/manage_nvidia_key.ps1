param(
    [ValidateSet("Set", "Remove", "Status")]
    [string]$Action = "Status"
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "nvidia_key.ps1")

switch ($Action) {
    "Set" {
        Save-ProjectThetaNvidiaApiKey
    }
    "Remove" {
        Remove-ProjectThetaNvidiaApiKey
    }
    "Status" {
        $credentialPath = Get-ProjectThetaNvidiaCredentialPath
        if (Test-Path -LiteralPath $credentialPath) {
            Write-Host "A Windows-encrypted NVIDIA key is saved for this account."
        }
        else {
            Write-Host "No saved NVIDIA key was found. The next NVIDIA run will ask once and save it."
        }
    }
}

