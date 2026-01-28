# Teradata to Microsoft Fabric Migration Diagrams

## 1. High-Level Migration Architecture

```mermaid
flowchart TB
    subgraph Source["🏢 Teradata Source Environment"]
        TD_DW[(Teradata<br/>Data Warehouse)]
        TD_ETL[BTEQ/TPT<br/>Scripts]
        TD_PROC[Stored<br/>Procedures]
        TD_VIEWS[Views &<br/>Macros]
    end

    subgraph Migration["🔄 Migration Layer"]
        ADF[Azure Data Factory<br/>Pipelines]
        SHIR[Self-Hosted<br/>Integration Runtime]
        TRANS[SQL<br/>Translator]
        NB[Fabric<br/>Notebooks]
    end

    subgraph Target["☁️ Microsoft Fabric"]
        subgraph OneLake["OneLake"]
            LH_B[(Bronze<br/>Lakehouse)]
            LH_S[(Silver<br/>Lakehouse)]
            LH_G[(Gold<br/>Lakehouse)]
        end
        WH[(Fabric<br/>Warehouse)]
        SM[Semantic<br/>Model]
        PBI[Power BI<br/>Reports]
    end

    TD_DW -->|JDBC| SHIR
    SHIR --> ADF
    TD_ETL -->|Convert| NB
    TD_PROC -->|Translate| TRANS
    TD_VIEWS -->|Translate| TRANS

    ADF -->|Parquet| LH_B
    NB -->|Delta| LH_B
    TRANS -->|T-SQL| WH

    LH_B --> LH_S --> LH_G
    LH_G --> SM
    WH --> SM
    SM --> PBI

    style Source fill:#e74c3c,color:#fff
    style Migration fill:#f39c12,color:#fff
    style Target fill:#27ae60,color:#fff
```

---

## 2. Data Migration Pipeline Flow

```mermaid
flowchart LR
    subgraph Extract["📤 Extract"]
        LOOKUP[Lookup<br/>Table List]
        FOREACH[ForEach<br/>Table]
        COPY_TD[Copy from<br/>Teradata]
    end

    subgraph Transform["🔄 Transform"]
        PARQUET[Convert to<br/>Parquet]
        STAGE[Stage in<br/>OneLake]
    end

    subgraph Load["📥 Load"]
        COPY_IN[COPY INTO<br/>Delta Table]
        OPTIMIZE[OPTIMIZE<br/>& Z-ORDER]
        VALIDATE[Validate<br/>Row Counts]
    end

    LOOKUP --> FOREACH
    FOREACH --> COPY_TD
    COPY_TD --> PARQUET
    PARQUET --> STAGE
    STAGE --> COPY_IN
    COPY_IN --> OPTIMIZE
    OPTIMIZE --> VALIDATE

    style Extract fill:#3498db,color:#fff
    style Transform fill:#9b59b6,color:#fff
    style Load fill:#1abc9c,color:#fff
```

---

## 3. SQL Translation Decision Tree

```mermaid
flowchart TD
    START([Teradata SQL]) --> CHECK{Contains<br/>QUALIFY?}

    CHECK -->|Yes| QUALIFY[Convert to CTE<br/>with ROW_NUMBER]
    CHECK -->|No| SET_CHECK{Uses SET<br/>Table?}

    SET_CHECK -->|Yes| DEDUP[Add DISTINCT<br/>or UNIQUE constraint]
    SET_CHECK -->|No| FUNC_CHECK{Teradata<br/>Functions?}

    FUNC_CHECK -->|Yes| TRANSLATE[Map to T-SQL<br/>equivalents]
    FUNC_CHECK -->|No| DATE_CHECK{Date<br/>Arithmetic?}

    DATE_CHECK -->|Yes| DATEADD[Convert to<br/>DATEADD]
    DATE_CHECK -->|No| VALID[SQL is<br/>Compatible]

    QUALIFY --> VALID
    DEDUP --> VALID
    TRANSLATE --> VALID
    DATEADD --> VALID

    VALID --> OUTPUT([Fabric T-SQL])

    style START fill:#e74c3c,color:#fff
    style OUTPUT fill:#27ae60,color:#fff
```

