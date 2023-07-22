from dataclasses import dataclass
from typing import Tuple, Dict
import random
import dice

@dataclass
class EwaRoller:
    ranks: Dict[str, dice.EwaRankDie]
    chanceDie: dice.EwaChanceDie

    def rollOut(self, rankName: str) -> Tuple[int, str]:
        if rankName not in self.ranks:
            raise ValueError(f"Rank '{rankName}' not found")
        rank = self.ranks[rankName]
        outcome = None
        while outcome is None:
            rollResult = random.randint(1, rank.die)
            for outcomeName, outcomeValues in rank.outcomes.items():
                if rollResult in outcomeValues:
                    outcome = outcomeName
                    break
        return rollResult, outcome

    def rollChance(self, bonus: int = 0) -> int:
        return random.randint(1, self.chanceDie.die) + bonus

    def rollAll(self, rankName: str, chanceBonus: int = 0) -> Tuple[int, str, int, str]:
        chanceResult = self.rollChance(chanceBonus)
        rankResult, outcome = self.rollOut(rankName)
        if chanceResult < self.ranks[rankName].failUnder:
            chanceOutcome = self.chanceDie.fail
        else:
            chanceOutcome = self.chanceDie.success
        return rankResult, outcome, chanceResult, chanceOutcome