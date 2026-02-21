$OutputEncoding = [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$source = "d:\_PAL\benino\agent-network"
$destination = "D:\Backups\agent-network\agent-network-$date"

Write-Host "Starting Agent Network Backup... ($date)" -ForegroundColor Cyan

# Exclude patterns
$excludeDirs = @('node_modules', '.git', 'dist', 'coverage', 'playwright-report', 'test-results', 'tmp', 'temp', '.claude')
$excludeFiles = @('*.log', '*.tmp', '*.env', '*.env.local', '*.env.production', 'package-lock.json')

Write-Host "Source: $source"
Write-Host "Destination: $destination"

# Create backup using robocopy
robocopy $source $destination /E /XD $excludeDirs /XF $excludeFiles /NFL /NDL /NJH /NJS /NC /NS /NP

if ($LASTEXITCODE -le 3) {
    $size = (Get-ChildItem $destination -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "Backup successful! ($([math]::Round($size, 1)) MB)" -ForegroundColor Green
    Write-Host "Location: $destination"
} else {
    Write-Host "Backup failed! (robocopy exit code: $LASTEXITCODE)" -ForegroundColor Red
}

Start-Sleep -Seconds 3
