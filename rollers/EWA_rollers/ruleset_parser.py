"""Вычитывалка правил"""

import json
from typing import Dict
from os.path import isfile
from rollers.EWA_rollers import dice

class Ruleset:
    """Вычитывалка правил"""
    data = {}
    ranks = {}
    num_ranks: int
    chance: dice.EwaChanceDie
    drama = {}

    @classmethod
    def parse_source(cls, some_str):
        """Читаем из файла или строки"""
        print(some_str)
        if isfile(some_str) and some_str.endswith('.json'):
            try:
                data = cls.parse_file(some_str)
            except json.decoder.JSONDecodeError:
                print("BAD JSON FILE")
                data = None
        else:
            try:
                data = cls.parse_string(some_str)
            except json.decoder.JSONDecodeError:
                print("BAD JSON")
                data = None
        cls.data = data

    @classmethod
    def parse_file(cls, some_str):
        """Читаем из файла"""
        with open(some_str, 'r', encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def parse_string(cls, some_str):
        """Читаем из строки"""
        return json.loads(some_str)

    @classmethod
    def create_rank_objects(cls, ranks: Dict[str, Dict[str, object]]):
        """Фабрика Исходов"""
        for rank_id, rank_data in ranks.items():
            outcomes = {}
            for outcome_name, outcome_values in rank_data["outcomes"].items():
                outcomes[outcome_name] = outcome_values
            rank = dice.EwaOutcomeDie(rank_id, rank_data["die"], rank_data["failUnder"], outcomes)
            cls.ranks[rank_id] = rank

    @classmethod
    def create_chance(cls) -> dice.EwaChanceDie:
        """Заводим кость Шанса"""
        cls.chance = dice.EwaChanceDie(**cls.data["chance"])

    def __init__(self, some_str):
        self.parse_source(some_str)
        self.create_rank_objects(self.data["ranks"])
        self.num_ranks = len(self.ranks.keys())
        self.create_chance()
