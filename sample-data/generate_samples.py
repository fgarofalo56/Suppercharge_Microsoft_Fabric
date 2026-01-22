#!/usr/bin/env python3
"""
Sample Data Generator
=====================

Generates pre-built sample datasets for the Microsoft Fabric Casino/Gaming POC.
Uses the existing data generators with fixed seeds for reproducibility.

Usage:
    python generate_samples.py                    # Generate all samples with defaults
    python generate_samples.py --seed 42          # Custom seed
    python generate_samples.py --slots 1000       # Custom record counts
    python generate_samples.py --format csv       # Output format (csv, parquet, both)
    python generate_samples.py --output ./data    # Custom output directory
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd

from data_generation.generators.slot_machine_generator import SlotMachineGenerator
from data_generation.generators.player_generator import PlayerGenerator
from data_generation.generators.table_games_generator import TableGamesGenerator
from data_generation.generators.financial_generator import FinancialGenerator
from data_generation.generators.security_generator import SecurityGenerator
from data_generation.generators.compliance_generator import ComplianceGenerator


# Default sample sizes matching the README specification
DEFAULT_COUNTS = {
    "slot_telemetry": 500,
    "player_profile": 100,
    "table_games": 200,
    "financial_transactions": 200,
    "security_events": 150,
    "compliance_filings": 50,
}

# Fixed date range for reproducible samples (30-day window)
DEFAULT_START_DATE = datetime(2024, 1, 1, 0, 0, 0)
DEFAULT_END_DATE = datetime(2024, 1, 31, 23, 59, 59)


def generate_slot_telemetry(
    count: int,
    seed: int,
    start_date: datetime,
    end_date: datetime,
) -> pd.DataFrame:
    """Generate slot machine telemetry sample data."""
    print(f"\nGenerating {count} slot telemetry records...")

    generator = SlotMachineGenerator(
        num_machines=50,  # Smaller machine pool for samples
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    df = generator.generate(count, show_progress=True)

    # Ensure some jackpot events are included for demo purposes
    jackpot_count = len(df[df["event_type"] == "JACKPOT"])
    if jackpot_count < 5:
        print(f"  Adding guaranteed jackpot events for demo...")
        # Manually ensure at least 5 jackpots exist
        jackpot_indices = df.sample(min(5, len(df))).index
        for idx in jackpot_indices[:5]:
            df.loc[idx, "event_type"] = "JACKPOT"
            df.loc[idx, "jackpot_amount"] = float(generator.faker.random_int(1200, 50000))
            df.loc[idx, "coin_out"] = df.loc[idx, "jackpot_amount"]

    print(f"  Generated {len(df)} records with {len(df[df['event_type'] == 'JACKPOT'])} jackpots")
    return df


def generate_player_profiles(
    count: int,
    seed: int,
    start_date: datetime,
    end_date: datetime,
) -> pd.DataFrame:
    """Generate player profile sample data."""
    print(f"\nGenerating {count} player profile records...")

    generator = PlayerGenerator(
        seed=seed,
        include_pii=False,  # Masked PII for samples
        start_date=start_date,
        end_date=end_date,
    )

    df = generator.generate(count, show_progress=True)

    # Ensure tier distribution is representative
    tier_counts = df["loyalty_tier"].value_counts()
    print(f"  Tier distribution: {tier_counts.to_dict()}")

    return df


def generate_table_games(
    count: int,
    seed: int,
    start_date: datetime,
    end_date: datetime,
) -> pd.DataFrame:
    """Generate table games event sample data."""
    print(f"\nGenerating {count} table game records...")

    generator = TableGamesGenerator(
        num_tables=25,  # Smaller table pool for samples
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    df = generator.generate(count, show_progress=True)

    # Report game type distribution
    game_counts = df["game_type"].value_counts()
    print(f"  Game distribution: {game_counts.to_dict()}")

    return df


def generate_financial_transactions(
    count: int,
    seed: int,
    start_date: datetime,
    end_date: datetime,
) -> pd.DataFrame:
    """Generate financial transaction sample data."""
    print(f"\nGenerating {count} financial transaction records...")

    generator = FinancialGenerator(
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    df = generator.generate(count, show_progress=True)

    # Ensure CTR threshold transactions exist for demo
    ctr_count = len(df[df["ctr_required"] == True])
    if ctr_count < 10:
        print(f"  Adjusting to ensure CTR threshold transactions...")
        # Set some amounts to trigger CTR
        high_value_indices = df.sample(min(10, len(df))).index
        for idx in high_value_indices[:10]:
            df.loc[idx, "amount"] = float(generator.faker.random_int(10000, 50000))
            df.loc[idx, "ctr_required"] = True

    ctr_count = len(df[df["ctr_required"] == True])
    suspicious_count = len(df[df["suspicious_activity_flag"] == True])
    print(f"  CTR required: {ctr_count}, Suspicious flagged: {suspicious_count}")

    return df


def generate_security_events(
    count: int,
    seed: int,
    start_date: datetime,
    end_date: datetime,
) -> pd.DataFrame:
    """Generate security event sample data."""
    print(f"\nGenerating {count} security event records...")

    generator = SecurityGenerator(
        num_employees=100,  # Smaller employee pool for samples
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    df = generator.generate(count, show_progress=True)

    # Report event type distribution
    event_counts = df["event_type"].value_counts().head(5)
    print(f"  Top event types: {event_counts.to_dict()}")

    return df


def generate_compliance_filings(
    count: int,
    seed: int,
    start_date: datetime,
    end_date: datetime,
) -> pd.DataFrame:
    """Generate compliance filing sample data."""
    print(f"\nGenerating {count} compliance filing records...")

    generator = ComplianceGenerator(
        seed=seed,
        start_date=start_date,
        end_date=end_date,
    )

    df = generator.generate(count, show_progress=True)

    # Report filing type distribution
    filing_counts = df["filing_type"].value_counts()
    print(f"  Filing distribution: {filing_counts.to_dict()}")

    return df


def ensure_referential_integrity(
    slot_df: pd.DataFrame,
    player_df: pd.DataFrame,
    table_df: pd.DataFrame,
    financial_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Ensure player IDs are consistent across datasets for joinability.

    Updates player_id fields in slot, table, and financial data to reference
    actual player IDs from the player profile dataset.
    """
    print("\nEnsuring referential integrity across datasets...")

    # Get valid player IDs
    valid_player_ids = player_df["player_id"].tolist()

    # Update slot telemetry player references
    if "player_id" in slot_df.columns:
        mask = slot_df["player_id"].notna()
        slot_df.loc[mask, "player_id"] = slot_df.loc[mask, "player_id"].apply(
            lambda x: valid_player_ids[hash(str(x)) % len(valid_player_ids)]
        )

    # Update table games player references
    if "player_id" in table_df.columns:
        mask = table_df["player_id"].notna()
        table_df.loc[mask, "player_id"] = table_df.loc[mask, "player_id"].apply(
            lambda x: valid_player_ids[hash(str(x)) % len(valid_player_ids)]
        )

    # Update financial transaction player references
    if "player_id" in financial_df.columns:
        mask = financial_df["player_id"].notna()
        financial_df.loc[mask, "player_id"] = financial_df.loc[mask, "player_id"].apply(
            lambda x: valid_player_ids[hash(str(x)) % len(valid_player_ids)]
        )

    print(f"  Updated player references to use {len(valid_player_ids)} valid player IDs")

    return slot_df, player_df, table_df, financial_df


