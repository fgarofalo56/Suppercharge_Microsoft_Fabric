#!/usr/bin/env bash
# =============================================================================
# Microsoft Fabric Casino/Gaming POC - Environment Setup (Unix/Mac)
# =============================================================================
#
# SYNOPSIS:
#     Complete environment setup for Microsoft Fabric Casino/Gaming POC.
#
# USAGE:
#     ./setup.sh [OPTIONS]
#
# OPTIONS:
#     --skip-azure-login    Skip Azure CLI login validation
#     --venv-path PATH      Path for virtual environment (default: .venv)
#     --help                Show this help message
#
# EXAMPLES:
#     ./setup.sh
#     ./setup.sh --skip-azure-login
#     ./setup.sh --venv-path /path/to/venv
#
# =============================================================================

set -e

# =============================================================================
# Configuration
# =============================================================================
MIN_PYTHON_VERSION="3.10"
VENV_PATH=".venv"
SKIP_AZURE_LOGIN=false

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# =============================================================================
# Color Output
# =============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

write_header() {
    echo ""
    echo -e "${CYAN}======================================================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}======================================================================${NC}"
    echo ""
}

write_step() {
    echo -e "${YELLOW}[*] $1${NC}"
}

write_success() {
    echo -e "${GREEN}[+] $1${NC}"
}

write_failure() {
    echo -e "${RED}[-] $1${NC}"
}

write_info() {
    echo -e "${GRAY}    $1${NC}"
}

# =============================================================================
# Helper Functions
# =============================================================================
command_exists() {
    command -v "$1" &> /dev/null
}

version_gte() {
    # Returns 0 (true) if $1 >= $2
    printf '%s\n%s\n' "$2" "$1" | sort -V -C
}

get_python_version() {
    local cmd=$1
    if command_exists "$cmd"; then
        "$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1
    fi
}

find_python() {
    local python_cmds=("python3" "python" "python3.12" "python3.11" "python3.10")

    for cmd in "${python_cmds[@]}"; do
        if command_exists "$cmd"; then
            local version=$(get_python_version "$cmd")
            if [ -n "$version" ] && version_gte "$version" "$MIN_PYTHON_VERSION"; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

# =============================================================================
# Parse Arguments
# =============================================================================
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-azure-login)
            SKIP_AZURE_LOGIN=true
            shift
            ;;
        --venv-path)
            VENV_PATH="$2"
            shift 2
            ;;
        --help|-h)
            head -50 "$0" | grep -E '^#' | sed 's/^# //' | sed 's/^#//'
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# =============================================================================
# Main Script
# =============================================================================

write_header "Microsoft Fabric Casino/Gaming POC - Environment Setup"

echo -e "${GRAY}Project Root: $PROJECT_ROOT${NC}"
echo -e "${GRAY}Script Root:  $SCRIPT_DIR${NC}"
echo ""

cd "$PROJECT_ROOT"

# =============================================================================
# Step 1: Check Prerequisites
# =============================================================================
write_header "Step 1: Checking Prerequisites"

PREREQUISITES_MET=true
PYTHON_CMD=""

# Check Python
write_step "Checking Python $MIN_PYTHON_VERSION+..."
PYTHON_CMD=$(find_python)
if [ -n "$PYTHON_CMD" ]; then
    PYTHON_VERSION=$(get_python_version "$PYTHON_CMD")
    write_success "Found $PYTHON_CMD version $PYTHON_VERSION"
else
    write_failure "Python $MIN_PYTHON_VERSION+ not found"
    write_info "Please install Python 3.10 or later from https://www.python.org/downloads/"
    PREREQUISITES_MET=false
fi

# Check Git
write_step "Checking Git..."
if command_exists git; then
    GIT_VERSION=$(git --version | sed 's/git version //')
    write_success "Found Git version $GIT_VERSION"
else
    write_failure "Git not found"
    write_info "Please install Git: https://git-scm.com/downloads"
    write_info "  macOS: brew install git"
    write_info "  Ubuntu/Debian: sudo apt-get install git"
    PREREQUISITES_MET=false
fi

# Check Azure CLI
write_step "Checking Azure CLI..."
if command_exists az; then
    AZ_VERSION=$(az version --query '"azure-cli"' -o tsv 2>/dev/null)
    write_success "Found Azure CLI version $AZ_VERSION"
else
    write_failure "Azure CLI not found"
    write_info "Please install Azure CLI: https://docs.microsoft.com/cli/azure/install-azure-cli"
    write_info "  macOS: brew install azure-cli"
    write_info "  Ubuntu/Debian: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
    PREREQUISITES_MET=false
fi

# Check Bicep
write_step "Checking Bicep..."
if command_exists az; then
    BICEP_VERSION=$(az bicep version 2>/dev/null)
    if [ -n "$BICEP_VERSION" ]; then
        write_success "Found Bicep: $(echo "$BICEP_VERSION" | sed 's/Bicep CLI version //')"
    else
        write_info "Bicep not installed, attempting to install..."
        if az bicep install 2>/dev/null; then
            write_success "Bicep installed successfully"
        else
            write_failure "Failed to install Bicep"
            write_info "Run 'az bicep install' manually"
            PREREQUISITES_MET=false
        fi
    fi
else
    write_info "Skipping Bicep check (Azure CLI not available)"
fi

