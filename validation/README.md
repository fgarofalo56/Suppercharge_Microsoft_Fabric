# :white_check_mark: Validation & Testing Framework

> **[Home](../README.md)** | **[Data Generation](../data-generation/)** | **[Notebooks](../notebooks/)** | **[Tutorials](../tutorials/)**

Comprehensive data quality validation and testing resources for the Microsoft Fabric Casino POC.

---

## Test Coverage Summary

| Test Type | Framework | Coverage | Status |
|-----------|-----------|----------|--------|
| Unit Tests | pytest | Generators, Utilities | Active |
| Integration Tests | pytest | Pipeline End-to-End | Active |
| Data Quality | Great Expectations | Bronze/Silver/Gold | Active |
| Schema Validation | Delta Lake | All Layers | Active |

---

## Testing Flow

```
+-------------+     +------------------+     +-------------------+
|   UNIT      |     |   INTEGRATION    |     |    DEPLOYMENT     |
|   TESTS     | --> |     TESTS        | --> |    VALIDATION     |
+-------------+     +------------------+     +-------------------+
|             |     |                  |     |                   |
| Generators  |     | Pipeline E2E     |     | Great Expectations|
| Utilities   |     | Data Flow        |     | Checkpoints       |
| Business    |     | Layer Integrity  |     | Production DQ     |
| Logic       |     |                  |     |                   |
+-------------+     +------------------+     +-------------------+
      |                    |                        |
      v                    v                        v
   pytest              pytest                  GE Framework
   --cov               --slow                  Checkpoints
```

---

## Directory Structure

```
validation/
|-- great_expectations/           # Data quality validation framework
|   |-- great_expectations.yml    # Main GX configuration
|   |-- validate_data.py          # Python validation utilities
|   |-- README.md                 # Detailed GX documentation
|   |-- expectations/             # Expectation suite definitions
|   |   |-- slot_machine_suite.json
|   |   |-- player_suite.json
|   |   |-- compliance_suite.json
|   |   |-- compliance_ctr_conditional_suite.json
|   |   |-- compliance_w2g_conditional_suite.json
|   |   |-- compliance_sar_conditional_suite.json
|   |   |-- financial_suite.json
|   |   |-- security_suite.json
|   |   |-- table_games_suite.json
|   |   |-- bronze_slot_telemetry_suite.json
|   |   |-- silver_slot_cleansed_suite.json
|   |   +-- gold_slot_performance_suite.json
|   +-- checkpoints/              # Validation checkpoints
|       |-- slot_machine_checkpoint.yml
|       |-- player_checkpoint.yml
|       |-- compliance_checkpoint.yml
|       |-- financial_checkpoint.yml
|       |-- security_checkpoint.yml
|       |-- table_games_checkpoint.yml
|       +-- all_domains_checkpoint.yml
|-- unit_tests/                   # Unit tests for generators
|   |-- conftest.py
|   +-- test_generators.py
|-- integration_tests/            # End-to-end tests
|   +-- test_pipeline.py
|-- deployment_tests/             # Infrastructure tests
|   +-- test_bicep_deployment.py
+-- README.md
```

---

## Quick Start

### Option 1: Docker (Recommended)

Run validation without installing dependencies locally.

```bash
# Validate generated data using Docker
docker-compose run --rm data-validator

# Run validation on specific output directory
docker-compose run --rm data-validator --input /app/output/custom

# Generate validation report
docker-compose run --rm data-validator --output-report ./validation-report.html
```

### Option 2: Local Python

```bash
# Run all unit tests
pytest validation/unit_tests/ -v

# Run integration tests (includes slow tests)
pytest validation/integration_tests/ -v --slow

# Run with coverage report
pytest validation/unit_tests/ --cov=data-generation/generators --cov-report=html

# Run Great Expectations checkpoints
great_expectations checkpoint run all_checkpoints
```

### Option 3: Script-Based

```powershell
# Run all validations
./scripts/validate.ps1

# Run specific suite
./scripts/validate.ps1 -Suite "slot_machine"

# Generate HTML report
./scripts/validate.ps1 -OutputReport ./validation-report.html
```

---

## Great Expectations

Data quality validation using the Great Expectations framework.

### Setup

```bash
pip install great_expectations

# Initialize project (already done)
cd validation/great_expectations
great_expectations init
```

### Running Validations

```bash
# Run all domain validations at once
great_expectations checkpoint run all_domains_checkpoint

# Or run individual domain checkpoints
great_expectations checkpoint run slot_machine_checkpoint
great_expectations checkpoint run player_checkpoint
great_expectations checkpoint run compliance_checkpoint
great_expectations checkpoint run financial_checkpoint
great_expectations checkpoint run security_checkpoint
great_expectations checkpoint run table_games_checkpoint
```

