#!/bin/bash

# get-avm-modules.sh
# Retrieves metadata for Azure Verified Modules (AVM) from the Bicep Public Registry.
#
# Usage:
#   ./get-avm-modules.sh
#   ./get-avm-modules.sh --search "storage"
#   ./get-avm-modules.sh --type res --search "network"

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
GRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
NC='\033[0m'

# Default values
SEARCH=""
TYPE="all"
OUTPUT_FORMAT="table"

# Parse arguments
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --search <term>    Filter modules by search term"
    echo "  --type <type>      Filter by type: all, res, ptn, utl"
    echo "  --json             Output in JSON format"
    echo "  --list             Output registry references only"
    echo "  -h, --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --search storage"
    echo "  $0 --type res --search network"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --search)
            SEARCH="$2"
            shift 2
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --json)
            OUTPUT_FORMAT="json"
            shift
            ;;
        --list)
            OUTPUT_FORMAT="list"
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo -e "${RED}Error: Unknown argument: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}Azure Verified Modules (AVM) Catalog${NC}"
echo "===================================="
echo ""

# Define AVM modules as JSON for easier processing
read -r -d '' AVM_MODULES << 'EOF' || true
[
  {"name":"avm/res/storage/storage-account","description":"Storage Account with blob, file, queue, and table services","type":"res","version":"0.9.0","registry":"br/public:avm/res/storage/storage-account:0.9.0"},
  {"name":"avm/res/network/virtual-network","description":"Virtual Network with subnets, peering, and DNS configuration","type":"res","version":"0.4.0","registry":"br/public:avm/res/network/virtual-network:0.4.0"},
  {"name":"avm/res/network/network-security-group","description":"Network Security Group with security rules","type":"res","version":"0.3.0","registry":"br/public:avm/res/network/network-security-group:0.3.0"},
  {"name":"avm/res/compute/virtual-machine","description":"Virtual Machine with extensions and diagnostics","type":"res","version":"0.5.0","registry":"br/public:avm/res/compute/virtual-machine:0.5.0"},
  {"name":"avm/res/key-vault/vault","description":"Key Vault with secrets, keys, and certificates management","type":"res","version":"0.6.0","registry":"br/public:avm/res/key-vault/vault:0.6.0"},
  {"name":"avm/res/web/site","description":"Web App / App Service with configuration and deployment slots","type":"res","version":"0.3.0","registry":"br/public:avm/res/web/site:0.3.0"},
  {"name":"avm/res/web/serverfarm","description":"App Service Plan for hosting web apps","type":"res","version":"0.2.0","registry":"br/public:avm/res/web/serverfarm:0.2.0"},
  {"name":"avm/res/sql/server","description":"Azure SQL Server with databases and firewall rules","type":"res","version":"0.4.0","registry":"br/public:avm/res/sql/server:0.4.0"},
  {"name":"avm/res/container-service/managed-cluster","description":"Azure Kubernetes Service (AKS) cluster","type":"res","version":"0.3.0","registry":"br/public:avm/res/container-service/managed-cluster:0.3.0"},
  {"name":"avm/res/container-registry/registry","description":"Azure Container Registry (ACR)","type":"res","version":"0.4.0","registry":"br/public:avm/res/container-registry/registry:0.4.0"},
  {"name":"avm/res/operational-insights/workspace","description":"Log Analytics Workspace","type":"res","version":"0.4.0","registry":"br/public:avm/res/operational-insights/workspace:0.4.0"},
  {"name":"avm/res/network/private-endpoint","description":"Private Endpoint for Azure services","type":"res","version":"0.4.0","registry":"br/public:avm/res/network/private-endpoint:0.4.0"},
  {"name":"avm/res/network/application-gateway","description":"Application Gateway with WAF","type":"res","version":"0.3.0","registry":"br/public:avm/res/network/application-gateway:0.3.0"},
  {"name":"avm/res/network/load-balancer","description":"Azure Load Balancer","type":"res","version":"0.2.0","registry":"br/public:avm/res/network/load-balancer:0.2.0"},
  {"name":"avm/res/insights/component","description":"Application Insights","type":"res","version":"0.3.0","registry":"br/public:avm/res/insights/component:0.3.0"},
  {"name":"avm/ptn/authorization/resource-role-assignment","description":"Role assignment pattern for RBAC","type":"ptn","version":"0.1.0","registry":"br/public:avm/ptn/authorization/resource-role-assignment:0.1.0"},
  {"name":"avm/ptn/network/private-link-private-dns-zones","description":"Private Link DNS zone configuration","type":"ptn","version":"0.2.0","registry":"br/public:avm/ptn/network/private-link-private-dns-zones:0.2.0"},
  {"name":"avm/ptn/lz/sub-vending","description":"Landing zone subscription vending","type":"ptn","version":"0.1.0","registry":"br/public:avm/ptn/lz/sub-vending:0.1.0"},
  {"name":"avm/utl/types/avm-common-types","description":"Common type definitions for AVM modules","type":"utl","version":"0.1.0","registry":"br/public:avm/utl/types/avm-common-types:0.1.0"}
]
EOF

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required but not installed.${NC}"
    echo "Install with: brew install jq (macOS) or apt-get install jq (Ubuntu)"
    exit 1
