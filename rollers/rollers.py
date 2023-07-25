"""Каталки костей"""

from dataclasses import dataclass
from typing import Tuple, Dict
import random
import dice

@dataclass
class EwaRoller:
    """Каталка костей"""
    ranks: Dict[str, dice.EwaOutcomeDie]
    chance_die: dice.EwaChanceDie

    def roll_out(self, rank_name: str) -> Tuple[int, str]:
        """Каталка Исхода"""
        if rank_name not in self.ranks:
            raise ValueError(f"Rank '{rank_name}' not found")
        rank = self.ranks[rank_name]
        outcome = None
        while outcome is None:
            roll_result = random.randint(1, rank.die)
            for outcome_name, outcome_values in rank.outcomes.items():
                if roll_result in outcome_values:
                    outcome = outcome_name
                    break
        return roll_result, outcome

    def roll_chance(self, bonus: int = 0, rank_name: str = None) -> Tuple[int, str]:
        """Каталка Шанса"""
        outcome = random.randint(1, self.chance_die.die) + bonus
        if rank_name is not None:
            if outcome < self.ranks[rank_name].fail_under:
                return outcome, self.chance_die.fail
            return outcome, self.chance_die.success
        return outcome, ""

    def roll_all(self, chance_bonus: int = 0, rank_name: str = None) -> Tuple[int, str, int, str]:
        """Каталка полной проверки"""
        chance_result, chance_outcome = self.roll_chance(chance_bonus, rank_name)
        rank_result, outcome = self.roll_out(rank_name)
        return rank_result, outcome, chance_result, chance_outcome
