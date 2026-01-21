"""
Data Generators Package
=======================

Provides synthetic data generators for casino/gaming domain:
- SlotMachineGenerator: Slot machine telemetry and events
- TableGameGenerator: Table game transactions
- PlayerGenerator: Player profiles and loyalty data
- FinancialGenerator: Cage and financial transactions
- SecurityGenerator: Security and surveillance events
- ComplianceGenerator: CTR, SAR, W-2G compliance data
"""

from .base_generator import BaseGenerator
from .slot_machine_generator import SlotMachineGenerator
from .table_games_generator import TableGameGenerator
from .player_generator import PlayerGenerator
from .financial_generator import FinancialGenerator
from .security_generator import SecurityGenerator
from .compliance_generator import ComplianceGenerator

__all__ = [
    "BaseGenerator",
    "SlotMachineGenerator",
    "TableGameGenerator",
    "PlayerGenerator",
    "FinancialGenerator",
    "SecurityGenerator",
    "ComplianceGenerator",
]
