import rollers
import rulesetParser
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

tg_bot_token = config['DEFAULT']['TELEGRAM_BOT_TOKEN']
relative_path = config['DEFAULT']['RULESET_PATH']
config_file_path = os.path.abspath('config.ini')
config_dir_path = os.path.dirname(config_file_path)
ruleset_path = os.path.abspath(os.path.join(config_dir_path, relative_path))


def getChanceParams():
    result = [int(input("bonus: "))]
    if input("rank?(y/n): ").lower() == 'y':
        result += getOutParams()
    return result


def getOutParams():
    return [input("rank:")]


def getAllParams():
    chanceParams = getChanceParams()
    if len(chanceParams) > 1:
        return chanceParams
    else:
        return chanceParams+getOutParams()


def main():
    rules = rulesetParser.Ruleset(ruleset_path)
    roller = rollers.EwaRoller(chanceDie=rules.chance, ranks=rules.ranks)
    responses = {1: roller.rollChance, 2: roller.rollOut, 3: roller.rollAll}
    paramSetters = {1: getChanceParams, 2: getOutParams, 3: getAllParams}
    while True:
        response = int(input("******\n1. Roll Chance\n2. Roll Rank\n3. Roll All\n(0 to exit)\n----\nI want to: "))
        if response == 0:
            break
        for i in [1, 2, 3]:
            if i == response:
                params = paramSetters[i]()
                print(responses[i](*params))


if __name__ == '__main__':
    main()
