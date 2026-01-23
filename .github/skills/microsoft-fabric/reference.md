# Microsoft Fabric MCP Server Reference

Quick reference for all Fabric MCP Server tools.

## Tool Categories

- **API Access** (6 tools) - Access API specs, schemas, and best practices
- **File Operations** (4 tools) - Download, upload, list, delete files
- **Directory Operations** (2 tools) - Create and delete directories
- **Item Operations** (3 tools) - List, create, and manage Fabric items

## API Access Tools

### publicapis_list
- **Returns:** List of all Fabric workload types
- **Parameters:** None
- **Use:** Discover available workloads

### publicapis_get
- **Returns:** Complete OpenAPI specification
- **Parameters:** workload (string)
- **Examples:** "DataPipeline", "Lakehouse", "SemanticModel"

### publicapis_platform_get
- **Returns:** Platform-level API spec
- **Parameters:** None
- **Use:** Cross-workload operations (workspaces, permissions)

### publicapis_bestpractices_get
- **Returns:** Best practice documentation
- **Parameters:** topic (string)
- **Topics:** pagination, error_handling, retry_backoff, authentication

### publicapis_bestpractices_examples_get
- **Returns:** Example API requests/responses
- **Parameters:** workload (string), example_type (optional)
- **Example types:** create, update, get, list, delete

### publicapis_bestpractices_itemdefinition_get
- **Returns:** JSON schema for item types
- **Parameters:** workload (string), item_type (string)
- **Use:** Get schema before creating items

## OneLake File Operations

### onelake download file
```
workspace: string (ID or name)
item: string (GUID or name.type)
path: string (OneLake path)
local_path: string (destination)
```

### onelake upload file
```
workspace: string
item: string
local_path: string (source)
onelake_path: string (destination)
```

### onelake file list
```
workspace: string
item: string
path: string (optional, default: root)
```

### onelake file delete
```
workspace: string
item: string
path: string (file to delete)
```

## OneLake Directory Operations

### onelake directory create
```
workspace: string
item: string
path: string (directory path)
```

### onelake directory delete
```
workspace: string
item: string
path: string
recursive: boolean (optional)
```

## OneLake Item Operations

### onelake item list
```
workspace: string
Returns: All items with metadata (ID, name, type, dates)
```

### onelake item list-data
```
workspace: string
Returns: Items via DFS endpoint
```

### onelake item create
```
workspace: string
item_type: string (Lakehouse, DataPipeline, Notebook, etc.)
display_name: string
description: string (optional)
definition: object (optional, item-specific config)
```

## Fabric Workload Types

| Workload | Item Type | Primary Use |
|----------|-----------|-------------|
| Lakehouse | `Lakehouse` | Delta Lake storage + SQL |
| Data Pipeline | `DataPipeline` | ETL and data integration |
| Semantic Model | `SemanticModel` | Power BI datasets |
| Notebook | `Notebook` | Interactive code (Python, Scala, R, SQL) |
| Warehouse | `Warehouse` | SQL data warehouse |
| KQL Database | `KQLDatabase` | Real-time analytics (Kusto) |
| Spark Job Definition | `SparkJobDefinition` | Batch Spark jobs |
| ML Model | `MLModel` | Machine learning models |
| ML Experiment | `MLExperiment` | ML experiment tracking |
| Eventhouse | `Eventhouse` | Event processing |

## OneLake File Structure

**Lakehouse:**
```
/Files/          # Unstructured files (CSV, JSON, Parquet)
/Tables/         # Delta tables
```

**Warehouse:**
```
/Tables/         # Warehouse tables
```

**Notebook:**
```
/notebook.ipynb  # Notebook file
```

## Item Name Formats

**GUID Format:**
```
550e8400-e29b-41d4-a716-446655440000
```

**Friendly Name Format:**
```
MyLakehouse.Lakehouse
DataPipeline1.DataPipeline
AnalyticsNotebook.Notebook
```

## Common Patterns

### Create Workspace Structure
```
1. onelake item create (Lakehouse)
2. onelake directory create (/Files/raw)
3. onelake directory create (/Files/processed)
4. onelake directory create (/Files/archive)
```

### Upload and Organize Data
```
1. onelake file list (check existing)
2. onelake upload file (upload data)
3. onelake file list (verify upload)
```

### Build Pipeline
```
1. publicapis_get (workload: "DataPipeline")
2. publicapis_bestpractices_itemdefinition_get (get schema)
3. publicapis_bestpractices_examples_get (see examples)
4. onelake item create (create pipeline with definition)
```

## Best Practice Topics

- **pagination** - Handling paginated API responses
- **error_handling** - Retry logic and error codes
- **retry_backoff** - Exponential backoff strategies
- **authentication** - Auth patterns and token management
- **rate_limiting** - Rate limit handling
- **api_versioning** - Version management

## Security Note

The Fabric MCP Server is **local-first** and runs entirely on your machine. It provides API specifications and schemas for reference - it does NOT connect to live Fabric environments or perform actual API calls against your Fabric resources.

## Additional Resources

- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Fabric REST API Reference](https://learn.microsoft.com/rest/api/fabric/)
- [OneLake Documentation](https://learn.microsoft.com/fabric/onelake/)
- [Fabric MCP Server GitHub](https://github.com/microsoft/mcp/tree/main/servers/Fabric.Mcp.Server)
