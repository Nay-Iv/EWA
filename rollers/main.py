"""Запуск"""

import configparser
import os

from ruleset_parser import Ruleset
import rollers
from setup import EwaConfig

def get_roll_params():
    get_bonus = input("Enter bonus: ")
    bonus = int(get_bonus) if get_bonus != '' else 0
    get_rank = input("Enter rank (leave blank for just chance roll): ")
    rank = get_rank if get_rank != '' else None
    return bonus, rank


def main():
    """Запуск Каталки"""
    roller = EwaConfig.roller
    print("1. Roll Chance\n2. Roll Rank\n3. Roll All")

    choice = input("Enter your choice: ")

    if choice == "1":
        params = get_roll_params()
        roll_result = roller.roll_chance(*params)

    elif choice == "2":
        _, rank_name = get_roll_params()
        roll_result = roller.roll_out(rank_name)

    elif choice == "3":
        params = get_roll_params()
        roll_result = roller.roll_all(*params)

    print(roll_result)


if __name__ == '__main__':
    main()
