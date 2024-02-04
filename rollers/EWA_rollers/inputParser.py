'''Обработка ввода'''

import re
from dataclasses import dataclass
from ruleset_parser import Ruleset
@dataclass
class inputParser:
    input_str: str
    ruleset: Ruleset
    chance_rexp: str = r'([+-]?\d+)'
    rank_rexp: str = r'([Rr]\d+)'
    full_rexp: str = r'([+-]?\d+[Rr]\d+)'
    def parse(self, input_str):
        roll_types = {self.chance_rexp:'chance', self.rank_rexp:'rank', self.full_rexp:'full'}
        params = {}
        for rexp, some_type in roll_types.items():
            if re.fullmatch(rexp, input_str):
                roll_type = some_type