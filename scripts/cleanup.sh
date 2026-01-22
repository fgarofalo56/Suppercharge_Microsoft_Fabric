#!/usr/bin/env bash
# =============================================================================
# Microsoft Fabric POC - Cleanup (Unix/Mac)
# =============================================================================
#
# SYNOPSIS:
#     Cleanup and teardown Microsoft Fabric POC resources.
#
# USAGE:
#     ./cleanup.sh [OPTIONS]
#
# OPTIONS:
#     --delete-azure        Delete the Azure resource group
#     --delete-data         Delete local generated data
#     --delete-venv         Delete Python virtual environment
#     --all                 Delete everything
#     --force               Skip confirmation prompts
#     --environment ENV     Target environment: dev, staging, prod (default: dev)
#     --help                Show this help message
#
# EXAMPLES:
#     ./cleanup.sh --delete-data
#     ./cleanup.sh --delete-azure
#     ./cleanup.sh --all --force
#     ./cleanup.sh --delete-azure --environment staging
#
# =============================================================================

set -e

# =============================================================================
# Configuration
# =============================================================================
DELETE_AZURE=false
DELETE_DATA=false
DELETE_VENV=false
FORCE=false
ENVIRONMENT="dev"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

# =============================================================================
# Color Output
# =============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m'

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

write_warning() {
    echo -e "${RED}[!] $1${NC}"
}

