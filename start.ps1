# JanMitra AI - Launch Script

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "       Starting JanMitra AI Suite        " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Get base directory of the script
$BaseDir = $PSScriptRoot
if (-not $BaseDir) {
    $BaseDir = Get-Location
}

# 1. Start FastAPI Backend in background
Write-Host "[1/3] Launching FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", ".\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload" -WorkingDirectory $BaseDir -WindowStyle Normal

# 2. Wait 2 seconds for backend boot
Start-Sleep -Seconds 2

# 3. Start React Frontend
Write-Host "[2/3] Launching React Dev Server on http://localhost:5173..." -ForegroundColor Green
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "npm run dev" -WorkingDirectory "$BaseDir\frontend" -WindowStyle Normal

# 4. Open Application in Web Browser
Write-Host "[3/3] Opening JanMitra Assistant in your browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:5173"

Write-Host "JanMitra AI runs successfully!" -ForegroundColor Cyan
Write-Host "Check the opened terminal windows to see logs for backend & frontend." -ForegroundColor DarkGray
