Set-StrictMode -Version Latest

function Get-ProjectThetaNvidiaCredentialPath {
    if ($env:THETA_NVIDIA_CREDENTIAL_PATH) {
        return $env:THETA_NVIDIA_CREDENTIAL_PATH
    }
    if (-not $env:LOCALAPPDATA) {
        throw "LOCALAPPDATA is unavailable, so the NVIDIA credential cannot be stored securely."
    }
    return Join-Path $env:LOCALAPPDATA "ProjectTheta\credentials\nvidia-nim.xml"
}

function ConvertTo-ProjectThetaPlainText {
    param([Parameter(Mandatory = $true)][Security.SecureString]$SecureValue)

    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureValue)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    }
}

function Save-ProjectThetaNvidiaApiKey {
    param([Security.SecureString]$SecureKey)

    if ($null -eq $SecureKey) {
        $SecureKey = Read-Host "Paste the NVIDIA API key once (input is hidden)" -AsSecureString
    }
    $plainText = ConvertTo-ProjectThetaPlainText -SecureValue $SecureKey
    try {
        if ([string]::IsNullOrWhiteSpace($plainText)) {
            throw "No NVIDIA API key was supplied."
        }
    }
    finally {
        $plainText = $null
    }

    $credentialPath = Get-ProjectThetaNvidiaCredentialPath
    $credentialDirectory = Split-Path -Parent $credentialPath
    New-Item -ItemType Directory -Path $credentialDirectory -Force | Out-Null
    $credential = [Management.Automation.PSCredential]::new("NVIDIA_API_KEY", $SecureKey)
    $credential | Export-Clixml -LiteralPath $credentialPath -Force
    Write-Host "NVIDIA key saved with Windows user encryption. Future Project Theta runs will reuse it."
}

function Import-ProjectThetaNvidiaApiKey {
    if ($env:NVIDIA_API_KEY) {
        return $false
    }

    $credentialPath = Get-ProjectThetaNvidiaCredentialPath
    if (-not (Test-Path -LiteralPath $credentialPath)) {
        Save-ProjectThetaNvidiaApiKey
    }

    try {
        $credential = Import-Clixml -LiteralPath $credentialPath
        if ($credential -isnot [Management.Automation.PSCredential]) {
            throw "The saved credential has an unexpected format."
        }
        $env:NVIDIA_API_KEY = $credential.GetNetworkCredential().Password
    }
    catch {
        throw "The saved NVIDIA key could not be decrypted for this Windows account. Run .\scripts\manage_nvidia_key.ps1 -Action Set to replace it."
    }

    if (-not $env:NVIDIA_API_KEY) {
        throw "The saved NVIDIA credential was empty. Run .\scripts\manage_nvidia_key.ps1 -Action Set to replace it."
    }
    Write-Host "Loaded the saved NVIDIA key for this run."
    return $true
}

function Remove-ProjectThetaNvidiaApiKey {
    $credentialPath = Get-ProjectThetaNvidiaCredentialPath
    if (Test-Path -LiteralPath $credentialPath) {
        Remove-Item -LiteralPath $credentialPath -Force
        Write-Host "Removed the saved NVIDIA key."
    }
    else {
        Write-Host "No saved NVIDIA key was found."
    }
}

