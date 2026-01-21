"""
Base Generator Class
====================

Abstract base class for all data generators providing common functionality:
- Seed management for reproducibility
- Output format handling (DataFrame, Parquet, JSON)
- Batch generation
- Progress tracking
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterator
import hashlib
import uuid

import pandas as pd
import numpy as np
from faker import Faker
from tqdm import tqdm


class BaseGenerator(ABC):
    """Abstract base class for data generators."""

    def __init__(
        self,
        seed: int | None = None,
        locale: str = "en_US",
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ):
        """
        Initialize the generator.

        Args:
            seed: Random seed for reproducibility
            locale: Faker locale
            start_date: Start date for generated data
            end_date: End date for generated data
        """
        self.seed = seed or 42
        self.locale = locale
        self.start_date = start_date or datetime.now() - timedelta(days=30)
        self.end_date = end_date or datetime.now()

        # Initialize random generators
        self.faker = Faker(locale)
        Faker.seed(self.seed)
        np.random.seed(self.seed)

        # Schema definition (to be overridden by subclasses)
        self._schema: dict[str, str] = {}

    @property
    def schema(self) -> dict[str, str]:
        """Return the schema definition for this generator."""
        return self._schema

    @abstractmethod
    def generate_record(self) -> dict[str, Any]:
        """Generate a single record. Must be implemented by subclasses."""
        pass

    def generate(
        self,
        num_records: int,
        show_progress: bool = True,
    ) -> pd.DataFrame:
        """
        Generate multiple records.

        Args:
            num_records: Number of records to generate
            show_progress: Show progress bar

        Returns:
            DataFrame containing generated records
        """
        records = []
        iterator = range(num_records)

        if show_progress:
            iterator = tqdm(iterator, desc=f"Generating {self.__class__.__name__}")

        for _ in iterator:
            records.append(self.generate_record())

        return pd.DataFrame(records)

    def generate_batches(
        self,
        num_records: int,
        batch_size: int = 10000,
        show_progress: bool = True,
    ) -> Iterator[pd.DataFrame]:
        """
        Generate records in batches (memory efficient).

        Args:
            num_records: Total number of records
            batch_size: Records per batch
            show_progress: Show progress bar

        Yields:
            DataFrame batches
        """
        remaining = num_records
        batch_num = 0

        while remaining > 0:
            current_batch = min(batch_size, remaining)
            if show_progress:
                print(f"Generating batch {batch_num + 1} ({current_batch} records)...")

            yield self.generate(current_batch, show_progress=False)
            remaining -= current_batch
            batch_num += 1

    def to_parquet(
        self,
        df: pd.DataFrame,
        output_path: str | Path,
        partition_cols: list[str] | None = None,
    ) -> None:
        """
        Save DataFrame to Parquet format.

        Args:
            df: DataFrame to save
            output_path: Output file or directory path
            partition_cols: Columns to partition by
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if partition_cols:
            df.to_parquet(
                output_path,
                partition_cols=partition_cols,
                engine="pyarrow",
                index=False,
            )
        else:
            df.to_parquet(output_path, engine="pyarrow", index=False)

    def to_json(
        self,
        df: pd.DataFrame,
        output_path: str | Path,
        orient: str = "records",
        lines: bool = True,
    ) -> None:
        """
        Save DataFrame to JSON format.

        Args:
            df: DataFrame to save
            output_path: Output file path
            orient: JSON orientation
            lines: Write as JSON lines
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_json(output_path, orient=orient, lines=lines, date_format="iso")

    # ==========================================================================
    # Helper Methods
    # ==========================================================================

    def random_datetime(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> datetime:
        """Generate a random datetime within range."""
        start = start or self.start_date
        end = end or self.end_date
        delta = end - start
        random_seconds = np.random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)

    def generate_uuid(self) -> str:
        """Generate a UUID."""
        return str(uuid.uuid4())

    def hash_value(self, value: str, salt: str = "") -> str:
        """Generate SHA-256 hash of a value."""
        return hashlib.sha256(f"{salt}{value}".encode()).hexdigest()

    def mask_ssn(self, ssn: str) -> str:
        """Mask SSN showing only last 4 digits."""
        return f"XXX-XX-{ssn[-4:]}"

    def mask_card_number(self, card_number: str) -> str:
        """Mask card number showing only last 4 digits."""
        return f"****-****-****-{card_number[-4:]}"

    def weighted_choice(
        self,
        choices: list[Any],
        weights: list[float],
    ) -> Any:
        """Make a weighted random choice."""
        return np.random.choice(choices, p=weights)

    def add_metadata_columns(self, record: dict[str, Any]) -> dict[str, Any]:
        """Add standard metadata columns to a record."""
        record["_ingested_at"] = datetime.now().isoformat()
        record["_source"] = self.__class__.__name__
        record["_batch_id"] = self.generate_uuid()[:8]
        return record
