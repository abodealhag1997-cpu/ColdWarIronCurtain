# Install CWIC Reworked from an existing GitHub checkout.
# This registers the MOD without modifying the Steam Workshop installation.
$ErrorActionPreference = "Stop"

$modPath = Join-Path $PSScriptRoot "Cold War Iron Curtain"
$descriptor = Join-Path $modPath "descriptor.mod"
if (-not (Test-Path -LiteralPath $descriptor)) {
    throw "Cannot find 'Cold War Iron Curtain/descriptor.mod'. Run this script from the repository root."
}

$documents = [Environment]::GetFolderPath("MyDocuments")
$modDirectory = Join-Path $documents "Paradox Interactive\Hearts of Iron IV\mod"
New-Item -ItemType Directory -Path $modDirectory -Force | Out-Null

$registration = Join-Path $modDirectory "CWIC_Reworked.mod"
$normalized = $modPath.Replace('\','/')
$raw = Get-Content -LiteralPath $descriptor -Raw -Encoding UTF8
$raw = [regex]::Replace($raw, '(?m)^\s*path\s*=.*\r?\n?', '')
$registrationContent = $raw.TrimEnd() + "`r`n" + 'path="' + $normalized + '"' + "`r`n"
[System.IO.File]::WriteAllText(
    $registration,
    $registrationContent,
    (New-Object System.Text.UTF8Encoding($true))
)

Write-Host ""
Write-Host "CWIC Reworked launcher entry installed:" -ForegroundColor Green
Write-Host $registration
Write-Host "Mod source: $modPath"
Write-Host "Keep this repository folder in the same location."
Write-Host "Launch HOI4 and enable ONLY CWIC Reworked for the test."
