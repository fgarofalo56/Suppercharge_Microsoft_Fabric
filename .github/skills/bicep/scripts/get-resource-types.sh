#!/bin/bash

# get-resource-types.sh
# Lists Azure resource types for a specific provider with their API versions.
#
# Usage:
#   ./get-resource-types.sh <provider-namespace>
#   ./get-resource-types.sh Microsoft.Storage
#   ./get-resource-types.sh Microsoft.Compute --all-versions
#   ./get-resource-types.sh Microsoft.Network --json

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Default values
SHOW_ALL_VERSIONS=false
OUTPUT_FORMAT="table"

# Parse arguments
PROVIDER=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --all-versions)
            SHOW_ALL_VERSIONS=true
            shift
            ;;
        --json)
            OUTPUT_FORMAT="json"
            shift
            ;;
        --csv)
            OUTPUT_FORMAT="csv"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 <provider-namespace> [options]"
            echo ""
            echo "Options:"
            echo "  --all-versions    Show all available API versions"
            echo "  --json            Output in JSON format"
            echo "  --csv             Output in CSV format"
            echo "  -h, --help        Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 Microsoft.Storage"
            echo "  $0 Microsoft.Compute --all-versions"
            echo "  $0 Microsoft.Network --json"
            exit 0
            ;;
        *)
            if [[ -z "$PROVIDER" ]]; then
                PROVIDER="$1"
            else
                echo -e "${RED}Error: Unknown argument: $1${NC}"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate provider argument
if [[ -z "$PROVIDER" ]]; then
    echo -e "${RED}Error: Provider namespace is required${NC}"
    echo "Usage: $0 <provider-namespace>"
    echo "Example: $0 Microsoft.Storage"
    exit 1
fi

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Error: Azure CLI is not installed.${NC}"
    echo "Please install it from https://docs.microsoft.com/cli/azure/install-azure-cli"
    exit 1
fi

# Check if logged in
if ! az account show &> /dev/null; then
    echo -e "${RED}Error: Not logged in to Azure.${NC}"
    echo "Please run 'az login' first."
    exit 1
fi

echo -e "${CYAN}Fetching resource types for provider: $PROVIDER${NC}"
SUBSCRIPTION=$(az account show --query name -o tsv)
echo -e "${GRAY}Subscription: $SUBSCRIPTION${NC}"
echo ""

# Fetch resource types
if [[ "$SHOW_ALL_VERSIONS" == true ]]; then
    QUERY="resourceTypes[].{ResourceType:resourceType, ApiVersions:apiVersions}"
else
    QUERY="resourceTypes[].{ResourceType:resourceType, LatestApiVersion:apiVersions[0]}"
fi

RESULT=$(az provider show --namespace "$PROVIDER" --query "$QUERY" -o json 2>&1)

if [[ $? -ne 0 ]]; then
    echo -e "${RED}Error: Failed to fetch resource types${NC}"
    echo "$RESULT"
    exit 1
fi

# Check if empty
COUNT=$(echo "$RESULT" | jq 'length')
if [[ "$COUNT" == "0" || "$COUNT" == "null" ]]; then
    echo -e "${YELLOW}Warning: No resource types found for provider: $PROVIDER${NC}"
    echo "Make sure the provider is registered in your subscription."
    echo "Run: az provider register --namespace $PROVIDER"
    exit 0
fi

# Output based on format
case $OUTPUT_FORMAT in
    "table")
        if [[ "$SHOW_ALL_VERSIONS" == true ]]; then
            echo "$RESULT" | jq -r '.[] | "\n\u001b[32m'$PROVIDER'/\(.ResourceType)\u001b[0m\nAPI Versions:\n\(.ApiVersions | map("  " + .) | join("\n"))"'
        else
            echo -e "${YELLOW}Resource Type                                                Latest API Version${NC}"
            echo "--------------------------------------------------------------------------------"
            echo "$RESULT" | jq -r '.[] | "'$PROVIDER'/\(.ResourceType)|\(.LatestApiVersion)"' | \
                while IFS='|' read -r type version; do
                    printf "%-60s %s\n" "$type" "$version"
                done | sort
        fi
        echo ""
        echo -e "${CYAN}Total resource types: $COUNT${NC}"
        ;;
    "json")
        echo "$RESULT" | jq --arg provider "$PROVIDER" '[.[] | {
            FullResourceType: ($provider + "/" + .ResourceType),
            ResourceType: .ResourceType,
            ApiVersions: (if .ApiVersions then .ApiVersions else [.LatestApiVersion] end)
        }]'
        ;;
    "csv")
        echo "FullResourceType,ResourceType,ApiVersions"
        if [[ "$SHOW_ALL_VERSIONS" == true ]]; then
            echo "$RESULT" | jq -r --arg provider "$PROVIDER" '.[] | [$provider + "/" + .ResourceType, .ResourceType, (.ApiVersions | join(";"))] | @csv'
        else
            echo "$RESULT" | jq -r --arg provider "$PROVIDER" '.[] | [$provider + "/" + .ResourceType, .ResourceType, .LatestApiVersion] | @csv'
        fi
        ;;
esac

# Show Bicep usage example
echo ""
echo -e "${CYAN}Example Bicep usage:${NC}"
echo -e "${GRAY}resource myResource '$PROVIDER/<resourceType>@<apiVersion>' = {"
echo -e "  name: 'resourceName'"
echo -e "  location: location"
echo -e "  properties: {}"
echo -e "}${NC}"
