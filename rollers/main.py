"""Запуск"""

import configparser
import os
from ruleset_parser import Ruleset
import rollers

config = configparser.ConfigParser()
config.read('config.ini')

tg_bot_token = config['DEFAULT']['TELEGRAM_BOT_TOKEN']
relative_path = config['DEFAULT']['RULESET_PATH']
config_file_path = os.path.abspath('config.ini')
config_dir_path = os.path.dirname(config_file_path)
ruleset_path = os.path.abspath(os.path.join(config_dir_path, relative_path))


def get_chance_params():
    """Задаёт Шанс"""
    result = [int(input("bonus: "))]
    if input("rank?(y/n): ").lower() == 'y':
        result += get_out_params()
    return result


def get_out_params():
    """Задаёт Исход"""
    return [input("rank:")]


def get_all_params():
    """Задаёт полную проверку"""
    chance_params = get_chance_params()
    if len(chance_params) > 1:
        return chance_params
    return chance_params + get_out_params()


def main():
    """Запуск Каталки"""
    rules = Ruleset(ruleset_path)
    roller = rollers.EwaRoller(chance_die=rules.chance, ranks=rules.ranks)
    responses = {1: roller.roll_chance, 2: roller.roll_out, 3: roller.roll_all}
    param_setters = {1: get_chance_params, 2: get_out_params, 3: get_all_params}
    while True:
        response = int(input("""
        ******
        1. Roll Chance
        2. Roll Rank
        3. Roll All
        (0 to exit)
        ----
        I want to: """))
        if response == 0:
            break
        for i in [1, 2, 3]:
            if i == response:
                params = param_setters[i]()
                print(responses[i](*params))


if __name__ == '__main__':
    main()
