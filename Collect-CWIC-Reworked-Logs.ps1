# CWIC Reworked - assemble existing play-test logs without changing the game.
# Run once AFTER the integrated candidate has been tested inside HOI4.
$ErrorActionPreference = "Stop"

$documents = [Environment]::GetFolderPath("MyDocuments")
$desktop = [Environment]::GetFolderPath("Desktop")
$logs = Join-Path $documents "Paradox Interactive\Hearts of Iron IV\logs"
if (-not (Test-Path -LiteralPath $logs)) {
    throw "Hearts of Iron IV logs folder not found: $logs"
}
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$folder = Join-Path $desktop ("CWIC_Reworked_Test_" + $stamp)
New-Item -ItemType Directory -Path $folder -Force | Out-Null

$copied = @()
foreach ($filename in @("error.log", "game.log")) {
    $src = Join-Path $logs $filename
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $folder $filename)
        $copied += $filename
    }
}

$report = @'
CWIC Reworked - One-session QA report
======================================
Game version: 
Mod branch / commit: cwic-reworked / 
Enabled DLCs:
Workshop CWIC and other submods disabled? yes / no
Screen resolution:
HOI4 UI scale:

Syria 1949 focus tree:
Syria 1960 focus tree:
General research tabs in Syria:
General research tabs in other countries:
Syria-only research (12 technologies):
Grand doctrines / special forces:
Officer Corps / missing advisers / overlap:
Intelligence agency and agent portraits:
Syria-specific political/economic decisions:
At least one foreign acceptance/refusal response:
Economic decisions text and category banners:
Special Projects / Buran:
Other unexpected bugs:

Screenshots to attach separately (max 3):
1. Officer Corps
2. Research tree showing any empty tabs
3. Syrian decisions list

Privacy: Review logs before sharing. They can include your OS file paths,
computer username, launch arguments or other diagnostic data.
'@

[System.IO.File]::WriteAllText(
    (Join-Path $folder "CWIC_Test_Notes.txt"),
    $report,
    (New-Object System.Text.UTF8Encoding($true))
)

$zip = $folder + ".zip"
try {
    Compress-Archive -Path (Join-Path $folder "*") -DestinationPath $zip -CompressionLevel Optimal
    Write-Host "QA archive created: $zip" -ForegroundColor Green
} catch {
    Write-Warning "ZIP unavailable; the uncompressed report is still available."
}
Write-Host "Files copied: $($copied -join ', ')"
Write-Host "Review the report and logs for sensitive details before sharing."
Write-Host "No game, workshop, saves, or mod files were changed."