### Domain-Specific Validation Suites

| Domain | Suite | Key Validations |
|--------|-------|-----------------|
| Slot Machine | `slot_machine_suite` | machine_id format (SLOT-XXXX), event_type, coin_in >= 0, denomination |
| Player | `player_suite` | player_id format (P+digits), loyalty_tier, ssn_hash length (64), email format |
| Compliance | `compliance_suite` | filing_type (CTR/SAR/W2G), CTR amount >= $10K, W2G >= $600 |
| Financial | `financial_suite` | transaction_id format, amount > 0, ctr_required flag |
| Security | `security_suite` | event_type, severity_level (LOW/MEDIUM/HIGH/CRITICAL) |
| Table Games | `table_games_suite` | table_id format (TBL-XX-XXX), game_type, bet_amount > 0 |

### Creating New Expectations

```python
import great_expectations as gx

context = gx.get_context()

# Create expectation suite
suite = context.add_expectation_suite("new_suite")

# Add expectations
suite.add_expectation(
    expectation_type="expect_column_values_to_not_be_null",
    kwargs={"column": "player_id"}
)
```

### Compliance Thresholds Reference

| Filing Type | Amount Threshold | Regulation |
|-------------|------------------|------------|
| CTR (Currency Transaction Report) | >= $10,000 | Bank Secrecy Act |
| SAR (Suspicious Activity Report) | Variable | Bank Secrecy Act |
| W-2G General | >= $600 | IRS |
| W-2G Slots | >= $1,200 | IRS |
| W-2G Bingo/Keno | >= $1,500 | IRS |
| W-2G Poker Tournament | >= $5,000 | IRS |

---

## Unit Tests

Testing data generators and utility functions.

### Running Tests

```bash
# Run all unit tests
pytest validation/unit_tests/ -v

# Run specific test file
pytest validation/unit_tests/test_generators.py -v

# Run with coverage
pytest validation/unit_tests/ --cov=data-generation/generators --cov-report=html
```

### Test Categories

| Category | Description | Files |
|----------|-------------|-------|
| Generator Tests | Validate synthetic data generation | `test_generators.py` |
| Schema Tests | Verify output schemas match expectations | `test_schemas.py` |
| Business Logic Tests | Test compliance calculations (CTR, SAR) | `test_compliance.py` |
| Utility Tests | Test helper functions | `test_utils.py` |

---

## Integration Tests

End-to-end pipeline validation.

### Running Tests

```bash
# Run integration tests
pytest validation/integration_tests/ -v --slow

# Skip slow tests
pytest validation/integration_tests/ -v --skip-slow
```

### Test Scenarios

| Scenario | Description | Duration |
|----------|-------------|----------|
| Full Pipeline Test | Bronze -> Silver -> Gold flow | ~5 min |
| Data Quality Test | Verify quality metrics through layers | ~3 min |
| Compliance Test | Validate regulatory data handling | ~2 min |
| Volume Test | Large dataset processing | ~10 min |

---

## Validation Checkpoints

### Bronze Layer

| Check | Table | Expectation | Severity |
|-------|-------|-------------|----------|
| Not Null | `bronze_slot_telemetry` | `machine_id`, `event_timestamp` not null | Critical |
| Value Range | `bronze_slot_telemetry` | `coin_in >= 0` | Critical |
| Row Count | `bronze_slot_telemetry` | `count > 0` | Warning |
| Schema | All Bronze | Match expected columns | Critical |
| Freshness | All Bronze | Data within 24 hours | Warning |

### Silver Layer

| Check | Table | Expectation | Severity |
|-------|-------|-------------|----------|
| Data Quality Score | `silver_slot_cleansed` | `avg(_dq_score) > 80` | Critical |
| Uniqueness | `silver_player_master` | `player_id` unique (current) | Critical |
| Completeness | `silver_financial_reconciled` | `reconciliation_status` not null | Warning |
| Valid Values | `silver_slot_cleansed` | `event_type` in valid list | Critical |
| Referential | `silver_table_enriched` | `player_id` exists in player master | Warning |

### Gold Layer

| Check | Table | Expectation | Severity |
|-------|-------|-------------|----------|
| KPI Accuracy | `gold_slot_performance` | `hold_pct` between 0 and 100 | Critical |
| Player Count | `gold_player_360` | Matches Silver current records | Critical |
| Aggregation | `gold_compliance_reporting` | Sum matches Silver details | Critical |
| No Duplicates | All Gold | Business keys unique | Critical |
| Timeliness | All Gold | Refresh within SLA | Warning |