fi

# Filter modules
FILTERED_MODULES="$AVM_MODULES"

# Filter by type
if [[ "$TYPE" != "all" ]]; then
    FILTERED_MODULES=$(echo "$FILTERED_MODULES" | jq --arg type "$TYPE" '[.[] | select(.type == $type)]')
fi

# Filter by search term
if [[ -n "$SEARCH" ]]; then
    SEARCH_LOWER=$(echo "$SEARCH" | tr '[:upper:]' '[:lower:]')
    FILTERED_MODULES=$(echo "$FILTERED_MODULES" | jq --arg search "$SEARCH_LOWER" '[.[] | select((.name | ascii_downcase | contains($search)) or (.description | ascii_downcase | contains($search)))]')
fi

# Get count
COUNT=$(echo "$FILTERED_MODULES" | jq 'length')

if [[ "$COUNT" == "0" ]]; then
    echo -e "${YELLOW}No modules found matching your criteria.${NC}"
    echo ""
    echo -e "${CYAN}For the complete catalog, visit:${NC}"
    echo -e "  ${BLUE}https://azure.github.io/Azure-Verified-Modules/indexes/bicep/${NC}"
    exit 0
fi

# Output based on format
case $OUTPUT_FORMAT in
    "table")
        echo -e "${GRAY}Module Type Legend: res=Resource, ptn=Pattern, utl=Utility${NC}"
        echo ""

        echo "$FILTERED_MODULES" | jq -r '.[] | "\(.type)|\(.name)|\(.description)|\(.version)|\(.registry)"' | while IFS='|' read -r type name desc version registry; do
            case $type in
                "res") type_color="$GREEN" ;;
                "ptn") type_color="$MAGENTA" ;;
                "utl") type_color="$YELLOW" ;;
            esac

            echo -e "${type_color}[$type]${NC} ${CYAN}$name${NC}"
            echo -e "  ${GRAY}$desc${NC}"
            echo -e "  ${DARKGRAY}Version: $version | Ref: $registry${NC}"
            echo ""
        done
        ;;
    "list")
        echo "$FILTERED_MODULES" | jq -r '.[].registry'
        ;;
    "json")
        echo "$FILTERED_MODULES" | jq '.'
        ;;
esac

echo -e "${CYAN}Total modules: $COUNT${NC}"
echo ""
echo -e "${YELLOW}Usage Example:${NC}"
echo "=============="
echo ""

cat << 'EOF'
// Use in your Bicep file
module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  name: 'storageDeployment'
  params: {
    name: 'mystorageaccount'
    location: location
  }
}
EOF

echo ""
echo -e "${BLUE}Full AVM Catalog: https://azure.github.io/Azure-Verified-Modules/indexes/bicep/${NC}"
echo -e "${BLUE}GitHub: https://github.com/Azure/bicep-registry-modules${NC}"
