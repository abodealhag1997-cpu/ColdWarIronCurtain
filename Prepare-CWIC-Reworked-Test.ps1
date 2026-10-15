# CWIC Reworked beta: fetch only the active mod folder, register it locally.
# This script never deletes or overwrites files in Steam Workshop.
$ErrorActionPreference = "Stop"
$remote = "https://github.com/abodealhag1997-cpu/ColdWarIronCurtain.git"
$destination = Join-Path $env:USERPROFILE "CWIC_Reworked_Test"
$branch = "cwic-reworked"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git for Windows is required: https://git-scm.com/download/win" -ForegroundColor Yellow
    throw "Install Git, restart PowerShell, then run this script again."
}
if (Test-Path -LiteralPath $destination) {
    throw "The target folder already exists: $destination. Nothing was overwritten."
}

Write-Host "Downloading CWIC Reworked beta (sparse checkout)." -ForegroundColor Cyan
Write-Host "This downloads only the mod folder, not the massive backup folders."
Write-Host "Target: $destination"
Write-Host "It may still take a long time and require several GB of disk space."

& git clone --depth 1 --filter=blob:none --sparse --single-branch --branch $branch $remote $destination
if ($LASTEXITCODE -ne 0) {
    throw "Git clone failed. Inspect the terminal output and the target folder."
}
& git -C $destination sparse-checkout set "Cold War Iron Curtain"
if ($LASTEXITCODE -ne 0) {
    throw "Git sparse checkout failed. The Steam Workshop copy is unchanged."
}

$descriptor = Join-Path $destination "Cold War Iron Curtain\descriptor.mod"
$installer = Join-Path $destination "Install-CWIC-Reworked.ps1"
if (-not (Test-Path -LiteralPath $descriptor) -or -not (Test-Path -LiteralPath $installer)) {
    throw "Required mod files missing after download; no launcher entry was installed."
}
Write-Host "Registering CWIC Reworked in the HOI4 launcher..." -ForegroundColor Cyan
& $installer

Write-Host ""
Write-Host "INSTALLATION COMPLETE (NOT GAMEPLAY-TESTED)" -ForegroundColor Green
Write-Host "In the HOI4 launcher, select a new playset and enable ONLY:"
Write-Host "CWIC Reworked (HOI4 1.19)"
Write-Host "Do not enable the original Cold War Iron Curtain at the same time."
Write-Host "The Workshop mod and saves were not changed."
