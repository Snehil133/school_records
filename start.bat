@echo off
echo 🎓 Student Information System
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Navigate to backend directory
cd backend

REM Install requirements
echo 📦 Installing requirements...
pip install -r requirements.txt

REM Start backend server
echo 🚀 Starting backend server...
start "Backend Server" python app.py

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Navigate back to root
cd ..

REM Start frontend server (optional)
echo 🌐 Starting frontend server (optional)...
cd frontend
start "Frontend Server" python -m http.server 8000

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Open browser to main application
echo 🌍 Opening application in browser...
start http://localhost:5000

echo.
echo 🎉 Application is ready!
echo 📱 Main Application: http://localhost:5000
echo 🌐 Legacy Frontend: http://localhost:8000 (redirects to main)
echo.
echo 🔐 Login Credentials:
echo    Principal: username=principal, password=principal123
echo    Teacher: username=teacher1, password=teacher123
echo.
echo Press any key to stop the servers...
pause >nul

REM Stop servers
taskkill /f /im python.exe >nul 2>&1
echo ✅ Servers stopped!
pause 