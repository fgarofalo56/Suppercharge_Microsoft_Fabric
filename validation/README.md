# Validation & Testing Framework

This directory contains data quality validation and testing resources for the Microsoft Fabric Casino POC.

## Directory Structure

```
validation/
├── great_expectations/      # Data quality expectations
│   ├── expectations/        # Expectation suites
│   ├── checkpoints/         # Validation checkpoints
│   └── great_expectations.yml
├── unit_tests/              # Unit tests for generators
│   ├── test_generators.py
│   └── conftest.py
├── integration_tests/       # End-to-end tests
│   └── test_pipeline.py
└── README.md
```

## Great Expectations

Data quality validation using Great Expectations framework.

### Setup

```bash
pip install great_expectations

# Initialize project (already done)
cd validation/great_expectations
great_expectations init
```

### Running Validations

```bash
# Validate Bronze layer
great_expectations checkpoint run bronze_checkpoint

# Validate Silver layer
great_expectations checkpoint run silver_checkpoint

# Validate Gold layer
great_expectations checkpoint run gold_checkpoint
```

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

- **Generator Tests**: Validate synthetic data generation
- **Schema Tests**: Verify output schemas match expectations
- **Business Logic Tests**: Test compliance calculations (CTR, SAR)

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

1. **Full Pipeline Test**: Bronze → Silver → Gold flow
2. **Data Quality Test**: Verify quality metrics through layers
3. **Compliance Test**: Validate regulatory data handling

## Validation Checkpoints

### Bronze Layer

| Check | Table | Expectation |
|-------|-------|-------------|
| Not Null | bronze_slot_telemetry | machine_id, event_timestamp |
| Value Range | bronze_slot_telemetry | coin_in >= 0 |
| Row Count | bronze_slot_telemetry | count > 0 |
| Schema | All Bronze | Match expected columns |

### Silver Layer

| Check | Table | Expectation |
|-------|-------|-------------|
| Data Quality Score | silver_slot_cleansed | avg(_dq_score) > 80 |
| Uniqueness | silver_player_master | player_id unique (current records) |
| Completeness | silver_financial_reconciled | reconciliation_status not null |
| Valid Values | silver_slot_cleansed | event_type in valid list |

### Gold Layer

| Check | Table | Expectation |
|-------|-------|-------------|
| KPI Accuracy | gold_slot_performance | hold_pct between 0 and 100 |
| Player Count | gold_player_360 | matches Silver current records |
| Aggregation | gold_compliance_reporting | sum matches Silver details |
| No Duplicates | All Gold | business keys unique |

## CI/CD Integration

The validation tests run automatically in GitHub Actions:

```yaml
# .github/workflows/run-tests.yml
- name: Run Unit Tests
  run: pytest validation/unit_tests/ -v

- name: Run Data Quality Checks
  run: great_expectations checkpoint run all_checkpoints
```

## Writing New Validations

### Great Expectations

1. Create expectation suite in `expectations/`
2. Add checkpoint in `checkpoints/`
3. Document expectations in this README

### Unit Tests

1. Add test file in `unit_tests/`
2. Use pytest fixtures from `conftest.py`
3. Follow naming convention: `test_*.py`

### Integration Tests

1. Add test file in `integration_tests/`
2. Mark slow tests with `@pytest.mark.slow`
3. Use test data fixtures
