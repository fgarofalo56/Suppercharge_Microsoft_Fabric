# Fabric Real-Time Intelligence MCP - Complete Usage Guide

Comprehensive guide to using the Fabric RTI MCP skill with Claude Code for KQL queries, Eventstreams, Activator triggers, and geo mapping in Microsoft Fabric.

## Table of Contents

- [How to Invoke This Skill](#how-to-invoke-this-skill)
- [Tools Overview](#tools-overview)
- [Complete Use Cases](#complete-use-cases)
- [Workflow Examples](#workflow-examples)
- [Performance & Monitoring](#performance--monitoring)
- [Best Practices](#best-practices)

---

## How to Invoke This Skill

### Automatic Activation

Claude automatically activates this skill when you use these **trigger keywords**:

- `KQL`, `Kusto`, `KQL query`, `Kusto query`
- `Eventhouse`, `real-time database`, `RTI database`
- `Eventstream`, `event streaming`, `real-time data`
- `Activator`, `alert`, `trigger`, `data alert`
- `geo map`, `map visualization`, `geographic data`
- `real-time intelligence`, `RTI`, `streaming analytics`

### Explicit Requests

Be clear about what real-time operation you want to perform:

```
✅ GOOD: "Run a KQL query to count events in the last hour"
✅ GOOD: "Create an Eventstream to ingest IoT sensor data"
✅ GOOD: "Set up an Activator trigger for temperature anomalies"
✅ GOOD: "Show sales data on a geographic map"

⚠️ VAGUE: "Query my data"
⚠️ VAGUE: "Set up alerts"
```

### Example Invocation Patterns

```bash
# KQL/Eventhouse queries
"Run KQL query to show top 10 errors from logs"
"Query Eventhouse for user activity in the last 24 hours"
"Show me table schema in the Eventhouse database"

# Eventstream operations
"Create an Eventstream to process IoT telemetry"
"Add Azure Event Hub as source to my Eventstream"
"Configure output destination for processed events"

# Activator triggers
"Create an alert when temperature exceeds 100 degrees"
"Set up Activator trigger for failed transactions"
"Configure notification when queue depth > 1000"

# Map visualizations
"Show customer locations on a map"
"Create a geographic visualization of sales by region"
"Map sensor locations with current status"
```

---

## Tools Overview

The skill provides 38 tools organized into 4 categories:

### Eventhouse/KQL Tools (12 tools)

Query and analyze real-time data with Kusto Query Language:

- **kusto_query** - Execute KQL queries
- **kusto_list_tables** - List all tables in database
- **kusto_sample_table_data** - Preview table data
- **kusto_show_schema** - Get table schema
- **kusto_list_databases** - List databases
- **kusto_show_table_stats** - Get table statistics
- **kusto_validate_query** - Validate KQL syntax
- **kusto_explain_query** - Analyze query execution plan
- **kusto_get_ingestion_status** - Check data ingestion
- **kusto_list_functions** - List stored functions
- **kusto_list_materialized_views** - List materialized views
- **kusto_get_query_results** - Fetch query results

### Eventstream Tools (17 tools)

Build and manage real-time data pipelines:

**Stream Management**:
- **eventstream_create** - Create new Eventstream
- **eventstream_list** - List all Eventstreams
- **eventstream_get** - Get Eventstream details
- **eventstream_update** - Update configuration
- **eventstream_delete** - Remove Eventstream
- **eventstream_start** - Start streaming
- **eventstream_stop** - Stop streaming

**Builder Tools**:
- **eventstream_add_source** - Add data source
- **eventstream_add_destination** - Add output destination
- **eventstream_add_transformation** - Add transformation step
- **eventstream_configure_schema** - Define data schema
- **eventstream_set_processing_mode** - Configure processing
- **eventstream_add_filter** - Add event filter
- **eventstream_add_aggregation** - Add aggregation logic

**Validation**:
- **eventstream_validate** - Validate configuration
- **eventstream_test** - Test with sample data
- **eventstream_monitor** - Monitor metrics

### Activator Tools (2 tools)

Create real-time alerts and triggers:

- **activator_list_artifacts** - List all Activator artifacts
- **activator_create_trigger** - Create new trigger/alert

### Map Tools (7 tools)

Visualize geographic data:

- **map_list** - List all map visualizations
- **map_create** - Create new map
- **map_update** - Update map configuration
- **map_delete** - Remove map
- **map_add_layer** - Add data layer
- **map_configure_style** - Set visual style
- **map_export** - Export map

---

## Complete Use Cases

### Use Case 1: Real-Time Log Analysis with KQL

**Scenario**: Monitor application logs in real-time and identify errors

**Step-by-step workflow**:

1. **List available tables**:
```
Request: "List all tables in my Eventhouse database"

Claude returns:
Database: prod-eventhouse
Tables (8):
- ApplicationLogs (45.2M rows, updated 5 seconds ago)
- UserActivity (128.4M rows, updated 2 seconds ago)
- SystemMetrics (89.3M rows, updated 1 second ago)
- ErrorEvents (2.3M rows, updated 10 seconds ago)
...
```

2. **Check table schema**:
```
Request: "Show me the schema for ApplicationLogs table"

Claude returns:
Table: ApplicationLogs
Columns:
- Timestamp (datetime) - Event timestamp
- Level (string) - Log level (Info, Warning, Error, Critical)
- Message (string) - Log message
- Source (string) - Application source
- RequestId (string) - Request correlation ID
- UserId (string) - User identifier
- Properties (dynamic) - Additional properties JSON
```

3. **Run analysis query**:
```
Request: "Run KQL query to show error count by source in the last hour"

Claude executes:
```

```kql
ApplicationLogs
| where Timestamp > ago(1h)
| where Level == "Error"
| summarize ErrorCount = count() by Source
| order by ErrorCount desc
| take 10
```

```
Results:
Source                  ErrorCount
-----------------------------------
API.PaymentService      847
API.AuthService         234
Worker.EmailProcessor   156
API.OrderService        89
Worker.DataSync         43
...
```

4. **Drill down into specific errors**:
```
Request: "Show me the most common error messages from PaymentService in the last hour"

Claude queries:
```

```kql
ApplicationLogs
| where Timestamp > ago(1h)
| where Source == "API.PaymentService"
| where Level == "Error"
| summarize Count = count() by Message
| order by Count desc
| take 5
```

```
Results:
Message                                          Count
--------------------------------------------------------
"Payment gateway timeout after 30s"              423
"Invalid credit card format"                     201
"Insufficient funds"                             134
"Payment declined by issuer"                     67
"Duplicate transaction detected"                 22
```

5. **Create time-based analysis**:
```
Request: "Show error trend for PaymentService over last 24 hours, grouped by hour"

Claude generates:
```

```kql
ApplicationLogs
| where Timestamp > ago(24h)
| where Source == "API.PaymentService"
| where Level == "Error"
| summarize ErrorCount = count() by bin(Timestamp, 1h)
| render timechart
```

**Expected outcome**:
- Real-time log analysis
- Error patterns identified
- Time-based trends visible
- Root causes discovered
- Ready to create alerts

---

### Use Case 2: IoT Sensor Data Pipeline with Eventstream

**Scenario**: Ingest, process, and route IoT sensor data in real-time

**Step-by-step workflow**:

1. **Create Eventstream**:
```
Request: "Create an Eventstream called 'IoT-Sensors' for processing temperature and humidity data"

Claude creates:
✓ Eventstream created
Name: IoT-Sensors
ID: es-iot-001
Status: Created (not started)
Processing Mode: Streaming
```

2. **Add data source**:
```
Request: "Add Azure IoT Hub as source to IoT-Sensors Eventstream"

Claude configures:
✓ Source added: Azure IoT Hub
Configuration:
- Connection: iot-hub-prod.azure-devices.net
- Consumer Group: fabric-rti
- Data Format: JSON
- Starting Position: Latest
```

3. **Define schema**:
```
Request: "Configure schema for IoT sensor events: deviceId, timestamp, temperature, humidity, location"

Claude sets schema:
✓ Schema configured
Fields:
- deviceId (string)
- timestamp (datetime)
- temperature (decimal)
- humidity (decimal)
- location (string)
```

4. **Add transformation**:
```
Request: "Add transformation to convert temperature from Celsius to Fahrenheit and flag high temperature readings"

Claude creates transformation:
✓ Transformation added
Logic:
```

```kql
| extend TempF = (temperature * 9/5) + 32
| extend HighTemp = iff(temperature > 30, true, false)
| extend AlertLevel = case(
    temperature > 40, "Critical",
    temperature > 30, "Warning",
    "Normal"
  )
```

5. **Add filter**:
```
Request: "Add filter to only pass through events with temperature above 25°C"

Claude adds filter:
✓ Filter added
Condition: temperature > 25
Estimated reduction: ~60% of events filtered out
```

6. **Add destinations**:
```
Request: "Send all events to Eventhouse and critical alerts to Event Hub"

Claude configures outputs:
✓ Destination 1: Eventhouse
  - Database: sensor-data
  - Table: SensorReadings
  - Ingestion: Streaming

✓ Destination 2: Event Hub (conditional)
  - Event Hub: critical-alerts
  - Condition: AlertLevel == "Critical"
  - Format: JSON
```

7. **Validate and test**:
```
Request: "Validate Eventstream configuration and test with sample data"

Claude validates:
✓ Configuration valid
✓ Schema validated
✓ Transformations tested
✓ Destinations reachable

Test Results (10 sample events):
- 8 events passed filter
- 2 events filtered out
- 1 critical alert triggered
- All events ingested to Eventhouse
```

8. **Start Eventstream**:
```
Request: "Start the IoT-Sensors Eventstream"

Claude starts:
✓ Eventstream started
Status: Running
Events/sec: 0 (warming up...)
```

9. **Monitor**:
```
Request: "Monitor Eventstream metrics"

Claude shows:
Eventstream: IoT-Sensors
Status: Running
Duration: 5 minutes

Metrics:
- Events received: 15,234
- Events processed: 15,234 (100%)
- Events filtered: 9,140 (60%)
- Eventhouse ingestion: 6,094 events
- Event Hub alerts: 23 events
- Processing latency: 127ms (avg)
- Throughput: 51 events/sec
```

**Expected outcome**:
- Real-time IoT data pipeline
- Automatic temperature conversion
- High-temperature filtering
- Multi-destination routing
- Critical alerts generated
- Data ingested to Eventhouse

---

### Use Case 3: Real-Time Alerting with Activator

**Scenario**: Create alerts for business-critical events

**Step-by-step workflow**:

1. **List existing triggers**:
```
Request: "List all Activator triggers in my workspace"

Claude returns:
Activator Artifacts (5):
1. High-Error-Rate (active)
   - Checks: Error count > 100/min
   - Action: Send Teams notification

2. Low-Inventory (active)
   - Checks: Product stock < 10
   - Action: Email procurement team

3. Payment-Failures (paused)
   - Checks: Failed payments > 5/min
   - Action: Alert on-call engineer
...
```

2. **Create new trigger**:
```
Request: "Create an Activator trigger for when average response time exceeds 2 seconds"

Claude creates:
✓ Trigger created
Name: Slow-Response-Alert
Type: Threshold
Conditions:
- Metric: ResponseTime
- Aggregation: avg
- Window: 5 minutes
- Threshold: > 2000ms
- Severity: Warning

Actions:
- Send email to: devops@company.com
- Post to Teams channel: #alerts
- Create incident ticket: Auto

Status: Active
```

3. **Create complex trigger**:
```
Request: "Create trigger for anomalous user activity: login failures > 5 in 2 minutes from same IP"

Claude configures:
✓ Trigger created
Name: Suspicious-Login-Activity
Type: Complex Event Processing

Conditions:
```

```kql
UserActivity
| where EventType == "LoginFailed"
| summarize FailureCount = count() by bin(Timestamp, 2m), IPAddress
| where FailureCount > 5
```

```
Actions:
- Block IP: Yes (automatic)
- Alert security team: High priority
- Log to security events: Yes
- Trigger: Fraud investigation workflow

Status: Active
Cooldown: 10 minutes (prevent alert storms)
```

4. **Create business metric trigger**:
```
Request: "Alert when hourly revenue drops below $10,000"

Claude creates:
✓ Trigger created
Name: Low-Revenue-Alert
Type: Business Metric

Data Source: EventHouse.SalesData
Query:
```

```kql
Sales
| where Timestamp > ago(1h)
| summarize Revenue = sum(Amount)
| project Revenue
```

```
Condition: Revenue < 10000
Check Frequency: Every 5 minutes

Actions:
- Notify: Sales leadership
- Dashboard: Mark as critical
- Escalation: After 15 minutes, notify CEO
```

**Expected outcome**:
- Real-time performance monitoring
- Automated security responses
- Business metric tracking
- Multi-channel notifications
- Escalation workflows

---

### Use Case 4: Geographic Sales Visualization

**Scenario**: Visualize sales data on an interactive map

**Step-by-step workflow**:

1. **Query sales data with location**:
```
Request: "Query sales data grouped by city with total revenue"

Claude queries:
```

```kql
Sales
| where Timestamp > ago(7d)
| summarize
    Revenue = sum(Amount),
    OrderCount = count(),
    AvgOrderValue = avg(Amount)
    by City, State, Country, Latitude, Longitude
| order by Revenue desc
```

```
Results (top 10):
City          Revenue   Orders  Lat       Lon
---------------------------------------------------
New York      $2.4M     5,234   40.7128  -74.0060
Los Angeles   $1.8M     3,892   34.0522  -118.2437
Chicago       $1.2M     2,567   41.8781  -87.6298
...
```

2. **Create map visualization**:
```
Request: "Create a map showing these sales locations with size proportional to revenue"

Claude creates:
✓ Map created
Name: Sales-Geographic-Analysis
Type: Bubble map

Configuration:
- Base map: OpenStreetMap
- Center: USA (auto-detected)
- Zoom level: 4

Data Layer:
- Source: Query results
- Latitude: Lat column
- Longitude: Lon column
- Bubble size: Revenue (proportional)
- Bubble color: Gradient (green to red by revenue)
- Tooltip: City, Revenue, Orders
```

3. **Add additional layers**:
```
Request: "Add a layer showing warehouse locations"

Claude adds layer:
✓ Layer added: Warehouses
Type: Icon layer
Icons: Warehouse symbol
Data: WarehouseLocations table
Color: Blue
Tooltip: Warehouse name, capacity
```

4. **Configure interactivity**:
```
Request: "Make bubbles clickable to drill down into city details"

Claude configures:
✓ Click action configured
On bubble click:
- Show detail panel
- Display: Top products, customer count, trends
- Link to: City-specific dashboard
```

5. **Add real-time updates**:
```
Request: "Make the map update in real-time as new sales come in"

Claude enables:
✓ Real-time refresh: Enabled
Refresh interval: 30 seconds
Data source: Live Eventstream
Animation: Pulse effect on new sales
```

**Expected outcome**:
- Interactive geographic visualization
- Real-time sales tracking
- Multi-layer insights
- Drill-down capabilities
- Decision-making tool

---

## Workflow Examples

### Workflow 1: Complete Real-Time Analytics Pipeline

```
1. "Create Eventstream for application telemetry"
   → Set up ingestion

2. "Add transformations to enrich events with user context"
   → Process data

3. "Route processed events to Eventhouse"
   → Store for analysis

4. "Create KQL queries for dashboard metrics"
   → Visualize data

5. "Set up Activator triggers for anomalies"
   → Alert on issues
```

---

### Workflow 2: IoT Monitoring Solution

```
1. "Create Eventstream from IoT Hub"
   → Ingest sensor data

2. "Add filter for anomalous readings"
   → Identify issues

3. "Send alerts to critical events queue"
   → Notify operators

4. "Store all data in Eventhouse"
   → Historical analysis

5. "Create map showing sensor locations and status"
   → Visual monitoring
```

---

### Workflow 3: Security Event Processing

```
1. "Ingest security logs via Eventstream"
   → Collect events

2. "Transform to extract key security fields"
   → Parse data

3. "Run KQL queries to detect patterns"
   → Analyze threats

4. "Create Activator triggers for suspicious activity"
   → Automated response

5. "Route critical events to SIEM"
   → Integration
```

---

## Performance & Monitoring

### Query Performance

**Best Practices**:
```kql
// ✅ GOOD: Filter early
SecurityLogs
| where Timestamp > ago(1h)
| where EventType == "LoginFailed"
| summarize count() by UserId

// ❌ BAD: Filter late
SecurityLogs
| summarize count() by UserId, EventType, Timestamp
| where Timestamp > ago(1h)
| where EventType == "LoginFailed"
```

### Eventstream Monitoring

**Key Metrics to Track**:
- Events/second (throughput)
- Processing latency
- Filter efficiency
- Destination success rate
- Error rate

**Monitoring Request**:
```
"Monitor Eventstream performance metrics every 5 minutes"
```

---

### Activator Performance

**Trigger Design**:
```
✅ GOOD:
- Specific conditions
- Appropriate time windows
- Cooldown periods
- Clear actions

❌ BAD:
- Overly broad conditions
- Too frequent checks
- No cooldown (alert storms)
- Unclear actions
```

---

## Best Practices

### KQL Query Optimization

```
1. Filter early: Use 'where' before 'summarize'
2. Limit columns: Project only needed columns
3. Time-bound queries: Always use time filters
4. Use materialized views: For frequent queries
5. Partition awareness: Leverage table partitioning
```

---

### Eventstream Design

```
1. Schema definition: Always define explicit schemas
2. Error handling: Configure retry policies
3. Batching: Use appropriate batch sizes
4. Monitoring: Enable metrics collection
5. Testing: Validate with sample data first
```

---

### Activator Configuration

```
1. Threshold setting: Balance sensitivity vs. noise
2. Time windows: Match business requirements
3. Cooldown periods: Prevent alert fatigue
4. Escalation: Define clear escalation paths
5. Documentation: Document trigger purposes
```

---

### Map Visualization

```
1. Data aggregation: Pre-aggregate for performance
2. Layer limits: Don't exceed 5-7 layers
3. Refresh rate: Balance real-time vs. performance
4. Zoom levels: Configure appropriate bounds
5. Tooltips: Provide concise, useful information
```

---

## Additional Resources

- [SKILL.md](SKILL.md) - Main skill instructions
- [reference.md](reference.md) - Complete tool reference
- [KQL Documentation](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
- [Fabric Real-Time Intelligence](https://learn.microsoft.com/fabric/real-time-intelligence/)
- [Eventstream Documentation](https://learn.microsoft.com/fabric/real-time-intelligence/event-streams/)

---

## Quick Reference

### Common Commands

```bash
# KQL queries
"Run KQL query to show errors in last hour"
"List tables in Eventhouse database"
"Show schema for {table}"

# Eventstream
"Create Eventstream for {data-source}"
"Add {source-type} as source"
"Configure transformation to {logic}"
"Start Eventstream"

# Activator
"Create trigger for {condition}"
"List all active triggers"
"Configure alert action"

# Maps
"Create map visualization of {data}"
"Add layer showing {locations}"
"Update map with real-time data"
```

---

## Troubleshooting

### Issue: "Query timeout"
- Reduce time range
- Add more filters early in query
- Use materialized views
- Check database capacity

### Issue: "Eventstream falling behind"
- Increase compute resources
- Optimize transformations
- Reduce filter complexity
- Check destination capacity

### Issue: "Activator false positives"
- Adjust threshold values
- Increase time window
- Add cooldown period
- Refine conditions with KQL

### Issue: "Map not loading"
- Check data format (lat/lon valid)
- Reduce data points (aggregate)
- Verify network connectivity
- Check browser console for errors

---

## Questions?

**Q: What's the difference between Eventhouse and OneLake?**
A: Eventhouse is optimized for real-time analytics with KQL. OneLake is file-based storage for batch/bulk data.

**Q: Can I query historical data with KQL?**
A: Yes! Eventhouse stores data indefinitely (configurable). Query any time range.

**Q: How fast is real-time?**
A: Eventstream latency is typically <1 second end-to-end for simple transformations.

**Q: What's the cost model?**
A: Based on compute (CU hours) and storage. Real-time features consume more compute than batch.

**Q: Can I integrate with external systems?**
A: Yes! Event Hub, IoT Hub, Kafka, custom APIs all supported as sources/destinations.
