"""Обёртки для каталок"""

from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class EwaRollResult:
    """Результат броска"""
    rank_outcomes: List[Tuple[int, str]]
    chance_outcomes: List[int]
    chance_results: List[str]
    overall_outcome: str
