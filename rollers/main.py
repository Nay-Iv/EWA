"""Запуск"""

import configparser
import os

from output_wrappers import EwaRollResult
from ruleset_parser import Ruleset
import rollers

config = configparser.ConfigParser()
config.read('config.ini')

tg_bot_token = config['DEFAULT']['TELEGRAM_BOT_TOKEN']
relative_path = config['DEFAULT']['RULESET_PATH']
config_file_path = os.path.abspath('config.ini')
config_dir_path = os.path.dirname(config_file_path)
ruleset_path = os.path.abspath(os.path.join(config_dir_path, relative_path))


def get_roll_params():
    num_dice = int(input("Enter number of dice: "))
    bonus = int(input("Enter bonus: "))
    rank_name = input("Enter rank (leave blank for just chance roll): ")
    return num_dice, bonus, rank_name

def print_roll(roll_result: EwaRollResult):
    if isinstance(roll_result, tuple):
        num_dice, chance_outcomes, chance_results = roll_result
        print(f"Number of dice: {num_dice}")
        print(f"Chance outcomes: {chance_outcomes}")
        print(f"Chance results: {chance_results}")

    else:
        print(f"Chance outcomes: {roll_result.chance_outcomes}")
        print(f"Rank outcomes: {roll_result.rank_outcomes}")
        print(f"Chance results: {roll_result.chance_results}")
        print(f"Overall outcome: {roll_result.overall_outcome}")


def main():
    """Запуск Каталки"""
    rules = Ruleset(ruleset_path)
    roller = rollers.EwaRoller(chance_die=rules.chance, ranks=rules.ranks)
    print("1. Roll Chance\n2. Roll Rank\n3. Roll All")

    choice = input("Enter your choice: ")

    if choice == "1":
        params = get_roll_params()
        roll_result = roller.roll_chance(*params[:-1])

    elif choice == "2":
        num_dice, _, rank_name = get_roll_params()
        roll_result = roller.roll_out(rank_name, num_dice)

    elif choice == "3":
        params = get_roll_params()
        roll_result = roller.roll_all(*params)

    print_roll(roll_result)


if __name__ == '__main__':
    main()
