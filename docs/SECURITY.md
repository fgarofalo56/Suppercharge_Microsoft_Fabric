# Security and Compliance Guide

This document outlines security controls, compliance requirements, and best practices for the Microsoft Fabric Casino/Gaming POC environment.

## Security Architecture

### Defense in Depth

```
┌────────────────────────────────────────────────────────────────────┐
│                        IDENTITY LAYER                               │
│  Azure AD | Conditional Access | MFA | PIM | RBAC                  │
├────────────────────────────────────────────────────────────────────┤
│                        NETWORK LAYER                                │
│  VNet | NSG | Private Endpoints | Firewall | DDoS Protection       │
├────────────────────────────────────────────────────────────────────┤
│                      APPLICATION LAYER                              │
│  Fabric Workspace Security | Row-Level Security | Object-Level     │
├────────────────────────────────────────────────────────────────────┤
│                         DATA LAYER                                  │
│  Encryption at Rest | Encryption in Transit | Key Vault | Purview  │
├────────────────────────────────────────────────────────────────────┤
│                       MONITORING LAYER                              │
│  Azure Monitor | Defender for Cloud | Sentinel | Audit Logs        │
└────────────────────────────────────────────────────────────────────┘
```

## Identity and Access Management

### Azure AD Integration

| Feature | Configuration |
|---------|--------------|
| Authentication | Azure AD SSO |
| MFA | Required for all users |
| Conditional Access | Location + device compliance |
| Session timeout | 8 hours (configurable) |

### Role-Based Access Control (RBAC)

#### Fabric Workspace Roles

| Role | Permissions | Typical Users |
|------|-------------|---------------|
| Admin | Full control | Workspace owners |
| Member | Edit all items | Data engineers |
| Contributor | Create/edit (no share) | Developers |
| Viewer | Read-only | Business users |

#### Custom RBAC Example

```json
{
  "Name": "Fabric Data Engineer",
  "Description": "Can manage data items but not workspace settings",
  "AssignableScopes": ["/subscriptions/{sub-id}"],
  "Permissions": [{
    "Actions": [
      "Microsoft.Fabric/capacities/read",
      "Microsoft.Fabric/workspaces/read",
      "Microsoft.Fabric/workspaces/items/*"
    ],
    "NotActions": [
      "Microsoft.Fabric/workspaces/delete",
      "Microsoft.Fabric/workspaces/write"
    ]
  }]
}
```

### Row-Level Security (RLS)

```dax
// DAX filter for player data - users see only their region
[Region] = USERPRINCIPALNAME()
  && RELATED(UserRegions[UserEmail]) = USERPRINCIPALNAME()

// Casino property filter
[PropertyID] IN VALUES(UserProperties[AllowedPropertyID])
```

## Data Protection

### Encryption

| Data State | Method | Key Management |
|------------|--------|----------------|
| At Rest | AES-256 | Microsoft-managed or CMK |
| In Transit | TLS 1.2+ | Azure-managed |
| In Use | Confidential computing (optional) | Azure Key Vault |

### Customer-Managed Keys (CMK)

```bicep
// Key Vault with CMK for Fabric
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  properties: {
    enablePurgeProtection: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    sku: {
      family: 'A'
      name: 'premium'  // Required for HSM-backed keys
    }
  }
}

resource encryptionKey 'Microsoft.KeyVault/vaults/keys@2023-07-01' = {
  parent: keyVault
  name: 'fabric-encryption-key'
  properties: {
    kty: 'RSA'
    keySize: 4096
    keyOps: ['encrypt', 'decrypt', 'wrapKey', 'unwrapKey']
  }
}
```

### Data Classification

| Classification | Examples | Controls |
|----------------|----------|----------|
| **Highly Confidential** | SSN, Full card numbers, Bank accounts | Encrypted, masked, audit logged |
| **Confidential** | Player PII, Win/loss records | RBAC, RLS, no export |
| **Internal** | Operational metrics, KPIs | Standard RBAC |
| **Public** | Aggregated reports | Open access |

### PII Handling

```python
# Example: PII masking in Silver layer
from pyspark.sql.functions import sha2, concat, lit, regexp_replace

def mask_pii(df):
    return df \
        .withColumn("ssn_hash", sha2(concat(col("ssn"), lit(SALT)), 256)) \
        .withColumn("ssn_masked", lit("XXX-XX-") + col("ssn").substr(-4, 4)) \
        .withColumn("card_masked",
            concat(lit("****-****-****-"), col("card_number").substr(-4, 4))) \
        .drop("ssn", "card_number")
```

## Network Security

### Private Endpoint Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Corporate Network                             │
│  ┌─────────────┐                                                │
│  │ User/Admin  │────────► ExpressRoute/VPN ──────┐              │
│  └─────────────┘                                 │              │
└──────────────────────────────────────────────────│──────────────┘
                                                   │
┌──────────────────────────────────────────────────▼──────────────┐
│                    Azure Virtual Network                         │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │  Fabric Subnet   │  │ Private Endpoint │                     │
│  │   10.0.1.0/24    │  │    Subnet        │                     │
│  │                  │  │   10.0.2.0/24    │                     │
│  │  - Fabric        │  │  - Storage PE    │                     │
│  │  - Dataflows     │  │  - Key Vault PE  │                     │
│  │                  │  │  - Purview PE    │                     │
│  └──────────────────┘  └──────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

### Network Security Groups (NSG)

