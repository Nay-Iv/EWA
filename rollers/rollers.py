from dataclasses import dataclass
from typing import Tuple, Dict, Optional
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

    def rollChance(self, bonus: int = 0, rankName: str = None) -> Tuple[int,str]:
        outcome = random.randint(1, self.chanceDie.die)+bonus
        if rankName is not None:
            if outcome < self.ranks[rankName].failUnder:
                return outcome, self.chanceDie.fail
            else:
                return outcome, self.chanceDie.success
        else:
            return outcome, ""

    def rollAll(self, chanceBonus: int = 0, rankName: str = None) -> Tuple[int, str, int, str]:
        chanceResult, chanceOutcome = self.rollChance(chanceBonus, rankName)
        rankResult, outcome = self.rollOut(rankName)
        return rankResult, outcome, chanceResult, chanceOutcome