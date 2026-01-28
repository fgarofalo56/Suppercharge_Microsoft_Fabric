"""
Microsoft Fabric Python SDK Examples
====================================

This module demonstrates common operations using the Fabric REST API
and Python SDK for casino analytics automation.

Prerequisites:
    pip install azure-identity requests msal

Authentication:
    Uses Azure AD authentication with service principal or user credentials.
"""

import os
import json
import time
from datetime import datetime
from typing import Optional, List, Dict, Any

import requests
from azure.identity import DefaultAzureCredential, ClientSecretCredential

# =============================================================================
# CONFIGURATION
# =============================================================================

FABRIC_API_BASE = "https://api.fabric.microsoft.com/v1"
POWER_BI_API_BASE = "https://api.powerbi.com/v1.0/myorg"

# Environment variables (set these or use .env file)
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID")


# =============================================================================
# AUTHENTICATION
# =============================================================================

class FabricClient:
    """Client for interacting with Microsoft Fabric REST API."""

    def __init__(
        self,
        tenant_id: str = None,
        client_id: str = None,
        client_secret: str = None
    ):
        """
        Initialize Fabric client with authentication.

        Args:
            tenant_id: Azure AD tenant ID
            client_id: Service principal client ID
            client_secret: Service principal client secret
        """
        self.tenant_id = tenant_id or TENANT_ID
        self.client_id = client_id or CLIENT_ID
        self.client_secret = client_secret or CLIENT_SECRET

        if self.client_id and self.client_secret:
            self.credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
        else:
            # Use default credential (Azure CLI, managed identity, etc.)
            self.credential = DefaultAzureCredential()

        self._token = None
        self._token_expiry = None

    def _get_token(self) -> str:
        """Get or refresh access token."""
        if self._token and self._token_expiry and datetime.now() < self._token_expiry:
            return self._token

        # Get token for Fabric API
        token = self.credential.get_token("https://api.fabric.microsoft.com/.default")
        self._token = token.token
        self._token_expiry = datetime.fromtimestamp(token.expires_on - 60)

        return self._token

    def _headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json"
        }

    def _request(
        self,
        method: str,
        url: str,
        data: Dict = None,
        params: Dict = None
    ) -> Dict:
        """Make authenticated request to Fabric API."""
        response = requests.request(
            method=method,
            url=url,
            headers=self._headers(),
            json=data,
            params=params
        )

        if response.status_code == 202:
            # Long-running operation - return operation ID
            return {"operationId": response.headers.get("x-ms-operation-id")}

        response.raise_for_status()

        if response.content:
            return response.json()
        return {}


# =============================================================================
# WORKSPACE OPERATIONS
# =============================================================================

def list_workspaces(client: FabricClient) -> List[Dict]:
    """
    List all accessible workspaces.

    Returns:
        List of workspace objects
    """
    url = f"{FABRIC_API_BASE}/workspaces"
    response = client._request("GET", url)
    return response.get("value", [])


def get_workspace(client: FabricClient, workspace_id: str) -> Dict:
    """
    Get workspace details.

    Args:
        workspace_id: Workspace GUID

    Returns:
        Workspace object
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}"
    return client._request("GET", url)


def create_workspace(
    client: FabricClient,
    display_name: str,
    description: str = None,
    capacity_id: str = None
) -> Dict:
    """
    Create a new workspace.

    Args:
        display_name: Workspace name
        description: Optional description
        capacity_id: Optional capacity to assign

    Returns:
        Created workspace object
    """
    url = f"{FABRIC_API_BASE}/workspaces"
    data = {
        "displayName": display_name,
        "description": description or ""
    }
    if capacity_id:
        data["capacityId"] = capacity_id

    return client._request("POST", url, data=data)


# =============================================================================
# LAKEHOUSE OPERATIONS
# =============================================================================

def list_lakehouses(client: FabricClient, workspace_id: str) -> List[Dict]:
    """
    List lakehouses in a workspace.

    Args:
        workspace_id: Workspace GUID

    Returns:
        List of lakehouse objects
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}/lakehouses"
    response = client._request("GET", url)
    return response.get("value", [])


def create_lakehouse(
    client: FabricClient,
    workspace_id: str,
    display_name: str,
    description: str = None
) -> Dict:
    """
    Create a new lakehouse.

    Args:
        workspace_id: Workspace GUID
        display_name: Lakehouse name
        description: Optional description

    Returns:
        Created lakehouse object
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}/lakehouses"
    data = {
        "displayName": display_name,
        "description": description or ""
    }
    return client._request("POST", url, data=data)


def get_lakehouse_tables(
    client: FabricClient,
    workspace_id: str,
    lakehouse_id: str
) -> List[Dict]:
    """
    List tables in a lakehouse.

    Args:
        workspace_id: Workspace GUID
        lakehouse_id: Lakehouse GUID

    Returns:
        List of table objects
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables"
    response = client._request("GET", url)
    return response.get("value", [])


# =============================================================================
# PIPELINE OPERATIONS
# =============================================================================

