$OutputEncoding = [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$backupRoot = "D:\Backups\benino"
$destination = "d:\_PAL\benino"

Write-Host "=== Benino Restore ===" -ForegroundColor Cyan

# Check if backup directory exists
if (-not (Test-Path $backupRoot)) {
    Write-Host "Backup directory not found: $backupRoot" -ForegroundColor Red
    Start-Sleep -Seconds 3
    exit 1
}

# List available backups (newest first)
$backups = Get-ChildItem $backupRoot -Directory | Sort-Object Name -Descending
if ($backups.Count -eq 0) {
    Write-Host "No backups found in $backupRoot" -ForegroundColor Red
    Start-Sleep -Seconds 3
    exit 1
}

Write-Host "`nAvailable backups:" -ForegroundColor Yellow
for ($i = 0; $i -lt [Math]::Min($backups.Count, 10); $i++) {
    $size = (Get-ChildItem $backups[$i].FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "  [$i] $($backups[$i].Name)  ($([math]::Round($size, 1)) MB)"
}

Write-Host "`nSelect backup number (0 = latest):" -ForegroundColor Yellow
$selection = Read-Host
$index = [int]$selection

if ($index -lt 0 -or $index -ge $backups.Count) {
    Write-Host "Invalid selection." -ForegroundColor Red
    Start-Sleep -Seconds 3
    exit 1
}

$selected = $backups[$index]
Write-Host "`nWARNING: This will overwrite $destination with backup:" -ForegroundColor Red
Write-Host "  $($selected.Name)" -ForegroundColor Yellow
Write-Host "Continue? (y/n)"
$response = Read-Host

if ($response -eq 'y') {
    # Restore using robocopy (mirror mode, skip same exclusions)
    $excludeDirs = @('node_modules', '.git', '.pnpm-store', 'nanobot-env', '.claude')

    robocopy $selected.FullName $destination /E /XD $excludeDirs /NFL /NDL /NJH /NJS /NC /NS /NP

    if ($LASTEXITCODE -le 3) {
        Write-Host "Restore complete from: $($selected.Name)" -ForegroundColor Green
    } else {
        Write-Host "Restore failed! (robocopy exit code: $LASTEXITCODE)" -ForegroundColor Red
    }
} else {
    Write-Host "Cancelled." -ForegroundColor Yellow
}

Start-Sleep -Seconds 3
