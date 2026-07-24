@echo off
setlocal enabledelayedexpansion

:: Vivara - Windows Batch Launcher

set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"

set "BACKEND=%ROOT%\backend"
set "FRONTEND=%ROOT%\frontend"
set "VENV=%BACKEND%\venv"
set "PIP=%VENV%\Scripts\pip.exe"
set "PYTHON=%VENV%\Scripts\python.exe"

echo.
echo  Vivara - Free AI Video Studio
echo  100%% Local, 100%% Free
echo  ================================
echo.

:: -------------------------------------------------------
:: Prerequisite checks
:: -------------------------------------------------------

echo [Step 1/5] Checking prerequisites...
echo.

python --version
if errorlevel 1 (
    echo  [MISSING] Python not found
    echo            Download from: https://python.org/downloads
    goto :fail
) else (
    echo  [OK] Python found
)

echo.
node --version
if errorlevel 1 (
    echo  [MISSING] Node.js not found
    echo            Download from: https://nodejs.org
    goto :fail
) else (
    echo  [OK] Node.js found
)

echo.
ffmpeg -version 2>nul | findstr /i "ffmpeg version"
if errorlevel 1 (
    echo  [WARN] FFmpeg not found - video rendering will not work
    echo         Fix: winget install ffmpeg
) else (
    echo  [OK] FFmpeg found
)

echo.

:: -------------------------------------------------------
:: Create storage directories
:: -------------------------------------------------------

echo [Step 2/5] Creating storage directories...
echo.

if not exist "%ROOT%\storage\projects" (
    mkdir "%ROOT%\storage\projects"
    echo  Created: storage\projects
)
if not exist "%ROOT%\storage\media" (
    mkdir "%ROOT%\storage\media"
    echo  Created: storage\media
)
if not exist "%ROOT%\storage\output" (
    mkdir "%ROOT%\storage\output"
    echo  Created: storage\output
)
if not exist "%ROOT%\storage\temp" (
    mkdir "%ROOT%\storage\temp"
    echo  Created: storage\temp
)
echo  [OK] Storage directories ready
echo.

:: -------------------------------------------------------
:: Python venv setup
:: -------------------------------------------------------

echo [Step 3/5] Setting up Python environment...
echo.

if not exist "%VENV%" (
    echo  Creating virtual environment at:
    echo  %VENV%
    echo.
    python -m venv "%VENV%"
    if errorlevel 1 (
        echo  [ERROR] Failed to create virtual environment
        goto :fail
    )
    echo  [OK] Virtual environment created
    echo.
) else (
    echo  [OK] Virtual environment already exists, skipping
    echo.
)

echo  Installing Python packages from requirements.txt...
echo  This may take a few minutes on first run...
echo.
"%PIP%" install -r "%BACKEND%\requirements.txt" --no-color
if errorlevel 1 (
    echo.
    echo  [WARN] Some packages may have failed. Check output above.
) else (
    echo.
    echo  [OK] All Python packages installed
)

echo.

:: Copy .env if missing
if not exist "%BACKEND%\.env" (
    if exist "%BACKEND%\.env.example" (
        copy "%BACKEND%\.env.example" "%BACKEND%\.env"
        echo  [OK] Created .env config from .env.example
        echo.
    )
) else (
    echo  [OK] .env config already exists
    echo.
)

:: -------------------------------------------------------
:: Node.js setup
:: -------------------------------------------------------

echo [Step 4/5] Setting up Node.js frontend...
echo.

if not exist "%FRONTEND%\node_modules" (
    echo  Installing Node.js packages...
    echo  This may take a minute on first run...
    echo.
    pushd "%FRONTEND%"
    call npm install
    if errorlevel 1 (
        echo.
        echo  [WARN] Some Node packages may have failed. Check output above.
    ) else (
        echo.
        echo  [OK] All Node packages installed
    )
    popd
) else (
    echo  [OK] Node modules already installed, skipping
)

echo.

:: -------------------------------------------------------
:: Launch servers
:: -------------------------------------------------------

echo [Step 5/5] Launching servers...
echo.
echo  Backend  : http://localhost:8000
echo  Frontend : http://localhost:5173
echo  API Docs : http://localhost:8000/docs
echo.

:: Write temp launcher for backend
set "BACK_LAUNCHER=%TEMP%\vf_backend.bat"
echo @echo off > "%BACK_LAUNCHER%"
echo echo [Vivara Backend] Starting... >> "%BACK_LAUNCHER%"
echo cd /d "%ROOT%" >> "%BACK_LAUNCHER%"
echo echo Working directory: %ROOT% >> "%BACK_LAUNCHER%"
echo echo. >> "%BACK_LAUNCHER%"
echo "%PYTHON%" -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 >> "%BACK_LAUNCHER%"
echo pause >> "%BACK_LAUNCHER%"

:: Write temp launcher for frontend
set "FRONT_LAUNCHER=%TEMP%\vf_frontend.bat"
echo @echo off > "%FRONT_LAUNCHER%"
echo echo [Vivara Frontend] Starting... >> "%FRONT_LAUNCHER%"
echo cd /d "%FRONTEND%" >> "%FRONT_LAUNCHER%"
echo echo Working directory: %FRONTEND% >> "%FRONT_LAUNCHER%"
echo echo. >> "%FRONT_LAUNCHER%"
echo npm run dev >> "%FRONT_LAUNCHER%"
echo pause >> "%FRONT_LAUNCHER%"

echo  Starting Backend server...
start "Vivara Backend"  cmd /c "%BACK_LAUNCHER%"

echo  Waiting for backend to start...
ping 127.0.0.1 -n 3 >nul

echo  Starting Frontend server...
start "Vivara Frontend" cmd /c "%FRONT_LAUNCHER%"

echo  Waiting for frontend to start...
ping 127.0.0.1 -n 4 >nul

echo  Opening browser...
start "" "http://localhost:5173"

echo.
echo  ================================
echo  Vivara is running!
echo  - Backend  : http://localhost:8000
echo  - Frontend : http://localhost:5173
echo  - API Docs : http://localhost:8000/docs
echo  ================================
echo.
echo  Close the two terminal windows to stop the servers.
echo.
pause
endlocal
goto :eof

:fail
echo.
echo  [FAILED] Please fix the issues above and re-run start.bat
echo.
pause
exit /b 1