```bicep
// NSG for Fabric subnet
resource fabricNsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: 'nsg-fabric-subnet'
  location: location
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
          destinationPortRange: '443'
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
          destinationPortRange: '*'
        }
      }
    ]
  }
}
```

## Compliance Requirements

### Gaming Industry (NIGC MICS)

| Requirement | Implementation |
|-------------|----------------|
| Meter accuracy | < 0.1% variance validation |
| Drop count verification | Daily reconciliation |
| Jackpot verification | W-2G >= $1,200 auto-generation |
| Access controls | Role-based + audit logging |
| Data retention | 5 years minimum |

### Financial (FinCEN BSA)

| Report | Threshold | Automation |
|--------|-----------|------------|
| CTR (Currency Transaction Report) | $10,000 | Auto-generate |
| SAR (Suspicious Activity Report) | Pattern-based | Alert + review |
| W-2G (Gambling Winnings) | $1,200 slots, $600 keno | Auto-generate |

```python
# CTR threshold detection
def detect_ctr_threshold(df):
    return df.filter(
        (col("transaction_type") == "CASH") &
        (col("amount") >= 10000)
    ).withColumn("ctr_required", lit(True))

# Structuring detection (SAR trigger)
def detect_structuring(df, window_hours=24):
    window_spec = Window.partitionBy("player_id") \
        .orderBy("transaction_time") \
        .rangeBetween(-window_hours * 3600, 0)

    return df.withColumn("rolling_total",
        sum("amount").over(window_spec)
    ).filter(
        (col("amount").between(8000, 9999)) &
        (col("rolling_total") >= 10000)
    )
```

### PCI-DSS

| Requirement | Control |
|-------------|---------|
| 3.4 - Render PAN unreadable | Hash/encrypt card numbers |
| 7.1 - Limit access | RBAC + need-to-know |
| 8.2 - MFA | Azure AD Conditional Access |
| 10.1 - Audit trails | Comprehensive logging |
| 12.3 - Security policies | Documented procedures |

## Audit and Monitoring

### Audit Log Configuration

```bicep
// Diagnostic settings for Fabric
resource fabricDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'fabric-audit-logs'
  scope: fabricCapacity
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        categoryGroup: 'audit'
        enabled: true
      }
      {
        categoryGroup: 'allLogs'
        enabled: true
      }
    ]
  }
}
```

### Key Audit Events

| Event Category | Examples | Retention |
|----------------|----------|-----------|
| Authentication | Login, logout, MFA challenges | 90 days |
| Authorization | Permission changes, access denied | 90 days |
| Data access | Query execution, data export | 1 year |
| Admin operations | Config changes, user management | 1 year |
| Security events | Threats detected, policies triggered | 2 years |

### Alerting Rules

```kusto
// KQL alert for suspicious data export
FabricAuditLogs
| where OperationName == "ExportData"
| where RecordCount > 10000
| summarize ExportCount = count(), TotalRecords = sum(RecordCount)
    by UserPrincipalName, bin(TimeGenerated, 1h)
| where ExportCount > 5 or TotalRecords > 100000
| project TimeGenerated, UserPrincipalName, ExportCount, TotalRecords
```

## Incident Response

### Security Incident Workflow

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  Detection │───▶│   Triage   │───▶│ Containment│───▶│ Eradication│
└────────────┘    └────────────┘    └────────────┘    └────────────┘
      │                 │                 │                 │
      ▼                 ▼                 ▼                 ▼
 Azure Sentinel    Security Team     Isolate User      Remove Threat
 Defender Alerts   Assessment       Revoke Access      Patch Systems
 Custom Alerts     Severity Rating  Block Network      Update Rules
                                                            │
                                   ┌────────────┐    ┌──────▼─────┐
                                   │   Review   │◀───│  Recovery  │
                                   └────────────┘    └────────────┘
                                         │
                                         ▼
                                   Update Policies
                                   Document Lessons
```

### Contact Matrix

| Severity | Response Time | Escalation |
|----------|---------------|------------|
| Critical | 15 minutes | SOC + Leadership |
| High | 1 hour | Security Team |
| Medium | 4 hours | On-call engineer |
| Low | Next business day | Ticket queue |

## Security Checklist

### Pre-Deployment

- [ ] Azure AD tenant hardened
- [ ] Conditional Access policies configured
- [ ] Key Vault created with proper access policies
- [ ] Network security groups defined
- [ ] Private endpoints planned (if required)

### Post-Deployment

- [ ] Fabric workspace roles assigned
- [ ] Row-level security implemented
- [ ] Audit logging enabled
- [ ] Alert rules configured
- [ ] Incident response plan documented
- [ ] Compliance controls validated

### Ongoing Operations

- [ ] Regular access reviews (quarterly)
- [ ] Vulnerability assessments (monthly)
- [ ] Penetration testing (annual)
- [ ] Compliance audits (as required)
- [ ] Security training (annual)

## References

- [Microsoft Fabric Security Documentation](https://learn.microsoft.com/fabric/security/)
- [Azure Security Best Practices](https://learn.microsoft.com/azure/security/fundamentals/best-practices-and-patterns)
- [NIGC MICS Standards](https://www.nigc.gov/compliance/minimum-internal-control-standards)
- [FinCEN BSA Regulations](https://www.fincen.gov/resources/statutes-and-regulations)
- [PCI-DSS Requirements](https://www.pcisecuritystandards.org/)
