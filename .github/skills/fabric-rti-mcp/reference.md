# Fabric RTI MCP Server Reference

Complete tool reference for Microsoft Fabric Real-Time Intelligence.

## Tool Summary (38 Total)

- **Eventhouse/Kusto:** 12 tools
- **Eventstreams:** 17 tools
- **Activator:** 2 tools
- **Map:** 7 tools

## Eventhouse Tools (12)

### kusto_known_services
Lists configured Kusto services.

### kusto_query
Execute KQL queries.
- database: string
- query: string (KQL)

### kusto_command
Execute management commands.

### kusto_list_databases
List all databases in cluster.

### kusto_list_tables
List tables in database.
- database: string

### kusto_get_entities_schema
Get schema for tables/views/functions.
- database: string

### kusto_get_table_schema
Get detailed table schema.
- table_name: string
- database: string

### kusto_get_function_schema
Get function schema.
- function_name: string
- database: string

### kusto_sample_table_data
Sample random records.
- table_name: string
- sample_count: number (default: 10)

### kusto_sample_function_data
Sample function results.
- function_name: string
- parameters: object

### kusto_ingest_inline_into_table
Ingest CSV data.
- table_name: string
- csv_data: string

### kusto_get_shots
Get semantically similar query examples.
- query: string
- count: number

## Eventstream Tools (17)

### Core Operations (6)

**eventstream_list**
List Eventstreams in workspace.
- workspace_id: string

**eventstream_get**
Get Eventstream details.
- workspace_id: string
- item_id: string

**eventstream_get_definition**
Get JSON definition.
- workspace_id: string
- item_id: string

**eventstream_create**
Create new Eventstream.
- workspace_id: string
- display_name: string
- description: string (optional)

**eventstream_update**
Update Eventstream.
- workspace_id: string
- item_id: string
- display_name: string (optional)
- description: string (optional)

**eventstream_delete**
Delete Eventstream.
- workspace_id: string
- item_id: string

### Builder Tools (11)

**Session Management:**
- `eventstream_start_definition` - Begin new definition
- `eventstream_get_current_definition` - View current definition
- `eventstream_clear_definition` - Clear session

**Sources:**
- `eventstream_add_sample_data_source` - Add sample data
- `eventstream_add_custom_endpoint_source` - Add custom endpoint

**Streams:**
- `eventstream_add_derived_stream` - Add transformation stream

**Destinations:**
- `eventstream_add_eventhouse_destination` - Route to Eventhouse
- `eventstream_add_custom_endpoint_destination` - Route to endpoint

**Validation:**
- `eventstream_validate_definition` - Validate config
- `eventstream_create_from_definition` - Create from session
- `eventstream_list_available_components` - List component types

## Activator Tools (2)

### activator_list_artifacts
List Activator artifacts.
- workspace_id: string

### activator_create_trigger
Create trigger with alerting.
- workspace_id: string
- display_name: string
- description: string
- eventhouse_id: string
- kql_database_id: string
- query: string (KQL for monitoring)
- notification_type: "Email" | "Teams"
- recipients: array

## Map Tools (7)

### map_list
List Maps in workspace.
- workspace_id: string

### map_get
Get Map details.
- workspace_id: string
- item_id: string

### map_get_definition
Get Map JSON definition.
- workspace_id: string
- item_id: string

### map_create
Create new Map.
- workspace_id: string
- display_name: string
- description: string (optional)
- definition: object

### map_update_definition
Replace Map definition.
- workspace_id: string
- item_id: string
- definition: object

### map_update
Update Map properties.
- workspace_id: string
- item_id: string
- display_name: string (optional)
- description: string (optional)

### map_delete
Delete Map.
- workspace_id: string
- item_id: string

## Configuration

Environment Variables:
- `KUSTO_SERVICE_URI` - Default Eventhouse URI
- `KUSTO_SERVICE_DEFAULT_DB` - Default database
- `AZ_OPENAI_EMBEDDING_ENDPOINT` - For semantic search
- `FABRIC_API_BASE_URL` - Fabric API endpoint

## Authentication

Uses Azure Identity DefaultAzureCredential chain:
1. Environment Variables
2. Visual Studio
3. Azure CLI
4. Azure PowerShell
5. Azure Developer CLI
6. Interactive Browser

## Additional Resources

- [Fabric RTI Documentation](https://learn.microsoft.com/fabric/real-time-intelligence/)
- [KQL Reference](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
- [Eventstreams Documentation](https://learn.microsoft.com/fabric/real-time-intelligence/eventstreams/overview)
