@echo off
setlocal EnableDelayedExpansion

rem A script to set up and run the AI-Powered Configuration Scanner on Windows.

rem --- Configuration ---
set "VENV_DIR=venv"
set "REQUIREMENTS_FILE=requirements.txt"
set "ENV_FILE=.env"
set "HOST=0.0.0.0"
set "PORT=8000"

rem --- Main Script ---

echo [INFO] Starting the AI Scanner setup script...

rem 1. Check for and create the virtual environment if it doesn't exist.
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Virtual environment not found. Creating one now at '.\%VENV_DIR%'...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create the virtual environment. Ensure Python is installed and in PATH.
        pause
        exit /b 1
    )
)

rem 2. Activate the virtual environment - this sets up PATH for pip/python.
echo [INFO] Activating the virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

rem 3. Install/Update dependencies.
if exist "%REQUIREMENTS_FILE%" (
    echo [INFO] Installing/Updating dependencies from '%REQUIREMENTS_FILE%'...
    pip install -r "%REQUIREMENTS_FILE%"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install/update dependencies. Please check the '%REQUIREMENTS_FILE%' file.
        pause
        exit /b 1
    )
) else (
    echo [WARNING] Could not find '%REQUIREMENTS_FILE%'. Skipping dependency installation.
)

rem 4. Load environment variables from .env file directly (simplified for robustness).
if not exist "%ENV_FILE%" (
    echo [ERROR] '%ENV_FILE%' file not found!
    echo [INFO] Please create a file named .env in this folder containing:
    echo GEMINI_API_KEY=your-actual-key-here
    echo.
    pause
    exit /b 1
)

echo [INFO] Loading environment variables from %ENV_FILE%...
for /f "tokens=*" %%a in (%ENV_FILE%) do (
    rem Skip empty lines and lines starting with #
    echo "%%a" | findstr /r /c:"^$" /c:"^#" >nul
    if errorlevel 1 (
        rem Only set if it contains an equals sign (key=value)
        echo "%%a" | findstr "=" >nul
        if not errorlevel 1 (
            set "%%a"
            rem Optional: echo [DEBUG] Set environment variable: %%a
        )
    )
)

if not defined GEMINI_API_KEY (
    echo [ERROR] GEMINI_API_KEY is missing or empty in '%ENV_FILE%'!
    echo Please add a line like: GEMINI_API_KEY=sk-...
    echo.
    pause
    exit /b 1
)

if "%GEMINI_API_KEY%"=="" (
    echo [ERROR] GEMINI_API_KEY is empty in '%ENV_FILE%'!
    pause
    exit /b 1
)

echo [INFO] GEMINI_API_KEY loaded successfully.

rem 5. Run the application, explicitly using the virtual environment's Python.
echo [INFO] Starting the FastAPI server on http://%HOST%:%PORT%
echo [INFO] Press CTRL+C to stop the server.
echo.

"%VENV_DIR%\Scripts\python.exe" -m uvicorn src.main:app --host "%HOST%" --port "%PORT%" --reload --reload-dir "src"

endlocal