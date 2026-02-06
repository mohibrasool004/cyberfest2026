# monitor_training.ps1
# Usage: .\train_logs\monitor_training.ps1 -IntervalSeconds 120
param(
    [int]$IntervalSeconds = 120
)

$metrics = Join-Path (Get-Location) 'train_stats/evaluation_metrics.txt'
$runlog = Join-Path (Get-Location) 'train_logs/run.log'

Write-Host "Monitoring training (metrics: $metrics, run log: $runlog) - interval ${IntervalSeconds}s"
while ($true) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "`n=== $ts ==="
    if (Test-Path $metrics) {
        Write-Host "-- Metrics (tail 10):"
        Get-Content $metrics -Tail 10 | ForEach-Object { Write-Host "  $_" }
    } else {
        Write-Host "-- Metrics file not present yet. Showing run log tail (50 lines):"
        if (Test-Path $runlog) { Get-Content $runlog -Tail 50 | ForEach-Object { Write-Host "  $_" } } else { Write-Host "  No run.log yet." }
    }
    Start-Sleep -Seconds $IntervalSeconds
}
