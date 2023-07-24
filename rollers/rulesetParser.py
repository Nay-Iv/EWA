import json
from typing import Dict
import dice
from os.path import isfile


class Ruleset:
    data = {}
    ranks = {}
    numRanks: int
    chance: dice.EwaChanceDie

    @classmethod
    def createRankObjects(cls, ranks: Dict[str, Dict[str, object]]) -> None:
        for rankId, rankData in ranks.items():
            outcomes = {}
            for outcomeName, outcomeValues in rankData["outcomes"].items():
                outcomes[outcomeName] = outcomeValues
            rank = dice.EwaRankDie(rankId, rankData["die"], rankData["failUnder"], outcomes)
            cls.ranks[rankId] = rank

    @classmethod
    def parseSource(cls, someStr) -> Dict:
        print(someStr)
        if isfile(someStr) and someStr.endswith('.json'):
            try:
                with open(someStr, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.decoder.JSONDecodeError:
                print("BAD JSON FILE")
                data = None
        else:
            try:
                data = json.loads(someStr)
            except json.decoder.JSONDecodeError:
                print("BAD JSON")
                data = None
        cls.data = data

    @classmethod
    def createChance(cls) -> dice.EwaChanceDie:
        cls.chance = dice.EwaChanceDie(**cls.data["chance"])

    def __init__(self, someStr):
        self.parseSource(someStr)
        self.createRankObjects(self.data["ranks"])
        self.numRanks = len(self.ranks.keys())
        self.createChance()
