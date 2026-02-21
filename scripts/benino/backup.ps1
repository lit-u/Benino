$OutputEncoding = [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

Write-Host "=== Benino Full Backup ===" -ForegroundColor Cyan
Write-Host "Timestamp: $date`n"

# === BENINO (visas monorepo) ===
$beninoSrc = "d:\_PAL\benino"
$beninoDst = "D:\Backups\benino\benino-$date"

Write-Host "[1/2] Benino monorepo..." -ForegroundColor Yellow
$excludeDirs = @('node_modules', '.git', '.pnpm-store', 'dist', 'coverage', 'tmp', 'temp', 'playwright-report', 'test-results', '__screenshots__', '.build', 'vendor', 'nanobot-env', '.claude')
$excludeFiles = @('*.log', '*.tmp', '*.env', '*.env.local', '*.env.production', 'pnpm-lock.yaml', 'bun.lock', 'bun.lockb', 'package-lock.json')

robocopy $beninoSrc $beninoDst /E /XD $excludeDirs /XF $excludeFiles /NFL /NDL /NJH /NJS /NC /NS /NP

if ($LASTEXITCODE -le 3) {
    $size = (Get-ChildItem $beninoDst -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "  OK ($([math]::Round($size, 1)) MB) -> $beninoDst" -ForegroundColor Green
} else {
    Write-Host "  FAILED (exit code: $LASTEXITCODE)" -ForegroundColor Red
}

# === AGENT NETWORK (atskiras) ===
$agentSrc = "d:\_PAL\benino\agent-network"
$agentDst = "D:\Backups\agent-network\agent-network-$date"

Write-Host "[2/2] Agent Network..." -ForegroundColor Yellow
$agentExcludeDirs = @('node_modules', '.git', 'dist', 'coverage', 'playwright-report', 'test-results', 'tmp', 'temp', '.claude')

robocopy $agentSrc $agentDst /E /XD $agentExcludeDirs /XF $excludeFiles /NFL /NDL /NJH /NJS /NC /NS /NP

if ($LASTEXITCODE -le 3) {
    $size = (Get-ChildItem $agentDst -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "  OK ($([math]::Round($size, 1)) MB) -> $agentDst" -ForegroundColor Green
} else {
    Write-Host "  FAILED (exit code: $LASTEXITCODE)" -ForegroundColor Red
}

Write-Host "`n=== Backup Complete ===" -ForegroundColor Cyan
Start-Sleep -Seconds 3