def list_pipelines(client: FabricClient, workspace_id: str) -> List[Dict]:
    """
    List data pipelines in a workspace.

    Args:
        workspace_id: Workspace GUID

    Returns:
        List of pipeline objects
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}/dataPipelines"
    response = client._request("GET", url)
    return response.get("value", [])


def run_pipeline(
    client: FabricClient,
    workspace_id: str,
    pipeline_id: str,
    parameters: Dict = None
) -> Dict:
    """
    Trigger a pipeline run.

    Args:
        workspace_id: Workspace GUID
        pipeline_id: Pipeline GUID
        parameters: Optional pipeline parameters

    Returns:
        Run information
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/jobs/instances?jobType=Pipeline"
    data = {"executionData": {"parameters": parameters or {}}}
    return client._request("POST", url, data=data)


def get_pipeline_runs(
    client: FabricClient,
    workspace_id: str,
    pipeline_id: str
) -> List[Dict]:
    """
    Get pipeline run history.

    Args:
        workspace_id: Workspace GUID
        pipeline_id: Pipeline GUID

    Returns:
        List of run objects
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/jobs/instances"
    response = client._request("GET", url)
    return response.get("value", [])


# =============================================================================
# NOTEBOOK OPERATIONS
# =============================================================================

def list_notebooks(client: FabricClient, workspace_id: str) -> List[Dict]:
    """
    List notebooks in a workspace.

    Args:
        workspace_id: Workspace GUID

    Returns:
        List of notebook objects
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}/notebooks"
    response = client._request("GET", url)
    return response.get("value", [])


def run_notebook(
    client: FabricClient,
    workspace_id: str,
    notebook_id: str,
    parameters: Dict = None
) -> Dict:
    """
    Execute a notebook.

    Args:
        workspace_id: Workspace GUID
        notebook_id: Notebook GUID
        parameters: Optional notebook parameters

    Returns:
        Execution information
    """
    url = f"{FABRIC_API_BASE}/workspaces/{workspace_id}/notebooks/{notebook_id}/jobs/instances?jobType=RunNotebook"
    data = {"executionData": {"parameters": parameters or {}}}
    return client._request("POST", url, data=data)


# =============================================================================
# CAPACITY OPERATIONS
# =============================================================================

def list_capacities(client: FabricClient) -> List[Dict]:
    """
    List available Fabric capacities.

    Returns:
        List of capacity objects
    """
    url = f"{FABRIC_API_BASE}/capacities"
    response = client._request("GET", url)
    return response.get("value", [])


def get_capacity(client: FabricClient, capacity_id: str) -> Dict:
    """
    Get capacity details.

    Args:
        capacity_id: Capacity GUID

    Returns:
        Capacity object
    """
    url = f"{FABRIC_API_BASE}/capacities/{capacity_id}"
    return client._request("GET", url)


# =============================================================================
# SEMANTIC MODEL (DATASET) OPERATIONS
# =============================================================================

def refresh_semantic_model(
    client: FabricClient,
    workspace_id: str,
    dataset_id: str
) -> Dict:
    """
    Trigger semantic model refresh.

    Args:
        workspace_id: Workspace GUID
        dataset_id: Dataset/Semantic Model GUID

    Returns:
        Refresh information
    """
    url = f"{POWER_BI_API_BASE}/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
    return client._request("POST", url)


def get_refresh_history(
    client: FabricClient,
    workspace_id: str,
    dataset_id: str
) -> List[Dict]:
    """
    Get semantic model refresh history.

    Args:
        workspace_id: Workspace GUID
        dataset_id: Dataset GUID

    Returns:
        List of refresh objects
    """
    url = f"{POWER_BI_API_BASE}/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
    response = client._request("GET", url)
    return response.get("value", [])


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def main():
    """Example usage of Fabric API client."""

    # Initialize client
    client = FabricClient()

    # List workspaces
    print("=== Workspaces ===")
    workspaces = list_workspaces(client)
    for ws in workspaces[:5]:
        print(f"  - {ws['displayName']} ({ws['id']})")

    # Get workspace details
    if WORKSPACE_ID:
        print(f"\n=== Workspace Details ===")
        workspace = get_workspace(client, WORKSPACE_ID)
        print(f"  Name: {workspace['displayName']}")
        print(f"  Capacity: {workspace.get('capacityId', 'N/A')}")

        # List lakehouses
        print(f"\n=== Lakehouses ===")
        lakehouses = list_lakehouses(client, WORKSPACE_ID)
        for lh in lakehouses:
            print(f"  - {lh['displayName']} ({lh['id']})")

        # List pipelines
        print(f"\n=== Pipelines ===")
        pipelines = list_pipelines(client, WORKSPACE_ID)
        for pl in pipelines:
            print(f"  - {pl['displayName']} ({pl['id']})")

        # List notebooks
        print(f"\n=== Notebooks ===")
        notebooks = list_notebooks(client, WORKSPACE_ID)
        for nb in notebooks:
            print(f"  - {nb['displayName']} ({nb['id']})")


if __name__ == "__main__":
    main()
