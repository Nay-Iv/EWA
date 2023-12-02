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

    def roll_out(self, rank_name: str, num_dice: int = 1) -> List[Tuple[int, str]]:
        """Каталка Исхода"""
        if rank_name not in self.ranks:
            raise ValueError(f"Rank '{rank_name}' not found")
        rank = self.ranks[rank_name]
        outcomes: list[tuple[int, str]] = []
        for _ in range(num_dice):
            roll_result = random.randint(1, rank.die)
            for outcome_name, outcome_values in rank.outcomes.items():
                if roll_result in outcome_values:
                    outcome = outcome_name
            outcomes.append((roll_result, outcome))
        return outcomes

    def roll_chance(self, num_dice: int = 1, bonus: int = 0, rank_name: str = None) -> Tuple[int, List[int], str]:
        """Каталка Шанса"""

        outcomes = []
        chance_results = []

        for _ in range(num_dice):
            outcome = random.randint(1, self.chance_die.die) + bonus
            outcomes.append(outcome)

            if rank_name is not None:
                rank = self.ranks.get(rank_name)
                if rank:
                    fail_under = rank.fail_under
                    if outcome >= fail_under:
                        chance_results.append(self.chance_die.success)
                    else:
                        chance_results.append(self.chance_die.fail)

            else:
                chance_results.append("")

        return num_dice, outcomes, chance_results

    def roll_all(self, num_dice: int = 1, chance_bonus: int = 0, rank_name: str = None) -> EwaRollResult:
        """Каталка полной проверки"""
        num_chance_dice, chance_outcomes, chance_results = self.roll_chance(num_dice, chance_bonus, rank_name)

        rank_outcomes = self.roll_out(rank_name, num_dice)

        if rank_name is not None:
            rank = self.ranks[rank_name]
            fail_under = rank.fail_under
            success_outcome = self.chance_die.success
            fail_outcome = self.chance_die.fail

            chance_passes = [co >= fail_under for co in chance_outcomes]

            if all(chance_passes):
                overall_outcome = success_outcome
            else:
                overall_outcome = fail_outcome

        else:
            overall_outcome = ""

        return EwaRollResult(
            rank_outcomes=rank_outcomes,
            chance_outcomes=chance_outcomes,
            chance_results=chance_results,
            overall_outcome=overall_outcome
        )
