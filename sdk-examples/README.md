# SDK Examples

> **Home > SDK Examples**

---

## Overview

This directory contains code examples for programmatically interacting with Microsoft Fabric and related services. Use these examples for automation, integration, and custom tooling.

---

## Example Categories

| Category | Description | Language |
|----------|-------------|----------|
| [REST API](./rest-api/) | Fabric REST API examples | Python, PowerShell |
| [Python SDK](./python-sdk/) | Python client library examples | Python |
| [Semantic Link](./semantic-link/) | Power BI semantic model integration | Python |

---

## Quick Start

### Prerequisites

```bash
# Install Python dependencies
pip install azure-identity requests msal semantic-link

# Set environment variables
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export FABRIC_WORKSPACE_ID="your-workspace-id"
```

### Authentication Options

1. **Service Principal** (recommended for automation)
   ```python
   from azure.identity import ClientSecretCredential

   credential = ClientSecretCredential(
       tenant_id=os.getenv("AZURE_TENANT_ID"),
       client_id=os.getenv("AZURE_CLIENT_ID"),
       client_secret=os.getenv("AZURE_CLIENT_SECRET")
   )
   ```

2. **Azure CLI** (for development)
   ```python
   from azure.identity import AzureCliCredential
   credential = AzureCliCredential()
   ```

3. **Managed Identity** (for Azure-hosted workloads)
   ```python
   from azure.identity import ManagedIdentityCredential
   credential = ManagedIdentityCredential()
   ```

---

## REST API Examples

### List Workspaces

```python
from sdk_examples.python_sdk.fabric_api_examples import FabricClient, list_workspaces

client = FabricClient()
workspaces = list_workspaces(client)
for ws in workspaces:
    print(f"{ws['displayName']}: {ws['id']}")
```

### Trigger Pipeline Run

```python
from sdk_examples.python_sdk.fabric_api_examples import FabricClient, run_pipeline

client = FabricClient()
result = run_pipeline(
    client,
    workspace_id="workspace-guid",
    pipeline_id="pipeline-guid",
    parameters={"process_date": "2024-01-15"}
)
print(f"Pipeline triggered: {result}")
```

### Refresh Semantic Model

```python
from sdk_examples.python_sdk.fabric_api_examples import FabricClient, refresh_semantic_model

client = FabricClient()
refresh_semantic_model(
    client,
    workspace_id="workspace-guid",
    dataset_id="dataset-guid"
)
```

---

## Semantic Link Examples

### Query Semantic Model with DAX

```python
import sempy.fabric as fabric

# Execute DAX query
result = fabric.evaluate_dax(
    dataset="sm_casino_analytics",
    dax_string="""
    EVALUATE
    SUMMARIZECOLUMNS(
        'dim_date'[Date],
        "Revenue", [Net Gaming Revenue]
    )
    """
)
print(result)
```

### Read Table from Semantic Model

```python
import sempy.fabric as fabric

# Read entire table
df = fabric.read_table(
    dataset="sm_casino_analytics",
    table="fact_daily_slot_performance"
)
print(f"Rows: {len(df)}")
```

---

## PowerShell Examples

### Capacity Management

```powershell
# Pause Fabric capacity
$capacityId = "your-capacity-id"
$subscriptionId = "your-subscription-id"
$resourceGroup = "your-resource-group"

# Pause
az rest --method post `
  --url "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Fabric/capacities/$capacityId/suspend?api-version=2023-11-01"

# Resume
az rest --method post `
  --url "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Fabric/capacities/$capacityId/resume?api-version=2023-11-01"
```

### Workspace Export

```powershell
# Export workspace items
$workspaceId = "your-workspace-id"

# List items
$items = Invoke-RestMethod -Method Get `
  -Uri "https://api.fabric.microsoft.com/v1/workspaces/$workspaceId/items" `
  -Headers @{Authorization = "Bearer $token"}

$items.value | ForEach-Object {
    Write-Host "$($_.type): $($_.displayName)"
}
```

---

## Common Use Cases

### Automated Pipeline Orchestration

```python
def orchestrate_medallion_pipeline(client, workspace_id):
    """
    Orchestrate Bronze → Silver → Gold pipeline execution.
    """
    pipelines = {
        "bronze": "pl_bronze_ingestion",
        "silver": "pl_silver_transform",
        "gold": "pl_gold_aggregate"
    }

    for layer, pipeline_name in pipelines.items():
        print(f"Running {layer} pipeline...")
        result = run_pipeline(client, workspace_id, pipeline_name)

        # Wait for completion
        while True:
            status = get_pipeline_status(client, workspace_id, result["runId"])
            if status["status"] in ["Succeeded", "Failed"]:
                break
            time.sleep(30)

        if status["status"] == "Failed":
            raise Exception(f"{layer} pipeline failed!")

        print(f"{layer} complete")
```

### Scheduled Capacity Scaling

```python
def scale_capacity_for_workload(client, capacity_id, target_sku):
    """
    Scale capacity based on workload requirements.
    """
    url = f"https://management.azure.com/.../capacities/{capacity_id}"
    data = {"sku": {"name": target_sku}}

    response = client._request("PATCH", url, data=data)
    print(f"Capacity scaling to {target_sku}")
    return response
```

---

## Error Handling

```python
import requests
from requests.exceptions import HTTPError

def safe_api_call(client, method, url, **kwargs):
    """
    Wrapper with retry logic and error handling.
    """
    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            response = client._request(method, url, **kwargs)
            return response

        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                time.sleep(retry_delay * (attempt + 1))
                continue
            elif e.response.status_code >= 500:  # Server error
                time.sleep(retry_delay)
                continue
            else:
                raise

    raise Exception(f"API call failed after {max_retries} retries")
```

---

## Resources

- [Fabric REST API Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/)
- [Semantic Link Documentation](https://learn.microsoft.com/en-us/python/api/semantic-link/)
- [Azure Identity Library](https://learn.microsoft.com/en-us/python/api/azure-identity/)

---

[Back to Documentation](../docs/README.md)
