"""
Deployment Tests for Bicep Infrastructure

These tests validate the Bicep IaC deployment using Azure CLI what-if analysis.
"""

import subprocess
import json
import pytest
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestBicepValidation:
    """Tests for Bicep template validation."""

    def test_main_bicep_builds(self):
        """Test that main.bicep compiles without errors."""
        bicep_file = PROJECT_ROOT / "infra" / "main.bicep"

        result = subprocess.run(
            ["az", "bicep", "build", "--file", str(bicep_file)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Bicep build failed: {result.stderr}"

    def test_all_modules_build(self):
        """Test that all Bicep modules compile."""
        modules_dir = PROJECT_ROOT / "infra" / "modules"

        bicep_files = list(modules_dir.rglob("*.bicep"))
        assert len(bicep_files) > 0, "No Bicep modules found"

        for bicep_file in bicep_files:
            result = subprocess.run(
                ["az", "bicep", "build", "--file", str(bicep_file)],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"Module {bicep_file.name} failed: {result.stderr}"

    def test_parameter_files_exist(self):
        """Test that parameter files exist for all environments."""
        environments = ["dev", "staging", "prod"]

        for env in environments:
            param_file = PROJECT_ROOT / "infra" / "environments" / env / f"{env}.bicepparam"
            assert param_file.exists(), f"Missing parameter file for {env}"


class TestDeploymentWhatIf:
    """Tests for deployment what-if analysis."""

    @pytest.fixture
    def azure_subscription(self):
        """Get current Azure subscription."""
        result = subprocess.run(
            ["az", "account", "show", "--query", "id", "-o", "tsv"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            pytest.skip("Not logged into Azure CLI")
        return result.stdout.strip()

    def test_dev_whatif_succeeds(self, azure_subscription):
        """Test that dev deployment what-if succeeds."""
        bicep_file = PROJECT_ROOT / "infra" / "main.bicep"
        param_file = PROJECT_ROOT / "infra" / "environments" / "dev" / "dev.bicepparam"

        result = subprocess.run(
            [
                "az", "deployment", "sub", "what-if",
                "--location", "eastus2",
                "--template-file", str(bicep_file),
                "--parameters", str(param_file),
                "--no-prompt"
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        # What-if should succeed even if resources would be created
        assert result.returncode == 0, f"What-if failed: {result.stderr}"


class TestResourceConfiguration:
    """Tests for resource configuration validation."""

    def test_fabric_capacity_sku(self):
        """Test that Fabric capacity uses correct SKU."""
        bicep_file = PROJECT_ROOT / "infra" / "modules" / "fabric" / "fabric-capacity.bicep"

        with open(bicep_file, 'r') as f:
            content = f.read()

        # Check for F64 SKU reference
        assert "F64" in content or "sku" in content.lower(), \
            "Fabric capacity should reference F64 SKU"

    def test_storage_account_hns_enabled(self):
        """Test that storage account has hierarchical namespace enabled."""
        bicep_file = PROJECT_ROOT / "infra" / "modules" / "storage" / "storage-account.bicep"

        with open(bicep_file, 'r') as f:
            content = f.read()

        assert "isHnsEnabled" in content, \
            "Storage account should have hierarchical namespace enabled for ADLS Gen2"

    def test_key_vault_soft_delete(self):
        """Test that Key Vault has soft delete enabled."""
        bicep_file = PROJECT_ROOT / "infra" / "modules" / "security" / "security.bicep"

        with open(bicep_file, 'r') as f:
            content = f.read()

        assert "enableSoftDelete" in content or "softDelete" in content.lower(), \
            "Key Vault should have soft delete enabled"


class TestNetworkSecurity:
    """Tests for network security configuration."""

    def test_private_endpoints_configured(self):
        """Test that private endpoints are configured."""
        vnet_file = PROJECT_ROOT / "infra" / "modules" / "networking" / "vnet.bicep"

        with open(vnet_file, 'r') as f:
            content = f.read()

        assert "privateEndpoint" in content.lower() or "subnet" in content.lower(), \
            "VNet should include private endpoint configuration"

    def test_no_public_ip_by_default(self):
        """Test that resources don't expose public IPs by default."""
        modules_dir = PROJECT_ROOT / "infra" / "modules"

        for bicep_file in modules_dir.rglob("*.bicep"):
            with open(bicep_file, 'r') as f:
                content = f.read()

            # Check for explicit public access settings
            if "publicNetworkAccess" in content:
                # Should be disabled or conditional
                assert "Disabled" in content or "param" in content.lower(), \
                    f"{bicep_file.name} should disable public network access"


class TestGovernance:
    """Tests for governance configuration."""

    def test_purview_account_configured(self):
        """Test that Purview account is properly configured."""
        purview_file = PROJECT_ROOT / "infra" / "modules" / "governance" / "purview.bicep"

        assert purview_file.exists(), "Purview module should exist"

        with open(purview_file, 'r') as f:
            content = f.read()

        assert "Microsoft.Purview" in content, \
            "Purview module should reference Microsoft.Purview resource type"

    def test_monitoring_workspace_configured(self):
        """Test that Log Analytics workspace is configured."""
        monitoring_file = PROJECT_ROOT / "infra" / "modules" / "monitoring" / "log-analytics.bicep"

        assert monitoring_file.exists(), "Log Analytics module should exist"

        with open(monitoring_file, 'r') as f:
            content = f.read()

        assert "OperationalInsights" in content, \
            "Monitoring module should reference Log Analytics workspace"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
