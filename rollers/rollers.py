"""Каталки костей"""

from dataclasses import dataclass
from typing import Tuple, Dict, List
import random
import dice
from output_wrappers import EwaRollResult


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

    def roll_chance(self, num_dice: int = 1, bonus: int = 0, rank_name: str = None) -> Tuple[List[int], str]:
        """Каталка Шанса"""
        outcomes = []
        for i in range(num_dice):
            outcome = random.randint(1, self.chance_die.die) + bonus
            outcomes.append(outcome)
        if rank_name is not None:
            fail_under = self.ranks[rank_name].fail_under
            success_outcome = self.chance_die.success
            fail_outcome = self.chance_die.fail
            outcome_results = [success_outcome if outcome >= fail_under else fail_outcome for outcome in outcomes]
            return outcomes, ", ".join(outcome_results)
        return outcomes, ""

    def roll_all(self, num_chance_dice: int = 1, chance_bonus: int = 0, rank_name: str = None) -> EwaRollResult:
        """Каталка полной проверки"""
        chance_outcomes = []
        for i in range(num_chance_dice):
            chance_result, _ = self.roll_chance(bonus=chance_bonus, rank_name=rank_name)
            chance_outcomes.append(chance_result)
        outcome_value, outcome = self.roll_out(rank_name)
        if rank_name is not None:
            fail_under = self.ranks[rank_name].fail_under
            success_outcome = self.chance_die.success
            fail_outcome = self.chance_die.fail
            overall_outcome = success_outcome if all(
                result >= fail_under for result in chance_outcomes) else fail_outcome
        else:
            overall_outcome = ""
        return EwaRollResult(outcome=outcome, outcome_value=outcome_value, chance_outcomes=chance_outcomes,
                             overall_outcome=overall_outcome)
