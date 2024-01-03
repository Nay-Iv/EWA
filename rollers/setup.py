"""Запуск"""

import configparser
import os
from dataclasses import dataclass

from EWA_rollers.ruleset_parser import Ruleset
from EWA_rollers import rollers

config = configparser.ConfigParser()
config.read('config.ini')


@dataclass
class EwaConfig:
    tg_bot_token = config['DEFAULT']['TELEGRAM_BOT_TOKEN']
    relative_path = config['DEFAULT']['RULESET_PATH']
    config_file_path = os.path.abspath('config.ini')
    config_dir_path = os.path.dirname(config_file_path)
    ruleset_path = os.path.abspath(os.path.join(config_dir_path, relative_path))
    rules = Ruleset(ruleset_path)
    roller = rollers.EwaRoller(chance_die=rules.chance, ranks=rules.ranks)