# Check pip
write_step "Checking pip..."
if [ -n "$PYTHON_CMD" ]; then
    if $PYTHON_CMD -m pip --version &>/dev/null; then
        PIP_VERSION=$($PYTHON_CMD -m pip --version 2>&1 | grep -oE 'pip [0-9.]+' | sed 's/pip //')
        write_success "Found pip version $PIP_VERSION"
    else
        write_failure "pip not available"
        PREREQUISITES_MET=false
    fi
fi

if [ "$PREREQUISITES_MET" = false ]; then
    echo ""
    write_failure "Prerequisites check failed. Please install missing components."
    exit 1
fi

write_success "All prerequisites met!"

# =============================================================================
# Step 2: Create Virtual Environment
# =============================================================================
write_header "Step 2: Creating Python Virtual Environment"

VENV_FULL_PATH="$PROJECT_ROOT/$VENV_PATH"

if [ -d "$VENV_FULL_PATH" ]; then
    write_info "Virtual environment already exists at $VENV_FULL_PATH"
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        write_step "Removing existing virtual environment..."
        rm -rf "$VENV_FULL_PATH"
    else
        write_info "Using existing virtual environment"
    fi
fi

if [ ! -d "$VENV_FULL_PATH" ]; then
    write_step "Creating virtual environment at $VENV_FULL_PATH..."
    $PYTHON_CMD -m venv "$VENV_FULL_PATH"
    write_success "Virtual environment created"
fi

# =============================================================================
# Step 3: Activate Virtual Environment and Install Dependencies
# =============================================================================
write_header "Step 3: Installing Dependencies"

VENV_ACTIVATE="$VENV_FULL_PATH/bin/activate"
VENV_PYTHON="$VENV_FULL_PATH/bin/python"
VENV_PIP="$VENV_FULL_PATH/bin/pip"

if [ ! -f "$VENV_ACTIVATE" ]; then
    write_failure "Virtual environment activation script not found"
    exit 1
fi

write_step "Activating virtual environment..."
source "$VENV_ACTIVATE"

write_step "Upgrading pip..."
$VENV_PYTHON -m pip install --upgrade pip --quiet
write_success "pip upgraded"

# Install main requirements
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    write_step "Installing requirements from requirements.txt..."
    $VENV_PIP install -r "$REQUIREMENTS_FILE" --quiet
    write_success "Main dependencies installed"
else
    write_failure "requirements.txt not found"
    exit 1
fi

# Install dev requirements if exists
DEV_REQUIREMENTS_FILE="$PROJECT_ROOT/requirements-dev.txt"
if [ -f "$DEV_REQUIREMENTS_FILE" ]; then
    write_step "Installing development dependencies..."
    if $VENV_PIP install -r "$DEV_REQUIREMENTS_FILE" --quiet 2>/dev/null; then
        write_success "Development dependencies installed"
    else
        write_info "Warning: Some dev dependencies failed to install"
    fi
fi

# =============================================================================
# Step 4: Validate Azure Login
# =============================================================================
if [ "$SKIP_AZURE_LOGIN" = false ]; then
    write_header "Step 4: Validating Azure Login"

    write_step "Checking Azure CLI login status..."

    if az account show &>/dev/null; then
        ACCOUNT_NAME=$(az account show --query 'name' -o tsv)
        TENANT_ID=$(az account show --query 'tenantId' -o tsv)
        USER_NAME=$(az account show --query 'user.name' -o tsv)

        write_success "Logged in to Azure"
        write_info "Subscription: $ACCOUNT_NAME"
        write_info "Tenant ID:    $TENANT_ID"
        write_info "User:         $USER_NAME"
    else
        write_info "Not logged in to Azure CLI"
        read -p "Do you want to log in now? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            write_step "Opening Azure login..."
            if az login; then
                write_success "Azure login successful"
            else
                write_failure "Azure login failed"
            fi
        else
            write_info "Skipping Azure login"
            write_info "Run 'az login' before deploying infrastructure"
        fi
    fi
else
    write_info "Skipping Azure login validation (--skip-azure-login specified)"
fi

# =============================================================================
# Step 5: Setup .env File
# =============================================================================
write_header "Step 5: Environment Configuration"

ENV_FILE="$PROJECT_ROOT/.env"
ENV_SAMPLE_FILE="$PROJECT_ROOT/.env.sample"

if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_SAMPLE_FILE" ]; then
        write_step "Creating .env from .env.sample..."
        cp "$ENV_SAMPLE_FILE" "$ENV_FILE"
        write_success ".env file created"
        write_info "Please edit .env and fill in your configuration values"
    else
        write_info ".env.sample not found, skipping .env creation"
    fi
else
    write_info ".env file already exists"
fi

# =============================================================================
# Summary and Next Steps
# =============================================================================
write_header "Setup Complete!"

echo -e "${GREEN}Environment is ready for development.${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo -e "  1. Activate the virtual environment:"
echo -e "     ${CYAN}source $VENV_ACTIVATE${NC}"
echo ""
echo -e "  2. Edit .env with your Azure configuration:"
echo -e "     ${CYAN}nano .env${NC}  or  ${CYAN}code .env${NC}"
echo ""
echo -e "  3. Generate sample data:"
echo -e "     ${CYAN}./scripts/generate-data.sh --quick${NC}"
echo ""
echo -e "  4. Deploy infrastructure (requires .env configuration):"
echo -e "     ${CYAN}./scripts/deploy-infrastructure.sh${NC}"
echo ""
echo -e "  5. Validate environment:"
echo -e "     ${CYAN}./scripts/validate-environment.sh${NC}"
echo ""
echo -e "${GRAY}For help, see scripts/README.md${NC}"
echo ""