---

## 4. Incremental Migration Pattern

```mermaid
sequenceDiagram
    participant TD as Teradata
    participant ADF as Data Factory
    participant OL as OneLake
    participant DT as Delta Table

    Note over TD,DT: Initial Load

    ADF->>TD: Query: SELECT * WHERE date >= '2020-01-01'
    TD-->>ADF: Full dataset (millions of rows)
    ADF->>OL: Write Parquet files
    OL->>DT: COPY INTO bronze.table

    Note over TD,DT: Incremental Load (Daily)

    ADF->>DT: Get MAX(watermark_column)
    DT-->>ADF: Last watermark: 2024-01-15 23:59:59

    ADF->>TD: Query: SELECT * WHERE timestamp > watermark
    TD-->>ADF: New/changed rows only
    ADF->>OL: Write Parquet files
    OL->>DT: COPY INTO (APPEND mode)

    ADF->>DT: OPTIMIZE table
```

---

## 5. Validation Workflow

```mermaid
flowchart TB
    subgraph Source["Source Validation"]
        S_COUNT[Row Count]
        S_SUM[Column Sums]
        S_SAMPLE[Sample Rows]
    end

    subgraph Target["Target Validation"]
        T_COUNT[Row Count]
        T_SUM[Column Sums]
        T_SAMPLE[Sample Rows]
    end

    subgraph Compare["Comparison"]
        CMP_COUNT{Counts<br/>Match?}
        CMP_SUM{Sums<br/>Match?}
        CMP_SAMPLE{Samples<br/>Match?}
    end

    subgraph Result["Result"]
        PASS([✅ PASS])
        FAIL([❌ FAIL])
        INVESTIGATE[Investigate<br/>Differences]
    end

    S_COUNT --> CMP_COUNT
    T_COUNT --> CMP_COUNT
    S_SUM --> CMP_SUM
    T_SUM --> CMP_SUM
    S_SAMPLE --> CMP_SAMPLE
    T_SAMPLE --> CMP_SAMPLE

    CMP_COUNT -->|Yes| CMP_SUM
    CMP_COUNT -->|No| INVESTIGATE
    CMP_SUM -->|Yes| CMP_SAMPLE
    CMP_SUM -->|No| INVESTIGATE
    CMP_SAMPLE -->|Yes| PASS
    CMP_SAMPLE -->|No| INVESTIGATE
    INVESTIGATE --> FAIL

    style PASS fill:#27ae60,color:#fff
    style FAIL fill:#e74c3c,color:#fff
```

---

## 6. BTEQ to Notebook Conversion

```mermaid
flowchart LR
    subgraph BTEQ["BTEQ Script"]
        LOGON[.LOGON]
        SET[.SET variables]
        SQL1[SQL Queries]
        EXPORT[.EXPORT]
        LOGOFF[.LOGOFF]
    end

    subgraph Notebook["Fabric Notebook"]
        CONNECT[JDBC/Linked Service]
        PARAMS[Notebook Parameters]
        SPARK[Spark SQL]
        WRITE[df.write.csv/parquet]
        CLEANUP[Cleanup]
    end

    LOGON -->|Convert| CONNECT
    SET -->|Convert| PARAMS
    SQL1 -->|Convert| SPARK
    EXPORT -->|Convert| WRITE
    LOGOFF -->|Convert| CLEANUP

    style BTEQ fill:#e74c3c,color:#fff
    style Notebook fill:#27ae60,color:#fff
```

---

## 7. Third-Party Tool Integration

```mermaid
flowchart TB
    subgraph Tools["Migration Tools"]
        DATOMETRY[Datometry<br/>Query Translation]
        RAVEN[Raven<br/>Code Conversion]
        X2X[X2X Suite<br/>ETL Migration]
        QLIK[Qlik Replicate<br/>CDC Streaming]
    end

    subgraph Teradata["Teradata"]
        TD_SQL[SQL Queries]
        TD_ETL[ETL Jobs]
        TD_CDC[Change Data]
    end

    subgraph Fabric["Microsoft Fabric"]
        F_WH[Warehouse]
        F_PIPE[Pipelines]
        F_LH[Lakehouse]
    end

    TD_SQL -->|Real-time translate| DATOMETRY --> F_WH
    TD_ETL -->|Convert| RAVEN --> F_PIPE
    TD_ETL -->|Convert| X2X --> F_PIPE
    TD_CDC -->|Stream| QLIK --> F_LH

    style Tools fill:#9b59b6,color:#fff
```

