"""Запуск"""
import re

from setup import EwaConfig

def parse_roll_input(input_str):
    roll_type = 'chance'

    if re.fullmatch(r'(r\d+)', input_str):
        roll_type = 'rank'
    elif re.fullmatch(r'([+-]\d+)', input_str):
        roll_type = 'chance'
    elif re.fullmatch(r'([+-]\d+r\d+)', input_str):
        roll_type = 'full'

    roll_params = {}

    if roll_type in ['chance', 'full']:
        chance_match = re.match(r'([+-]\d+)', input_str)
        roll_params['bonus'] = int(chance_match.group(1))

    if roll_type in ['rank', 'full']:
        rank_match = re.search(r'r(\d+)', input_str)
        roll_params['rank'] = rank_match.group(1)

    return roll_type, roll_params


def main():
    """Roll dice"""

    roller = EwaConfig.roller

    while True:
        input_str = input("Enter roll (e.g. '-1r3'): ")

        if input_str.lower() == 'quit':
            break

        roll_type, params = parse_roll_input(input_str)
        bonus = params.get('bonus', 0)
        rank = params.get('rank')

        if roll_type == 'rank':
            roll_result = roller.roll_rank(params['rank'])
        elif roll_type == 'chance':
            roll_result = roller.roll_chance(params['bonus'])
        elif roll_type == 'full':
            roll_result = roller.roll_full(bonus, rank)

        print(roll_result)


if __name__ == '__main__':
    main()