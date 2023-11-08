from random import randint, choice, uniform
import json


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


BOT_NAMES = [
    "FreshMemory",
    "SECRET",
    "LiberalSyrup",
    "UniformGalley",
    "Source4",
    "quietlycra",
    "One03",
    "ExcitedSpeaker",
    "GradualSea",
    "REGULARSEPAL",
    "AncientCheque",
    "SKULL1",
    "Miter3",
    "Reality88",
    "OddSoldier",
    "Corsage4",
    "goodmusic",
    "Patient4781",
    "Score34",
    "CuteIkebana"
]


def generate_bot_id():
    return random_with_N_digits(12)


bot_example = {}
with open('bot_example.json', 'r') as f:
    bot_example = json.load(f)


def genereate_bot(deaths: int = randint(0, 2)):
    bot = bot_example.copy()
    name = choice(BOT_NAMES)

    bot['name'] = name
    bot['playerId'] = generate_bot_id()

    bot['stats']['deaths'] = deaths
    bot['stats']['timeDead'] = deaths * 5

    bot["stats"]["dmgDealt"] = (randint(0, 20) * 100)
    bot["stats"]["dmgReceived"] = uniform(200.0, 500.0)

    bot["stats"]["moveDistance"] = uniform(60.0, 90.0)
    bot["stats"]["boostDistance"] = uniform(15.0, 20.0)

    bot["stats"]["dmgDealtWith"]["0"] = bot["stats"]["dmgDealt"]
    bot["stats"]["dmgReceivedBy"]["0"] = bot["stats"]["dmgReceived"]
    bot["stats"]["dmgDealtWithTurret"]["light"] = bot["stats"]["dmgDealt"]

    bot["dog"]["name"] = name

    return json.dumps(bot)
