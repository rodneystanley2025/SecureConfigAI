@echo off
rem A script to initialize the database using Alembic.

rem --- Configuration ---
set "VENV_DIR=venv"
set "ALEMBIC_DIR=alembic"

rem --- Main Script ---

echo [INFO] Starting the database initialization script...

rem 1. Activate the virtual environment.
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. Please run the 'run.bat' script first to create it.
    exit /b 1
)
echo [INFO] Activating the virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

rem 2. Check if alembic is already initialized.
if exist "%ALEMBIC_DIR%" (
    echo [INFO] The '%ALEMBIC_DIR%' directory already exists. Skipping initialization.
) else (
    echo [INFO] Initializing the Alembic migration environment...
    python -m alembic init "%ALEMBIC_DIR%"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to initialize Alembic.
        exit /b 1
    ) else (
        echo [INFO] Alembic initialized successfully.
    )
)

echo [INFO] Database initialization script finished.

