"""Классы возможных игральных костей"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class EwaOutcomeDie:
    """Кость Исхода"""
    name: str
    die: int
    fail_under: int
    outcomes: Dict[str, List[int]]

@dataclass
class EwaChanceDie:
    """Кость Шанса"""
    die: int
    fail: str
    success: str
