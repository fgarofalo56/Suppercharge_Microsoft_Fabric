// =============================================================================
// Log Analytics Workspace Module
// =============================================================================
// Deploys Log Analytics for centralized monitoring
// =============================================================================

@description('Name of the Log Analytics workspace')
param name string

@description('Azure region for deployment')
param location string

@description('Retention period in days')
@minValue(30)
@maxValue(730)
param retentionInDays int = 90

@description('Tags to apply to resources')
param tags object = {}

// =============================================================================
// Log Analytics Workspace
// =============================================================================

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: retentionInDays
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping: {
      dailyQuotaGb: 10
    }
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// =============================================================================
// Data Collection Rules
// =============================================================================

// Performance counters solution
resource performanceSolution 'Microsoft.OperationsManagement/solutions@2015-11-01-preview' = {
  name: 'VMInsights(${logAnalytics.name})'
  location: location
  tags: tags
  plan: {
    name: 'VMInsights(${logAnalytics.name})'
    publisher: 'Microsoft'
    product: 'OMSGallery/VMInsights'
    promotionCode: ''
  }
  properties: {
    workspaceResourceId: logAnalytics.id
  }
}

// =============================================================================
// Saved Queries for Fabric Monitoring
// =============================================================================

resource fabricActivityQuery 'Microsoft.OperationalInsights/workspaces/savedSearches@2020-08-01' = {
  parent: logAnalytics
  name: 'FabricActivity'
  properties: {
    category: 'Fabric Monitoring'
    displayName: 'Fabric Activity Overview'
    query: '''
// Fabric activity overview
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.FABRIC"
| summarize Count = count() by OperationName, ResultType, bin(TimeGenerated, 1h)
| order by TimeGenerated desc
'''
    version: 2
  }
}

resource storageActivityQuery 'Microsoft.OperationalInsights/workspaces/savedSearches@2020-08-01' = {
  parent: logAnalytics
  name: 'StorageActivity'
  properties: {
    category: 'Fabric Monitoring'
    displayName: 'Storage Operations'
    query: '''
// Storage operations for Fabric data
StorageBlobLogs
| where OperationName in ("PutBlob", "GetBlob", "DeleteBlob")
| summarize Count = count(), TotalBytes = sum(ResponseBodySize) by OperationName, bin(TimeGenerated, 1h)
| order by TimeGenerated desc
'''
    version: 2
  }
}

resource keyVaultAccessQuery 'Microsoft.OperationalInsights/workspaces/savedSearches@2020-08-01' = {
  parent: logAnalytics
  name: 'KeyVaultAccess'
  properties: {
    category: 'Security'
    displayName: 'Key Vault Access Patterns'
    query: '''
// Key Vault access audit
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.KEYVAULT"
| where OperationName has "Secret" or OperationName has "Key"
| summarize Count = count() by OperationName, CallerIPAddress, bin(TimeGenerated, 1h)
| order by TimeGenerated desc
'''
    version: 2
  }
}

// =============================================================================
// Outputs
// =============================================================================

@description('The resource ID of the Log Analytics workspace')
output workspaceId string = logAnalytics.id

@description('The name of the Log Analytics workspace')
output workspaceName string = logAnalytics.name

@description('The customer ID of the Log Analytics workspace')
output workspaceCustomerId string = logAnalytics.properties.customerId
