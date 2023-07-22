from dataclasses import dataclass
from typing import List, Tuple, Dict, Union

@dataclass
class EwaRankDie:
    name: str
    die: int
    failUnder: int
    outcomes: Dict[str, List[int]]

@dataclass
class EwaChanceDie:
    die: int
    fail: str
    success: str