# Sentinel Demo Launcher

Write-Host "Starting Sentinel..." -ForegroundColor Green

# 1. Check for API Key
if (-not $env:GOOGLE_API_KEY) {
    Write-Host "WARNING: GOOGLE_API_KEY environment variable not found." -ForegroundColor Yellow
    Write-Host "AI features will not work without it." -ForegroundColor Yellow
}

# 2. Start Backend Engine (Background)
Write-Host "Starting Sentinel Engine (Pathway on WSL)..." -ForegroundColor Cyan
# Use WSL python3 to run the Pathway app
$backend = Start-Process wsl -ArgumentList "-d", "Ubuntu", "python3", "src/pathway_app.py" -PassThru -WindowStyle Minimized

# 3. Start Streamlit Dashboard
Write-Host "Starting Streamlit Dashboard (dashboard/main.py)..." -ForegroundColor Cyan
# Use venv streamlit
Start-Process ".venv\Scripts\streamlit.exe" -ArgumentList "run dashboard/main.py"

Write-Host "Demo is running!" -ForegroundColor Green
Write-Host "Backend PID: $($backend.Id)"
Write-Host "Press any key to stop the backend..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Stop-Process -Id $backend.Id -Force
Write-Host "Backend stopped." -ForegroundColor Green