def save_dataframe(
    df: pd.DataFrame,
    name: str,
    output_dir: Path,
    formats: list[str],
) -> None:
    """Save DataFrame in specified formats."""
    # Convert datetime columns to ISO format strings for CSV compatibility
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%dT%H:%M:%S")
        elif df[col].dtype == object:
            # Check if it's a datetime object
            sample = df[col].dropna().head(1)
            if len(sample) > 0 and isinstance(sample.iloc[0], datetime):
                df[col] = df[col].apply(
                    lambda x: x.strftime("%Y-%m-%dT%H:%M:%S") if pd.notna(x) else None
                )

    if "csv" in formats or "both" in formats:
        csv_path = output_dir / "bronze" / f"{name}_sample.csv"
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False)
        print(f"  Saved: {csv_path}")

    if "parquet" in formats or "both" in formats:
        parquet_path = output_dir / "bronze" / f"{name}_sample.parquet"
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(parquet_path, index=False, engine="pyarrow")
        print(f"  Saved: {parquet_path}")


def main():
    """Main entry point for sample data generation."""
    parser = argparse.ArgumentParser(
        description="Generate sample data for Microsoft Fabric Casino POC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python generate_samples.py
    python generate_samples.py --seed 123 --format both
    python generate_samples.py --slots 1000 --players 200
    python generate_samples.py --output ./my-data --format parquet
        """,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "parquet", "both"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory (default: same as script)",
    )
    parser.add_argument(
        "--slots",
        type=int,
        default=DEFAULT_COUNTS["slot_telemetry"],
        help=f"Number of slot telemetry records (default: {DEFAULT_COUNTS['slot_telemetry']})",
    )
    parser.add_argument(
        "--players",
        type=int,
        default=DEFAULT_COUNTS["player_profile"],
        help=f"Number of player profile records (default: {DEFAULT_COUNTS['player_profile']})",
    )
    parser.add_argument(
        "--tables",
        type=int,
        default=DEFAULT_COUNTS["table_games"],
        help=f"Number of table game records (default: {DEFAULT_COUNTS['table_games']})",
    )
    parser.add_argument(
        "--financial",
        type=int,
        default=DEFAULT_COUNTS["financial_transactions"],
        help=f"Number of financial records (default: {DEFAULT_COUNTS['financial_transactions']})",
    )
    parser.add_argument(
        "--security",
        type=int,
        default=DEFAULT_COUNTS["security_events"],
        help=f"Number of security event records (default: {DEFAULT_COUNTS['security_events']})",
    )
    parser.add_argument(
        "--compliance",
        type=int,
        default=DEFAULT_COUNTS["compliance_filings"],
        help=f"Number of compliance records (default: {DEFAULT_COUNTS['compliance_filings']})",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="2024-01-01",
        help="Start date for data range (YYYY-MM-DD, default: 2024-01-01)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default="2024-01-31",
        help="End date for data range (YYYY-MM-DD, default: 2024-01-31)",
    )

    args = parser.parse_args()

    # Parse dates
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d").replace(
        hour=23, minute=59, second=59
    )

    # Set output directory
    output_dir = Path(args.output) if args.output else Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    formats = [args.format] if args.format != "both" else ["csv", "parquet"]

    print("=" * 60)
    print("Microsoft Fabric Casino POC - Sample Data Generator")
    print("=" * 60)
    print(f"Seed: {args.seed}")
    print(f"Date Range: {start_date.date()} to {end_date.date()}")
    print(f"Output Format: {args.format}")
    print(f"Output Directory: {output_dir}")
    print("=" * 60)

    # Generate all datasets
    slot_df = generate_slot_telemetry(
        args.slots, args.seed, start_date, end_date
    )

    player_df = generate_player_profiles(
        args.players, args.seed + 1, start_date, end_date
    )

    table_df = generate_table_games(
        args.tables, args.seed + 2, start_date, end_date
    )

    financial_df = generate_financial_transactions(
        args.financial, args.seed + 3, start_date, end_date
    )

    security_df = generate_security_events(
        args.security, args.seed + 4, start_date, end_date
    )

    compliance_df = generate_compliance_filings(
        args.compliance, args.seed + 5, start_date, end_date
    )

    # Ensure referential integrity
    slot_df, player_df, table_df, financial_df = ensure_referential_integrity(
        slot_df, player_df, table_df, financial_df
    )

    # Save all datasets
    print("\nSaving datasets...")
    save_dataframe(slot_df, "slot_telemetry", output_dir, formats)
    save_dataframe(player_df, "player_profile", output_dir, formats)
    save_dataframe(table_df, "table_games", output_dir, formats)
    save_dataframe(financial_df, "financial_transactions", output_dir, formats)
    save_dataframe(security_df, "security_events", output_dir, formats)
    save_dataframe(compliance_df, "compliance_filings", output_dir, formats)

    # Print summary
    print("\n" + "=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(f"Total records generated: {sum([
        len(slot_df), len(player_df), len(table_df),
        len(financial_df), len(security_df), len(compliance_df)
    ])}")
    print(f"\nFiles saved to: {output_dir / 'bronze'}")
    print("\nDataset Summary:")
    print(f"  - slot_telemetry_sample: {len(slot_df)} records")
    print(f"  - player_profile_sample: {len(player_df)} records")
    print(f"  - table_games_sample: {len(table_df)} records")
    print(f"  - financial_transactions_sample: {len(financial_df)} records")
    print(f"  - security_events_sample: {len(security_df)} records")
    print(f"  - compliance_filings_sample: {len(compliance_df)} records")


if __name__ == "__main__":
    main()
