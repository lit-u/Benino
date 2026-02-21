$OutputEncoding = [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$source = "d:\_PAL\benino"
$destination = "D:\Backups\benino\benino-$date"

Write-Host "Starting Benino Backup... ($date)" -ForegroundColor Cyan

# Exclude patterns (node_modules, .git, temp, build artifacts)
$exclude = @(
    'node_modules', '.git', '.pnpm-store', 'dist', 'coverage',
    'tmp', 'temp', '.env', '*.log', 'playwright-report',
    'test-results', '__screenshots__', '.build', 'vendor',
    'nanobot-env', '.claude'
)

# Build robocopy exclude dirs and files
$excludeDirs = $exclude | ForEach-Object { $_ }
$excludeFiles = @('*.log', '*.tmp', '*.env', '*.env.local', '*.env.production', 'pnpm-lock.yaml', 'bun.lock', 'bun.lockb', 'package-lock.json')

Write-Host "Source: $source"
Write-Host "Destination: $destination"

# Create backup using robocopy (fast, skips junk)
robocopy $source $destination /E /XD $excludeDirs /XF $excludeFiles /NFL /NDL /NJH /NJS /NC /NS /NP

if ($LASTEXITCODE -le 3) {
    $size = (Get-ChildItem $destination -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "Backup successful! ($([math]::Round($size, 1)) MB)" -ForegroundColor Green
    Write-Host "Location: $destination"
} else {
    Write-Host "Backup failed! (robocopy exit code: $LASTEXITCODE)" -ForegroundColor Red
}

Start-Sleep -Seconds 3
