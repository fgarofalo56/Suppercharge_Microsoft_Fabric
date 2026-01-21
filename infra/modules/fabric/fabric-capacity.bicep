// =============================================================================
// Microsoft Fabric Capacity Module
// =============================================================================
// Deploys a Microsoft Fabric capacity with specified SKU
// =============================================================================

@description('Name of the Fabric capacity')
param capacityName string

@description('Azure region for deployment')
param location string

@description('Fabric capacity SKU')
@allowed(['F2', 'F4', 'F8', 'F16', 'F32', 'F64', 'F128', 'F256', 'F512', 'F1024', 'F2048'])
param skuName string = 'F64'

@description('Admin email address for the capacity')
param adminEmail string

@description('Tags to apply to resources')
param tags object = {}

// =============================================================================
// Resources
// =============================================================================

resource fabricCapacity 'Microsoft.Fabric/capacities@2023-11-01' = {
  name: capacityName
  location: location
  tags: tags
  sku: {
    name: skuName
    tier: 'Fabric'
  }
  properties: {
    administration: {
      members: [
        adminEmail
      ]
    }
  }
}

// =============================================================================
// Outputs
// =============================================================================

@description('The name of the Fabric capacity')
output capacityName string = fabricCapacity.name

@description('The resource ID of the Fabric capacity')
output capacityId string = fabricCapacity.id

@description('The SKU of the Fabric capacity')
output capacitySku string = fabricCapacity.sku.name

@description('The provisioning state of the capacity')
output provisioningState string = fabricCapacity.properties.provisioningState