---

## 8. Migration Timeline

```mermaid
gantt
    title Teradata to Fabric Migration Timeline
    dateFormat  YYYY-MM-DD
    section Assessment
    Environment Analysis     :a1, 2024-01-01, 1w
    Complexity Scoring       :a2, after a1, 1w
    Migration Planning       :a3, after a2, 1w

    section Foundation
    Fabric Setup             :b1, after a3, 1w
    Connectivity Config      :b2, after b1, 3d
    Pipeline Development     :b3, after b2, 1w

    section Pilot
    Migrate 5 Tables         :c1, after b3, 1w
    Validate & Test          :c2, after c1, 1w
    Lessons Learned          :c3, after c2, 2d

    section Core Migration
    Dimension Tables         :d1, after c3, 2w
    Fact Tables              :d2, after d1, 2w
    BTEQ Conversion          :d3, after d1, 2w
    Incremental Setup        :d4, after d2, 1w

    section Cutover
    Full Validation          :e1, after d4, 1w
    Performance Testing      :e2, after e1, 1w
    User Acceptance          :e3, after e2, 1w
    Go-Live                  :milestone, e4, after e3, 0d
```

---

## 9. Hybrid Architecture (Phased Migration)

```mermaid
flowchart TB
    subgraph Phase1["Phase 1: Parallel Run"]
        TD1[(Teradata<br/>Primary)]
        FB1[(Fabric<br/>Read-Only)]
        SYNC1[Daily Sync]

        TD1 --> SYNC1 --> FB1
    end

    subgraph Phase2["Phase 2: Fabric Primary"]
        TD2[(Teradata<br/>Archive)]
        FB2[(Fabric<br/>Primary)]
        SYNC2[On-Demand<br/>Historical]

        FB2 --> SYNC2 --> TD2
    end

    subgraph Phase3["Phase 3: Decommission"]
        TD3[(Teradata<br/>Decommissioned)]
        FB3[(Fabric<br/>Complete)]

        TD3 -.->|Archive| FB3
    end

    Phase1 --> Phase2 --> Phase3

    style Phase1 fill:#f39c12,color:#fff
    style Phase2 fill:#3498db,color:#fff
    style Phase3 fill:#27ae60,color:#fff
```

---

## 10. Cost Comparison Model

```mermaid
pie showData
    title Teradata vs Fabric Cost Distribution
    "Compute (Fabric CUs)" : 35
    "Storage (OneLake)" : 15
    "Data Transfer" : 10
    "Migration Tools" : 15
    "Professional Services" : 25
```

---

## Quick Reference Diagrams

### Function Mapping

```
┌─────────────────────────────────────────────────────────────┐
│              Teradata → Fabric Function Map                 │
├───────────────────────┬─────────────────────────────────────┤
│     TERADATA          │           FABRIC T-SQL              │
├───────────────────────┼─────────────────────────────────────┤
│ NVL(a, b)             │ COALESCE(a, b)                      │
│ NULLIFZERO(x)         │ NULLIF(x, 0)                        │
│ ZEROIFNULL(x)         │ ISNULL(x, 0)                        │
│ ADD_MONTHS(d, n)      │ DATEADD(MONTH, n, d)                │
│ CURRENT_DATE          │ CAST(GETDATE() AS DATE)             │
│ INDEX(s, p)           │ CHARINDEX(p, s)                     │
│ OREPLACE(s, o, n)     │ REPLACE(s, o, n)                    │
│ QUALIFY ROW_NUMBER()  │ CTE + WHERE rn = 1                  │
│ SAMPLE 0.01           │ TABLESAMPLE (1 PERCENT)             │
│ TOP N WITH TIES       │ RANK() <= N                         │
└───────────────────────┴─────────────────────────────────────┘
```
