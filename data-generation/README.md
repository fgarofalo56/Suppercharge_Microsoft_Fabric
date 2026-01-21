# Data Generation

This directory contains Python generators for creating synthetic casino/gaming data for the Microsoft Fabric POC.

## Quick Start

```bash
# Install dependencies
pip install -r ../requirements.txt

# Generate all data with default volumes
python generate.py --all --days 30

# Generate specific data types
python generate.py --slots 100000 --players 5000

# Output to different format
python generate.py --all --format csv --output ./csv_output
```

## Data Generators

| Generator | Output File | Description |
|-----------|-------------|-------------|
| `SlotMachineGenerator` | `bronze_slot_telemetry` | Slot machine events, meters, jackpots |
| `TableGameGenerator` | `bronze_table_games` | Table game transactions, ratings |
| `PlayerGenerator` | `bronze_player_profile` | Player demographics, loyalty |
| `FinancialGenerator` | `bronze_financial_txn` | Cage transactions, markers |
| `SecurityGenerator` | `bronze_security_events` | Access control, surveillance |
| `ComplianceGenerator` | `bronze_compliance` | CTR, SAR, W-2G filings |

## Default Volumes

When using `--all`, the following volumes are generated:

| Data Type | Records | Est. Size |
|-----------|---------|-----------|
| Slot Events | 500,000 | ~500 MB |
| Table Games | 100,000 | ~100 MB |
| Players | 10,000 | ~10 MB |
| Financial | 50,000 | ~50 MB |
| Security | 25,000 | ~25 MB |
| Compliance | 10,000 | ~10 MB |
| **Total** | **~700,000** | **~700 MB** |

## Command Line Options

```
usage: generate.py [-h] [--output OUTPUT] [--format {parquet,json,csv}]
                   [--days DAYS] [--seed SEED] [--all]
                   [--slots SLOTS] [--tables TABLES] [--players PLAYERS]
                   [--financial FINANCIAL] [--security SECURITY]
                   [--compliance COMPLIANCE] [--include-pii]

Options:
  --output, -o     Output directory (default: ./output)
  --format, -f     Output format: parquet, json, csv (default: parquet)
  --days, -d       Days of historical data (default: 30)
  --seed, -s       Random seed for reproducibility (default: 42)
  --all, -a        Generate all data types
  --slots          Number of slot machine events
  --tables         Number of table game events
  --players        Number of player profiles
  --financial      Number of financial transactions
  --security       Number of security events
  --compliance     Number of compliance records
  --include-pii    Include raw PII (testing only)
```

## Using Generators Programmatically

```python
from generators import SlotMachineGenerator, PlayerGenerator
from datetime import datetime, timedelta

# Configure date range
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Generate slot machine data
slot_gen = SlotMachineGenerator(
    num_machines=500,
    seed=42,
    start_date=start_date,
    end_date=end_date,
)

# Generate 10,000 events
df = slot_gen.generate(10000)

# Save to parquet
slot_gen.to_parquet(df, "output/slot_events.parquet")

# Generate in batches (memory efficient)
for batch in slot_gen.generate_batches(100000, batch_size=10000):
    process_batch(batch)
```

## Data Quality

All generators include:
- Consistent schema definitions
- Referential integrity (player IDs, machine IDs)
- Realistic distributions and patterns
- Compliance threshold logic (CTR $10K, W-2G $1,200)
- PII handling (hashing, masking)

## PII Handling

By default, PII is protected:
- SSN: Hashed + masked (XXX-XX-1234)
- Names: First initial only (J*** S***)
- Addresses: Hashed
- Card numbers: Masked (****-****-****-1234)

Use `--include-pii` only for testing/development.

## Compliance Data

The compliance generator includes realistic patterns for:

### CTR (Currency Transaction Reports)
- Threshold: >= $10,000
- Filed within 15 days
- Includes cash-in/cash-out breakdown

### SAR (Suspicious Activity Reports)
- Pattern detection (structuring)
- Multiple categories
- Narrative generation
- Filed within 30 days

### W-2G (Gambling Winnings)
- Slots: >= $1,200
- Keno: >= $1,500
- Poker tournaments: >= $5,000
- Includes withholding calculations

## Output Schemas

### Slot Machine Events
```
event_id, machine_id, asset_number, location_id, zone,
event_type, event_timestamp, denomination, coin_in, coin_out,
jackpot_amount, games_played, theoretical_hold, actual_hold,
player_id, session_id, machine_type, manufacturer, game_theme,
error_code, error_message, _ingested_at, _source, _batch_id
```

### Player Profiles
```
player_id, loyalty_number, first_name, last_name, email,
phone, date_of_birth, ssn_hash, ssn_masked, address_line1,
city, state, zip_code, country, loyalty_tier, points_balance,
lifetime_points, tier_credits, enrollment_date, last_visit_date,
total_visits, total_theo, total_actual_win_loss, average_daily_theo,
preferred_game, communication_preference, marketing_opt_in,
marketing_channel, host_assigned, vip_flag, self_excluded,
account_status, _ingested_at, _source, _batch_id
```

See individual generator docstrings for complete schemas.
