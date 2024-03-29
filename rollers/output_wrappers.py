"""Обёртки для каталок"""

from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class EwaRollResult:
    """Результат броска"""
    roll_result: int
    roll_outcome: str
    pretty_result: str = None

    def __init__(self, roll_result, roll_outcome=None):
        self.roll_result = roll_result
        self.roll_outcome = roll_outcome
        self.pretty_result = f"{self.roll_outcome}"+(f"({self.roll_result})" if self.roll_result is not None else '')
