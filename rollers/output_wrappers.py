"""Обёртки для каталок"""

from typing import List
from dataclasses import dataclass

@dataclass
class EwaRollResult:
    """Результат броска"""
    outcome: str
    outcome_value: int
    chance_outcomes: List[int]
    overall_outcome: str
