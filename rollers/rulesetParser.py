import json
from typing import Dict
import dice

class RankFactory:
    @classmethod
    def createRankObjects(cls, ranks: Dict[str, Dict[str, object]]) -> Dict[str, dice.EwaRankDie]:
        rankObjects = {}
        for rankId, rankData in ranks.items():
            outcomes = {}
            for outcomeName, outcomeValues in rankData["outcomes"].items():
                outcomes[outcomeName] = outcomeValues
            rank = dice.EwaRankDie(rankId, rankData["die"], rankData["failUnder"], outcomes)
            rankObjects[rankId] = rank
        return rankObjects

class Ruleset:
    @classmethod
    def parseSource(self, rulesetPath) -> Dict:
        with open(rulesetPath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
