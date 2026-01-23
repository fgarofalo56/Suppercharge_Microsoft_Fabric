# Microsoft Fabric - Complete Usage Guide

Comprehensive guide to using the Microsoft Fabric skill with Claude Code for managing Fabric workspaces, lakehouses, and OneLake operations.

## Table of Contents

- [How to Invoke This Skill](#how-to-invoke-this-skill)
- [Tools Overview](#tools-overview)
- [Complete Use Cases](#complete-use-cases)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)
- [Local-First Development](#local-first-development)

---

## How to Invoke This Skill

### Automatic Activation

Claude automatically activates this skill when you use these **trigger keywords**:

- `Fabric`, `Microsoft Fabric`, `Fabric workspace`
- `OneLake`, `lakehouse`, `Fabric lakehouse`
- `Fabric API`, `workspace management`
- `Fabric item`, `Fabric file`, `Fabric directory`
- `public APIs`, `Fabric REST API`

### Explicit Requests

Be clear about what Fabric operation you want to perform:

```
✅ GOOD: "List all items in my Fabric workspace"
✅ GOOD: "Download files from my OneLake lakehouse"
✅ GOOD: "Explore Fabric public APIs for workspace management"
✅ GOOD: "Create a new directory in OneLake"

⚠️ VAGUE: "Show me Fabric stuff"
⚠️ VAGUE: "Get my data"
```

### Example Invocation Patterns

```bash
# API exploration
"Show me available Fabric public APIs"
"Get details about the Workspace API"
"What's in the Fabric Platform API?"

# Workspace operations
"List all items in workspace abc-123"
"Show data items in my workspace"
"Create a new lakehouse item"

# OneLake file operations
"Download files from my lakehouse"
"Upload this CSV to OneLake"
"List all files in the sales directory"
"Delete old backup files from OneLake"
```

---

## Tools Overview

The skill provides 15 tools organized into two categories:

### API Access Tools (6 tools)

Tools for exploring and understanding Fabric REST APIs:

1. **publicapis_list** - List all available Fabric APIs
2. **publicapis_get** - Get details about a specific API
3. **publicapis_platform_get** - Get platform API collection details
4. **publicapis_bestpractices_get** - Get best practices for APIs
5. **publicapis_bestpractices_examples_get** - Get API usage examples
6. **publicapis_bestpractices_itemdefinition_get** - Get item definition examples

### OneLake Management Tools (9 tools)

Tools for managing files and directories in OneLake:

**File Operations**:
- **onelake_download_file** - Download file from OneLake
- **onelake_upload_file** - Upload file to OneLake
- **onelake_list_files** - List files in directory
- **onelake_delete_file** - Delete file from OneLake

**Directory Operations**:
- **onelake_create_directory** - Create new directory
- **onelake_delete_directory** - Delete directory

**Item Operations**:
- **onelake_list_items** - List workspace items
- **onelake_list_data_items** - List data-specific items
- **onelake_create_item** - Create new Fabric item

---

## Complete Use Cases

### Use Case 1: Exploring Fabric APIs Before Development

**Scenario**: You're building a custom application and need to understand available Fabric APIs

**Step-by-step workflow**:

1. **List all available APIs**:
```
Request: "List all Fabric public APIs"

Claude returns:
- Workspace API
- Lakehouse API
- Item API
- Pipeline API
- Notebook API
- Semantic Model API
... and more
```

2. **Get specific API details**:
```
Request: "Get details about the Fabric Workspace API"

Claude provides:
- Base URL
- Available endpoints
- Authentication requirements
- Supported operations (CRUD)
- Resource schemas
```

3. **Get best practices**:
```
Request: "Show me best practices for using Fabric APIs"

Claude returns:
- Authentication patterns
- Rate limiting guidance
- Error handling
- Pagination strategies
- Caching recommendations
```

4. **Get code examples**:
```
Request: "Get examples of creating items with Fabric API"

Claude provides working code:
```

```python
import requests

# Authentication
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Create lakehouse
workspace_id = 'abc-123-def-456'
url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items'

payload = {
    'displayName': 'Sales Lakehouse',
    'type': 'Lakehouse',
    'description': 'Lakehouse for sales data'
}

response = requests.post(url, json=payload, headers=headers)
lakehouse = response.json()
print(f'Created lakehouse: {lakehouse["id"]}')
```

**Expected outcome**:
- Full understanding of available APIs
- Working code examples
- Best practices for implementation
- Ready to build Fabric integrations

---

### Use Case 2: Managing Workspace Items

**Scenario**: Organize and manage items in your Fabric workspace

**Step-by-step workflow**:

1. **List all items**:
```
Request: "List all items in my Fabric workspace abc-123"

Claude returns:
Workspace: abc-123
Items (25 total):
- Lakehouse: Sales Data (id: lh-001)
- Lakehouse: Marketing Data (id: lh-002)
- Notebook: Data Analysis (id: nb-001)
- Pipeline: Daily ETL (id: pipe-001)
- Semantic Model: Sales Dashboard (id: sm-001)
...
```

2. **Filter to data items only**:
```
Request: "Show only data items (lakehouses, warehouses) in workspace abc-123"

Claude returns:
Data Items (10):
- Lakehouse: Sales Data
- Lakehouse: Marketing Data
- Lakehouse: Customer 360
- Warehouse: Analytics DW
...
```

3. **Create new lakehouse**:
```
Request: "Create a new lakehouse called 'Product Analytics' in workspace abc-123"

Claude creates lakehouse and returns:
✓ Lakehouse created successfully
Name: Product Analytics
ID: lh-new-123
Type: Lakehouse
Workspace: abc-123
OneLake path: /workspaces/abc-123/lakehouses/lh-new-123
```

4. **Verify creation**:
```
Request: "List lakehouses in workspace abc-123"

Claude shows updated list including new lakehouse
```

**Expected outcome**:
- Clear view of workspace contents
- New lakehouse created
- Organized by item type
- Ready for data operations

---

### Use Case 3: File Operations in OneLake

**Scenario**: Upload, download, and manage files in OneLake lakehouse

**Step-by-step workflow**:

1. **List current files**:
```
Request: "List all files in my lakehouse lh-001 in workspace abc-123"

Claude returns:
Lakehouse: Sales Data (lh-001)
Files:
/Files/
  /data/
    sales-2024-01.csv (2.3 MB)
    sales-2024-02.csv (2.1 MB)
    sales-2024-03.csv (2.4 MB)
  /raw/
    import-log.txt (15 KB)
  /processed/
    aggregated-sales.parquet (1.2 MB)
```

2. **Upload new files**:
```
Request: "Upload sales-2024-04.csv to /Files/data/ in lakehouse lh-001"

Claude uploads and confirms:
✓ File uploaded successfully
Path: /Files/data/sales-2024-04.csv
Size: 2.2 MB
Lakehouse: lh-001
Workspace: abc-123
```

3. **Create organized directory structure**:
```
Request: "Create directory structure /Files/archive/2024/Q1 in lakehouse lh-001"

Claude creates nested directories:
✓ Created: /Files/archive
✓ Created: /Files/archive/2024
✓ Created: /Files/archive/2024/Q1
```

4. **Download for local processing**:
```
Request: "Download aggregated-sales.parquet from lakehouse lh-001 to local /data folder"

Claude downloads:
✓ Downloaded successfully
Source: /Files/processed/aggregated-sales.parquet
Destination: /data/aggregated-sales.parquet
Size: 1.2 MB
```

5. **Clean up old files**:
```
Request: "Delete sales files older than Q1 2024 from lakehouse lh-001"

Claude identifies and removes:
Deleted 12 files:
- /Files/data/sales-2023-10.csv
- /Files/data/sales-2023-11.csv
- /Files/data/sales-2023-12.csv
...
Total space freed: 28.4 MB
```

**Expected outcome**:
- Files uploaded to OneLake
- Organized directory structure
- Downloaded files for analysis
- Old files cleaned up
- Storage optimized

---

### Use Case 4: Data Pipeline File Management

**Scenario**: Manage input/output files for a data pipeline

**Step-by-step workflow**:

1. **Check for new input files**:
```
Request: "List files in /Files/input/ directory of lakehouse lh-pipeline"

Claude returns:
Input Files (5 new):
- customer-data-2024-12-15.csv (5.2 MB)
- product-data-2024-12-15.csv (1.1 MB)
- orders-data-2024-12-15.csv (8.3 MB)
- inventory-2024-12-15.csv (2.4 MB)
- returns-2024-12-15.csv (890 KB)
```

2. **Download for processing**:
```
Request: "Download all CSV files from /Files/input/ to local /pipeline/input/"

Claude downloads all files:
✓ Downloaded 5 files (17.9 MB total)
✓ Saved to /pipeline/input/
Ready for processing
```

3. **Process locally** (your code runs)

4. **Upload results**:
```
Request: "Upload all parquet files from /pipeline/output/ to lakehouse /Files/processed/"

Claude uploads results:
✓ Uploaded: customer-enriched.parquet (3.2 MB)
✓ Uploaded: orders-aggregated.parquet (4.1 MB)
✓ Uploaded: inventory-summary.parquet (890 KB)
Total: 3 files, 8.19 MB
```

5. **Archive input files**:
```
Request: "Move processed input files to /Files/archive/2024-12-15/"

Claude archives:
✓ Created archive directory
✓ Moved 5 input files to archive
✓ Cleared input directory
Input ready for next run
```

**Expected outcome**:
- Automated file management workflow
- Files downloaded for processing
- Results uploaded to Fabric
- Input files archived
- Pipeline ready for next run

---

### Use Case 5: Multi-Workspace File Sync

**Scenario**: Sync files between development and production workspaces

**Step-by-step workflow**:

1. **List files in dev workspace**:
```
Request: "List all files in lakehouse lh-dev in workspace ws-dev"

Claude returns development files
```

2. **Download from dev**:
```
Request: "Download all files from /Files/models/ in dev lakehouse to local /temp/models/"

Claude downloads:
✓ model-v2.pkl (45 MB)
✓ preprocessor.pkl (2.3 MB)
✓ config.json (4 KB)
```

3. **Upload to production**:
```
Request: "Upload files from /temp/models/ to lakehouse lh-prod in workspace ws-prod"

Claude uploads to production:
✓ model-v2.pkl → ws-prod/lh-prod/Files/models/
✓ preprocessor.pkl → ws-prod/lh-prod/Files/models/
✓ config.json → ws-prod/lh-prod/Files/models/
Production updated with latest models
```

4. **Verify sync**:
```
Request: "List files in both dev and prod lakehouses, compare"

Claude compares:
Development (/Files/models/):
- model-v2.pkl (45 MB, modified 2024-12-15)
- preprocessor.pkl (2.3 MB, modified 2024-12-15)
- config.json (4 KB, modified 2024-12-15)

Production (/Files/models/):
- model-v2.pkl (45 MB, modified 2024-12-15) ✓
- preprocessor.pkl (2.3 MB, modified 2024-12-15) ✓
- config.json (4 KB, modified 2024-12-15) ✓

Status: ✓ In sync
```

**Expected outcome**:
- Files synced between workspaces
- Production updated safely
- Verification complete
- Consistent across environments

---

## Workflow Examples

### Workflow 1: Setting Up New Lakehouse

```
1. "List all items in workspace ws-analytics"
   → See existing resources

2. "Create lakehouse 'Customer Analytics' in workspace ws-analytics"
   → Create lakehouse

3. "Create directory structure /Files/raw, /Files/processed, /Files/archive in lakehouse"
   → Organize storage

4. "Upload initial data files to /Files/raw/"
   → Load data

5. "List all files to verify setup"
   → Confirm structure
```

---

### Workflow 2: Daily Data Refresh

```
1. "Download yesterday's sales file from Fabric to local"
   → Get data

2. Process locally (your code)

3. "Upload processed files to /Files/processed/"
   → Update Fabric

4. "Move yesterday's raw file to archive"
   → Clean up

5. "List files to verify refresh completed"
   → Confirm
```

---

### Workflow 3: API-Driven Automation

```
1. "Show me Fabric API best practices for automation"
   → Learn patterns

2. "Get examples of bulk item operations"
   → See code

3. Implement custom automation script

4. "Test by listing items via API"
   → Verify connection

5. Deploy automation
```

---

## Best Practices

### 1. Workspace Organization

```
✅ GOOD:
- Group related lakehouses in workspace
- Use descriptive names (Sales-Prod, Marketing-Dev)
- Maintain separate dev/test/prod workspaces
- Document workspace purpose

❌ BAD:
- All lakehouses in one workspace
- Generic names (lakehouse1, lakehouse2)
- Mixing environments
```

---

### 2. File Structure

```
✅ GOOD:
/Files/
  /raw/           # Original data
  /processed/     # Transformed data
  /archive/       # Historical data
  /config/        # Configuration files
  /logs/          # Processing logs

❌ BAD:
/Files/
  file1.csv
  file2.csv
  old_file.csv
  (no organization)
```

---

### 3. File Naming Conventions

```
✅ GOOD:
- sales-2024-12-15.csv (date-based)
- customer-enriched-v2.parquet (versioned)
- orders-aggregated-2024-Q4.parquet (time-bound)

❌ BAD:
- data.csv (too generic)
- file_final_FINAL_v2.csv (unclear)
- temp123.parquet (no context)
```

---

### 4. API Usage

```
✅ GOOD:
- Cache API responses locally
- Implement retry logic with backoff
- Use pagination for large result sets
- Handle rate limits gracefully
- Log all API operations

❌ BAD:
- No caching (repeated calls)
- No error handling
- Loading all results at once
- Ignoring rate limits
```

---

### 5. Data Management

```
✅ GOOD:
- Regular archival of old data
- Compression of large files
- Delete temporary files after use
- Monitor storage usage
- Document data lineage

❌ BAD:
- Never delete old files
- Store uncompressed data
- Accumulate temp files
- No storage monitoring
```

---

## Local-First Development

This skill is designed for **local-first** workflows:

### What "Local-First" Means

The skill operates primarily with local files and uses OneLake as a **storage layer**:

```
Local Files ↔ OneLake Storage ↔ Fabric Compute

Your code runs locally
Files stored in OneLake
Fabric provides infrastructure
```

---

### Typical Workflow

```
1. Download data from OneLake
   ↓
2. Process locally (Python, R, etc.)
   ↓
3. Upload results to OneLake
   ↓
4. Fabric notebooks/pipelines access results
```

---

### Benefits

- **Flexibility**: Use any local tools
- **Speed**: No network latency during processing
- **Control**: Full control over environment
- **Cost**: Only pay for storage and Fabric compute when needed

---

### When to Use Fabric Compute vs. Local

**Use Local Processing** when:
- Developing and testing code
- Small to medium datasets
- Need specific libraries
- Iterating quickly

**Use Fabric Compute** when:
- Very large datasets (>100GB)
- Need distributed processing (Spark)
- Scheduled/automated pipelines
- Team collaboration required

---

## Advanced Patterns

### Pattern 1: Version-Controlled Data

```
/Files/
  /models/
    /v1/
      model.pkl
      metadata.json
    /v2/
      model.pkl
      metadata.json
    /current/ → symlink to /v2
```

**Request**:
```
"Upload my model to /Files/models/v3/ and update /current/ to point to v3"
```

---

### Pattern 2: Environment-Based Structure

```
Development Workspace:
- lakehouse-dev
  /Files/
    /staging/
    /test/

Production Workspace:
- lakehouse-prod
  /Files/
    /live/
    /archive/
```

**Request**:
```
"Sync staging files from dev to production after validation"
```

---

### Pattern 3: Metadata-Driven Processing

```
/Files/
  /data/
    sales.csv
    sales.csv.meta (JSON with schema, lineage, etc.)
  /processed/
    sales-clean.parquet
    sales-clean.parquet.meta
```

**Request**:
```
"Upload data file with accompanying metadata JSON"
```

---

## Additional Resources

- [SKILL.md](SKILL.md) - Main skill instructions
- [reference.md](reference.md) - Complete tool reference
- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [OneLake Documentation](https://learn.microsoft.com/fabric/onelake/)
- [Fabric REST API Reference](https://learn.microsoft.com/rest/api/fabric/)

---

## Quick Reference

### Common Commands

```bash
# API exploration
"List all Fabric public APIs"
"Get Workspace API details"
"Show Fabric API best practices"

# Workspace management
"List items in workspace {id}"
"Create lakehouse {name} in workspace {id}"
"Show only data items"

# File operations
"Download {file} from lakehouse {id}"
"Upload {file} to lakehouse {id}"
"List files in {directory}"
"Delete {file}"

# Directory operations
"Create directory {path}"
"Delete directory {path}"
```

---

## Troubleshooting

### Issue: "Workspace not found"
- Verify workspace ID is correct
- Check you have access permissions
- Ensure workspace exists in correct capacity

### Issue: "File upload fails"
- Check file size (OneLake limits)
- Verify lakehouse path is correct
- Ensure you have write permissions
- Check network connectivity

### Issue: "API returns 429 (rate limit)"
- Implement exponential backoff
- Reduce request frequency
- Cache responses when possible
- Consider batch operations

### Issue: "Cannot list items"
- Verify workspace permissions
- Check API token is valid
- Ensure workspace is not paused
- Try refreshing authentication

---

## Questions?

**Q: Do I need to authenticate separately?**
A: Yes, you need Azure AD authentication. The skill works with authenticated requests.

**Q: Can I access files from multiple workspaces?**
A: Yes, specify workspace ID for each operation.

**Q: What file formats are supported?**
A: All formats - OneLake is file-based storage (CSV, Parquet, JSON, etc.)

**Q: Is there a file size limit?**
A: OneLake supports large files, but API upload limits may apply (typically 100MB per call).

**Q: Can I automate these operations?**
A: Yes! Use the API best practices to build automation scripts.
