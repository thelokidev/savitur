Write-Host "Starting PyJHora Web Application..." -ForegroundColor Cyan
Write-Host "=" * 50

Write-Host "`nChecking for existing servers..." -ForegroundColor Yellow
$backendRunning = Test-NetConnection -ComputerName localhost -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue
$frontendRunning = Test-NetConnection -ComputerName localhost -Port 9002 -InformationLevel Quiet -WarningAction SilentlyContinue

if ($backendRunning) {
    Write-Host "`nBackend detected on port 8000. Restarting..." -ForegroundColor Yellow
    $backendProcs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*uvicorn*main:app*' }
    foreach ($p in $backendProcs) { Try { Stop-Process -Id $p.ProcessId -Force } Catch {} }
    Start-Sleep -Seconds 1
}

Write-Host "`nStarting Backend (FastAPI on port 8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd web-app\backend; python -m uvicorn main:app --host 0.0.0.0 --port 8000" -WindowStyle Normal
Start-Sleep -Seconds 3

if ($frontendRunning) {
    Write-Host "`nFrontend detected on port 9002. Restarting..." -ForegroundColor Yellow
    $frontendProcs = Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -like '*web-app\\frontend*') -and (($_.CommandLine -like '*next dev*') -or ($_.CommandLine -like '*npm run dev*')) }
    foreach ($p in $frontendProcs) { Try { Stop-Process -Id $p.ProcessId -Force } Catch {} }
    Start-Sleep -Seconds 1
}

$lockPath = Join-Path "web-app\frontend" ".next\dev\lock"
if (Test-Path $lockPath) { Try { Remove-Item $lockPath -Force } Catch {} }

Write-Host "`nStarting Frontend (Next.js on port 9002)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd web-app\frontend; npm run dev" -WindowStyle Normal
Start-Sleep -Seconds 2

Write-Host "`n" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host "Servers Starting!" -ForegroundColor Green
Write-Host "=" * 50
Write-Host "`nBackend API:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Docs:     http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Frontend App: http://localhost:9002" -ForegroundColor Yellow
Write-Host "`nPress Ctrl+C in each terminal window to stop the servers" -ForegroundColor Cyan
