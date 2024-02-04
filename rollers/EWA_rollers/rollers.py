"""Каталки костей"""

from dataclasses import dataclass
from typing import Dict
import random
import dice
from output_wrappers import EwaRollResult


@dataclass
class EwaRoller:
    """Каталка костей"""
    ranks: Dict[str, dice.EwaOutcomeDie]
    chance_die: dice.EwaChanceDie

    def roll_rank(self, rank_name: str) -> EwaRollResult:
        """Каталка Исхода"""
        if rank_name not in self.ranks:
            raise ValueError(f"Rank '{rank_name}' not found")
        rank = self.ranks[rank_name]
        roll_result = random.randint(1, rank.die)
        outcome = 'Какой-то'
        for outcome_name, outcome_values in rank.outcomes.items():
            if roll_result in outcome_values:
                outcome = outcome_name
        return EwaRollResult(roll_result=roll_result, roll_outcome=outcome)

    def roll_chance(self, bonus: int = 0, rank_name: str = None) -> EwaRollResult:
        """Каталка Шанса"""

        roll_result = random.randint(1, self.chance_die.die) + bonus
        outcome = None

        if rank_name is not None:
            rank = self.ranks.get(rank_name)
            if rank:
                fail_under = rank.fail_under
                if roll_result >= fail_under:
                    outcome = self.chance_die.success
                else:
                    outcome = self.chance_die.fail

        return EwaRollResult(roll_result=roll_result, roll_outcome=outcome)

    def roll_full(self, chance_bonus: int = 0, rank_name: str = None) -> Dict[str, EwaRollResult]:
        """Каталка полной проверки"""
        chance_outcome = self.roll_chance(chance_bonus, rank_name)
        rank_outcome = self.roll_rank(rank_name)

        result = {
            'rank': rank_outcome,
            'chance': chance_outcome
        }
        return result
