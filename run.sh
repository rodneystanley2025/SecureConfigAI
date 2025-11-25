#!/bin/bash

# A script to set up and run the AI-Powered Configuration Scanner.

# --- Configuration ---
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
ENV_FILE=".env"
HOST="0.0.0.0"
PORT="8001"

# --- Colors for output ---
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
COLOR_NC='\033[0m' # No Color

# --- Helper Functions ---
function print_info {
    echo -e "${COLOR_GREEN}[INFO]${COLOR_NC} $1"
}

function print_warning {
    echo -e "${COLOR_YELLOW}[WARNING]${COLOR_NC} $1"
}

function print_error {
    echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $1"
}

# --- Main Script ---

# 1. Check for and create the virtual environment if it doesn't exist.
if [ ! -d "$VENV_DIR" ]; then
    print_info "Virtual environment not found. Creating one now at './$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        print_error "Failed to create the virtual environment. Please ensure Python 3 is installed and accessible."
        exit 1
    fi
fi

# 2. Activate the virtual environment.
print_info "Activating the virtual environment..."
source "$VENV_DIR/bin/activate"

# 3. Check for and install dependencies.
if [ -f "$REQUIREMENTS_FILE" ]; then
    # Using a simple flag file to avoid checking pip freeze every time.
    if [ ! -f "$VENV_DIR/.dependencies_installed" ] || [ "$REQUIREMENTS_FILE" -nt "$VENV_DIR/.dependencies_installed" ]; then
        print_info "Installing dependencies from '$REQUIREMENTS_FILE'"
        pip install -r "$REQUIREMENTS_FILE"
        if [ $? -ne 0 ]; then
            print_error "Failed to install dependencies. Please check the '$REQUIREMENTS_FILE' file."
            exit 1
        fi
        touch "$VENV_DIR/.dependencies_installed" # Mark dependencies as installed
    else
        print_info "Dependencies are already installed."
    fi
else
    print_warning "Could not find '$REQUIREMENTS_FILE'. Skipping dependency installation."
fi

# 4. Check for the .env file and the GEMINI_API_KEY.
if [ ! -f "$ENV_FILE" ]; then
    print_error "The '$ENV_FILE' file was not found."
    print_warning "Please create a '$ENV_FILE' file in the 'AIScanner' directory and add your Gemini API key to it, like this:"
    echo -e "\nGEMINI_API_KEY=YOUR_API_KEY_HERE\n"
    exit 1
elif ! grep -q "GEMINI_API_KEY" "$ENV_FILE" || grep -q "YOUR_API_KEY_HERE" "$ENV_FILE"; then
    print_error "The 'GEMINI_API_KEY' is missing or not set in your '$ENV_FILE' file."
    print_warning "Please make sure your '$ENV_FILE' file contains a valid line, like this:"
    echo -e "\nGEMINI_API_KEY=xxxxxxxxxxxxxxxxx\n"
    exit 1
fi

# 5. Load environment variables from the .env file
# This ensures uvicorn can see the variables without needing python-dotenv at runtime for this script.
export $(grep -v '^#' $ENV_FILE | xargs)

# 6. Run the application.
print_info "Starting the FastAPI server on http://$HOST:$PORT"
print_info "Press CTRL+C to stop the server."

uvicorn src.main:app --host "$HOST" --port "$PORT" --reload --reload-dir "src"