# =============================================================================
# Parse Arguments
# =============================================================================
while [[ $# -gt 0 ]]; do
    case $1 in
        --delete-azure)
            DELETE_AZURE=true
            shift
            ;;
        --delete-data)
            DELETE_DATA=true
            shift
            ;;
        --delete-venv)
            DELETE_VENV=true
            shift
            ;;
        --all)
            DELETE_AZURE=true
            DELETE_DATA=true
            DELETE_VENV=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --environment)
            ENVIRONMENT="$2"
            if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
                echo "Invalid environment: $ENVIRONMENT"
                exit 1
            fi
            shift 2
            ;;
        --help|-h)
            head -35 "$0" | grep -E '^#' | sed 's/^# //' | sed 's/^#//'
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
# Helper Functions
# =============================================================================
confirm_action() {
    local message="$1"
    if [ "$FORCE" = true ]; then
        return 0
    fi
    read -p "$message (y/N) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

load_env_var() {
    local var_name="$1"
    if [ -f "$ENV_FILE" ]; then
        local value=$(grep "^${var_name}=" "$ENV_FILE" | cut -d'=' -f2- | sed 's/^["'\'']//' | sed 's/["'\'']$//')
        echo "$value"
    fi
}

format_size() {
    local size=$1
    if [ $size -gt 1073741824 ]; then
        echo "$(awk "BEGIN {printf \"%.2f GB\", $size/1073741824}")"
    elif [ $size -gt 1048576 ]; then
        echo "$(awk "BEGIN {printf \"%.2f MB\", $size/1048576}")"
    else
        echo "$(awk "BEGIN {printf \"%.2f KB\", $size/1024}")"
    fi
}

get_dir_size() {
    local dir="$1"
    if [ -d "$dir" ]; then
        du -sb "$dir" 2>/dev/null | cut -f1 || echo 0
    else
        echo 0
    fi
}

# =============================================================================
# Main Script
# =============================================================================

write_header "Microsoft Fabric POC - Cleanup"

# Check if any action specified
if [ "$DELETE_AZURE" = false ] && [ "$DELETE_DATA" = false ] && [ "$DELETE_VENV" = false ]; then
    echo -e "${YELLOW}No cleanup action specified.${NC}"
    echo ""
    echo "Usage:"
    echo "  ./cleanup.sh --delete-data        # Delete generated data"
    echo "  ./cleanup.sh --delete-azure       # Delete Azure resources"
    echo "  ./cleanup.sh --delete-venv        # Delete virtual environment"
    echo "  ./cleanup.sh --all                # Delete everything"
    echo "  ./cleanup.sh --all --force        # Delete everything without prompts"
    echo ""
    exit 0
fi

# Display what will be cleaned
write_step "Cleanup plan:"
if [ "$DELETE_DATA" = true ]; then write_info "- Delete generated data"; fi
if [ "$DELETE_VENV" = true ]; then write_info "- Delete Python virtual environment"; fi
if [ "$DELETE_AZURE" = true ]; then write_info "- Delete Azure resource group ($ENVIRONMENT)"; fi
echo ""

# =============================================================================
# Delete Generated Data
# =============================================================================
if [ "$DELETE_DATA" = true ]; then
    write_header "Cleaning Generated Data"

    DATA_PATHS=(
        "$PROJECT_ROOT/data/generated"
        "$PROJECT_ROOT/output"
        "$PROJECT_ROOT/data/output"
    )

    for path in "${DATA_PATHS[@]}"; do
        if [ -d "$path" ]; then
            file_count=$(find "$path" -type f 2>/dev/null | wc -l | tr -d ' ')
            size=$(get_dir_size "$path")

            write_info "Found: $path"
            write_info "Files: $file_count, Size: $(format_size $size)"

            if confirm_action "Delete $path?"; then
                write_step "Deleting $path..."
                rm -rf "$path"
                write_success "Deleted"
            else
                write_info "Skipped"
            fi
        fi
    done

    # Clean temp files
    temp_files=$(find "$PROJECT_ROOT" -maxdepth 1 -name "tmpclaude-*" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [ "$temp_files" -gt 0 ]; then
        write_step "Found $temp_files temporary files"
        if confirm_action "Delete temporary files?"; then
            find "$PROJECT_ROOT" -maxdepth 1 -name "tmpclaude-*" -type f -delete
            write_success "Temporary files deleted"
        fi
    fi

    write_success "Data cleanup complete"
fi

# =============================================================================
# Delete Virtual Environment
# =============================================================================
if [ "$DELETE_VENV" = true ]; then
    write_header "Cleaning Virtual Environment"

    VENV_PATHS=(
        "$PROJECT_ROOT/.venv"
        "$PROJECT_ROOT/venv"
    )

    found=false
    for path in "${VENV_PATHS[@]}"; do
        if [ -d "$path" ]; then
            found=true
            size=$(get_dir_size "$path")

            write_info "Found: $path"
            write_info "Size: $(format_size $size)"

            if confirm_action "Delete virtual environment at $path?"; then
                write_step "Deleting $path..."

                # Deactivate if active
                if [ "$VIRTUAL_ENV" = "$path" ]; then
                    write_info "Deactivating virtual environment..."
                    deactivate 2>/dev/null || true
                fi

                rm -rf "$path"
                write_success "Virtual environment deleted"
            else
                write_info "Skipped"
            fi
        fi
    done

    if [ "$found" = false ]; then
        write_info "No virtual environment found"
    fi

    # Clean __pycache__ directories
    pycache_count=$(find "$PROJECT_ROOT" -name "__pycache__" -type d 2>/dev/null | wc -l | tr -d ' ')
    if [ "$pycache_count" -gt 0 ]; then
        write_step "Found $pycache_count __pycache__ directories"
        if confirm_action "Delete __pycache__ directories?"; then
            find "$PROJECT_ROOT" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
            write_success "__pycache__ directories deleted"
        fi
    fi

    # Clean .pytest_cache
    if [ -d "$PROJECT_ROOT/.pytest_cache" ]; then
        write_step "Found .pytest_cache"
        if confirm_action "Delete .pytest_cache?"; then
            rm -rf "$PROJECT_ROOT/.pytest_cache"
            write_success ".pytest_cache deleted"
        fi
    fi

    write_success "Virtual environment cleanup complete"
fi

# =============================================================================
# Delete Azure Resources
# =============================================================================
if [ "$DELETE_AZURE" = true ]; then
    write_header "Cleaning Azure Resources"

    # Load project prefix from .env
    PROJECT_PREFIX=$(load_env_var "PROJECT_PREFIX")
    if [ -z "$PROJECT_PREFIX" ]; then
        write_failure "PROJECT_PREFIX not found in .env file"
        write_info "Cannot determine resource group name"
        exit 1
    fi

    RESOURCE_GROUP="${PROJECT_PREFIX}-${ENVIRONMENT}-rg"

    write_warning "WARNING: This will permanently delete all Azure resources!"
    echo ""
    write_info "Resource Group: $RESOURCE_GROUP"
    write_info "Environment:    $ENVIRONMENT"
    echo ""

    # Check if logged in
    if ! az account show &>/dev/null; then
        write_failure "Not logged in to Azure CLI"
        write_info "Run 'az login' to authenticate"
        exit 1
    fi

    CURRENT_USER=$(az account show --query 'user.name' -o tsv)
    write_info "Logged in as: $CURRENT_USER"

    # Set subscription if specified
    SUBSCRIPTION_ID=$(load_env_var "AZURE_SUBSCRIPTION_ID")
    if [ -n "$SUBSCRIPTION_ID" ]; then
        az account set --subscription "$SUBSCRIPTION_ID" 2>/dev/null
    fi

    # Check if resource group exists
    RG_EXISTS=$(az group exists --name "$RESOURCE_GROUP")
    if [ "$RG_EXISTS" != "true" ]; then
        write_info "Resource group '$RESOURCE_GROUP' does not exist"
    else
        # List resources in the group
        write_step "Resources in $RESOURCE_GROUP:"
        az resource list --resource-group "$RESOURCE_GROUP" \
            --query "[].{Name:name, Type:type}" -o table 2>/dev/null | tail -n +3 | \
            while read -r line; do
                write_info "  $line"
            done
        echo ""

        write_warning "This action is IRREVERSIBLE!"

        if [ "$FORCE" = false ]; then
            echo ""
            echo -e "${RED}Type the resource group name to confirm deletion: ${NC}"
            read -r confirmation

            if [ "$confirmation" != "$RESOURCE_GROUP" ]; then
                write_info "Confirmation failed - resource group NOT deleted"
                exit 0
            fi
        fi

        write_step "Deleting resource group: $RESOURCE_GROUP"
        write_info "This may take several minutes..."

        if az group delete --name "$RESOURCE_GROUP" --yes --no-wait 2>/dev/null; then
            write_success "Resource group deletion initiated"
            write_info "Deletion is running in the background"
            write_info "Check Azure Portal for status"
        else
            write_failure "Failed to delete resource group"
            exit 1
        fi
    fi

    # Clean deployment outputs file
    OUTPUT_FILE="$PROJECT_ROOT/deployment-outputs.json"
    if [ -f "$OUTPUT_FILE" ]; then
        write_step "Found deployment-outputs.json"
        if confirm_action "Delete deployment outputs file?"; then
            rm -f "$OUTPUT_FILE"
            write_success "Deployment outputs deleted"
        fi
    fi

    write_success "Azure cleanup initiated"
fi

# =============================================================================
# Summary
# =============================================================================
write_header "Cleanup Complete!"

write_success "Cleanup operations completed"
echo ""

if [ "$DELETE_AZURE" = true ]; then
    echo -e "${YELLOW}Note: Azure resource group deletion may take several minutes.${NC}"
    echo -e "${YELLOW}Check the Azure Portal for confirmation.${NC}"
    echo ""
fi

if [ "$DELETE_VENV" = true ]; then
    echo -e "${YELLOW}To recreate the environment, run:${NC}"
    echo -e "${CYAN}  ./scripts/setup.sh${NC}"
    echo ""
fi