---

## CI/CD Integration

### GitHub Actions Workflows

The validation tests run automatically in GitHub Actions with multiple strategies.

#### Standard Python Workflow

```yaml
# .github/workflows/run-tests.yml
name: Validation Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run Unit Tests
        run: pytest validation/unit_tests/ -v --cov

      - name: Run Data Quality Checks
        run: great_expectations checkpoint run all_checkpoints
```

#### Docker-Based Workflow

```yaml
# .github/workflows/docker-validation.yml
name: Docker Validation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  docker-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker images
        run: docker-compose build

      - name: Generate test data
        run: docker-compose run --rm demo-generator

      - name: Run validation
        run: docker-compose run --rm data-validator

      - name: Upload validation report
        uses: actions/upload-artifact@v4
        with:
          name: validation-report
          path: ./validation-report.html
```

### Integration with Deployment Scripts

The validation can be integrated into deployment workflows:

```powershell
# In scripts/deploy.ps1
# Run validation before deployment
./scripts/validate.ps1 -Suite "all"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Validation failed. Deployment aborted."
    exit 1
}

# Proceed with deployment
az deployment sub create ...
```

### Running Tests in Dev Container

Tests run seamlessly in the Dev Container environment:

```bash
# In Dev Container terminal
pytest validation/unit_tests/ -v
great_expectations checkpoint run all_checkpoints
```

All dependencies are pre-installed in the container.

---

## Writing New Validations

### Great Expectations

1. Create expectation suite in `expectations/`
2. Add checkpoint in `checkpoints/`
3. Document expectations in this README

```python
# Example: Create new expectation suite
import great_expectations as gx

context = gx.get_context()
suite = context.add_expectation_suite("my_new_suite")

# Add expectations
suite.add_expectation(
    expectation_type="expect_column_values_to_be_between",
    kwargs={"column": "amount", "min_value": 0, "max_value": 1000000}
)

# Save
context.save_expectation_suite(suite)
```

### Unit Tests

1. Add test file in `unit_tests/`
2. Use pytest fixtures from `conftest.py`
3. Follow naming convention: `test_*.py`

```python
# Example: unit_tests/test_new_feature.py
import pytest
from generators import MyNewGenerator

class TestMyNewGenerator:
    @pytest.fixture
    def generator(self):
        return MyNewGenerator(seed=42)

    def test_generates_valid_data(self, generator):
        df = generator.generate(100)
        assert len(df) == 100
        assert "required_column" in df.columns

    def test_respects_constraints(self, generator):
        df = generator.generate(100)
        assert df["amount"].min() >= 0
```

### Integration Tests

1. Add test file in `integration_tests/`
2. Mark slow tests with `@pytest.mark.slow`
3. Use test data fixtures

```python
# Example: integration_tests/test_new_pipeline.py
import pytest

@pytest.mark.slow
class TestNewPipeline:
    def test_end_to_end_flow(self, bronze_data, spark_session):
        # Bronze -> Silver
        silver_df = transform_to_silver(bronze_data)
        assert silver_df.count() > 0

        # Silver -> Gold
        gold_df = aggregate_to_gold(silver_df)
        assert "kpi_metric" in gold_df.columns
```

---

## Test Data Fixtures

Common fixtures available in `conftest.py`:

| Fixture | Description | Scope |
|---------|-------------|-------|
| `sample_slot_data` | 100 slot machine events | Function |
| `sample_player_data` | 50 player profiles | Function |
| `sample_financial_data` | 200 transactions | Function |
| `spark_session` | Local Spark session | Session |
| `temp_lakehouse` | Temporary test Lakehouse | Function |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests timeout | Increase `--timeout` or mark as `@pytest.mark.slow` |
| Coverage low | Add tests for uncovered branches |
| GE checkpoint fails | Check data source connection settings |
| Import errors | Ensure `PYTHONPATH` includes project root |
| Spark not found | Install PySpark: `pip install pyspark` |

---

## Related Resources

| Resource | Description |
|----------|-------------|
| [Data Generation](../data-generation/README.md) | Generate test data |
| [Notebooks](../notebooks/README.md) | Fabric notebooks to test |
| [CI/CD Workflows](../.github/workflows/) | Automated testing pipelines |

---

<div align="center">

**[Back to Top](#white_check_mark-validation--testing-framework)** | **[Main README](../README.md)**

</div>
