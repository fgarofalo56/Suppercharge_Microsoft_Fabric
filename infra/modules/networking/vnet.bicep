// =============================================================================
// Virtual Network Module
// =============================================================================
// Deploys VNet with subnets for private endpoints
// =============================================================================

@description('Name of the Virtual Network')
param vnetName string

@description('Azure region for deployment')
param location string

@description('Address space for the VNet')
param addressSpace string = '10.0.0.0/16'

@description('Tags to apply to resources')
param tags object = {}

// =============================================================================
// Network Security Groups
// =============================================================================

resource privateEndpointNsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: 'nsg-private-endpoints'
  location: location
  tags: tags
  properties: {
    securityRules: [
      {
        name: 'AllowVNetInbound'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: '*'
          sourceAddressPrefix: 'VirtualNetwork'
          destinationAddressPrefix: 'VirtualNetwork'
          sourcePortRange: '*'
          destinationPortRange: '*'
        }
      }
      {
        name: 'DenyAllInbound'
        properties: {
          priority: 4096
          direction: 'Inbound'
          access: 'Deny'
          protocol: '*'
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
          sourcePortRange: '*'
          destinationPortRange: '*'
        }
      }
    ]
  }
}

resource fabricNsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: 'nsg-fabric'
  location: location
  tags: tags
  properties: {
    securityRules: [
      {
        name: 'AllowHTTPS'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: 'VirtualNetwork'
          destinationAddressPrefix: '*'
          sourcePortRange: '*'
          destinationPortRange: '443'
        }
      }
    ]
  }
}

// =============================================================================
// Virtual Network
// =============================================================================

resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: vnetName
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: [
        addressSpace
      ]
    }
    subnets: [
      {
        name: 'snet-fabric'
        properties: {
          addressPrefix: cidrSubnet(addressSpace, 24, 0) // 10.0.0.0/24
          networkSecurityGroup: {
            id: fabricNsg.id
          }
          serviceEndpoints: [
            {
              service: 'Microsoft.Storage'
            }
            {
              service: 'Microsoft.KeyVault'
            }
          ]
        }
      }
      {
        name: 'snet-private-endpoints'
        properties: {
          addressPrefix: cidrSubnet(addressSpace, 24, 1) // 10.0.1.0/24
          networkSecurityGroup: {
            id: privateEndpointNsg.id
          }
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
      {
        name: 'snet-management'
        properties: {
          addressPrefix: cidrSubnet(addressSpace, 24, 2) // 10.0.2.0/24
        }
      }
    ]
  }
}

// =============================================================================
// Outputs
// =============================================================================

@description('The resource ID of the VNet')
output vnetId string = vnet.id

@description('The name of the VNet')
output vnetName string = vnet.name

@description('The Fabric subnet ID')
output fabricSubnetId string = vnet.properties.subnets[0].id

@description('The Private Endpoint subnet ID')
output privateEndpointSubnetId string = vnet.properties.subnets[1].id

@description('The Management subnet ID')
output managementSubnetId string = vnet.properties.subnets[2].id
