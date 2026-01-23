#!/bin/bash

# get-resource-schema.sh
# Retrieves the schema for a specific Azure resource type.
#
# Usage:
#   ./get-resource-schema.sh <resource-type>
#   ./get-resource-schema.sh "Microsoft.Storage/storageAccounts@2023-05-01"

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
GRAY='\033[0;37m'
NC='\033[0m'

# Parse arguments
RESOURCE_TYPE=""

show_help() {
    echo "Usage: $0 <resource-type>"
    echo ""
    echo "Arguments:"
    echo "  resource-type    Full resource type string (Provider/Type@ApiVersion)"
    echo ""
    echo "Examples:"
    echo "  $0 'Microsoft.Storage/storageAccounts@2023-05-01'"
    echo "  $0 'Microsoft.Compute/virtualMachines@2023-09-01'"
    echo "  $0 'Microsoft.KeyVault/vaults@2023-07-01'"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            ;;
        *)
            if [[ -z "$RESOURCE_TYPE" ]]; then
                RESOURCE_TYPE="$1"
            else
                echo -e "${RED}Error: Unexpected argument: $1${NC}"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate resource type
if [[ -z "$RESOURCE_TYPE" ]]; then
    echo -e "${RED}Error: Resource type is required${NC}"
    echo ""
    show_help
fi

# Parse resource type (Provider/Type@ApiVersion)
if [[ "$RESOURCE_TYPE" =~ ^([^/]+)/([^@]+)@(.+)$ ]]; then
    PROVIDER="${BASH_REMATCH[1]}"
    TYPE="${BASH_REMATCH[2]}"
    API_VERSION="${BASH_REMATCH[3]}"
else
    echo -e "${RED}Error: Invalid resource type format${NC}"
    echo "Expected format: Provider/Type@ApiVersion"
    echo "Example: Microsoft.Storage/storageAccounts@2023-05-01"
    exit 1
fi

echo -e "${CYAN}Fetching schema for: $RESOURCE_TYPE${NC}"
echo ""

# Check for Bicep CLI
HAS_BICEP=false
if command -v bicep &> /dev/null; then
    HAS_BICEP=true
fi

# Display parsed information
echo -e "${YELLOW}Resource Type Information:${NC}"
echo "========================="
echo ""
echo -e "${GREEN}Provider:     $PROVIDER${NC}"
echo -e "${GREEN}Type:         $TYPE${NC}"
echo -e "${GREEN}API Version:  $API_VERSION${NC}"
echo ""

# Get additional info from Azure CLI if available
if command -v az &> /dev/null; then
    if az account show &> /dev/null; then
        echo -e "${GRAY}Fetching detailed schema from Azure...${NC}"

        PROVIDER_INFO=$(az provider show --namespace "$PROVIDER" --query "resourceTypes[?resourceType=='$TYPE']" -o json 2>/dev/null || echo "[]")

        if [[ "$PROVIDER_INFO" != "[]" && "$PROVIDER_INFO" != "null" ]]; then
            # Get API versions
            API_VERSIONS=$(echo "$PROVIDER_INFO" | jq -r '.[0].apiVersions // []')
            if [[ "$API_VERSIONS" != "[]" ]]; then
                echo ""
                echo -e "${YELLOW}Available API Versions:${NC}"
                echo "$API_VERSIONS" | jq -r '.[]' | head -10 | while read -r version; do
                    echo "  $version"
                done
                VERSION_COUNT=$(echo "$API_VERSIONS" | jq 'length')
                if [[ "$VERSION_COUNT" -gt 10 ]]; then
                    echo "  ... and $((VERSION_COUNT - 10)) more"
                fi
            fi

            # Get locations
            LOCATIONS=$(echo "$PROVIDER_INFO" | jq -r '.[0].locations // []')
            if [[ "$LOCATIONS" != "[]" ]]; then
                echo ""
                echo -e "${YELLOW}Available Locations:${NC}"
                echo "$LOCATIONS" | jq -r '.[]' | head -10 | while read -r loc; do
                    echo "  $loc"
                done
                LOC_COUNT=$(echo "$LOCATIONS" | jq 'length')
                if [[ "$LOC_COUNT" -gt 10 ]]; then
                    echo "  ... and $((LOC_COUNT - 10)) more"
                fi
            fi

            # Get capabilities
            CAPABILITIES=$(echo "$PROVIDER_INFO" | jq -r '.[0].capabilities // []')
            if [[ "$CAPABILITIES" != "[]" ]]; then
                echo ""
                echo -e "${YELLOW}Capabilities:${NC}"
                echo "$CAPABILITIES" | jq -r '.[] | "  \(.name): \(.value)"'
            fi
        fi
    else
        echo -e "${YELLOW}Note: Not logged into Azure. Run 'az login' for more detailed information.${NC}"
    fi
fi

# Show example Bicep code
echo ""
echo -e "${CYAN}Example Bicep Declaration:${NC}"
echo "=========================="
echo ""

cat << EOF
${GRAY}@description('The name of the $TYPE resource')
param resourceName string

@description('The location for the resource')
param location string = resourceGroup().location

resource myResource '$RESOURCE_TYPE' = {
  name: resourceName
  location: location
  // Add required properties here
  properties: {
    // Resource-specific properties
  }
}

output resourceId string = myResource.id${NC}
EOF

# Documentation links
echo ""
echo -e "${CYAN}Documentation Links:${NC}"
echo "==================="
DOCS_URL="https://learn.microsoft.com/azure/templates/${PROVIDER,,}/$TYPE"
echo -e "${BLUE}ARM Template Reference: $DOCS_URL${NC}"

echo ""
echo -e "${YELLOW}Tip: Use VS Code with the Bicep extension for IntelliSense and auto-completion${NC}"
