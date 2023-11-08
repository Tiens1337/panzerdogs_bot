from datetime import datetime
import json
import random
import requests
import proxies
from match_stats import MatchStats
import bot_generator
from credentials_generator import get_uagent
from models.account import AccountData

import compressor

import os, random

def get_random_match_end():
    return random.choice(os.listdir("match_end_examples"))


class PanzerdogsApi:
    def __init__(self, auth_token: str, proxy, acc: AccountData) -> None:
        self.username = None

        with open(f"match_end_examples/{get_random_match_end()}", "r", encoding="utf-8") as f:
            self.match_end_data = json.load(f)

        self.session = requests.Session()
        self.session.headers.update({'Sid': 'null',
                                    'Authorization': auth_token,
                                     'Idtoken': auth_token,
                                     'User-Agent': get_uagent(acc.id),
                                     'Serverbuild': "48",
                                     "Gamemode": "teamdeathmatch",
                                     "Region": "eu"})

        self.session.proxies = proxy

    def register(self, username: str):
        url = "https://lobby2.luckykatgames.net/userdata/register"
        input_data = {"userName": username, "signUpPlatform": "ANDROID",
                      "signUpProvider": "email", "gaClientId": "", "ftueStage": 10000}

        try:
            response = self.session.post(url=url, json=input_data)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            self.username = username  # todo: need do get username without registration
            return json.loads(response.text)
        return None

    def get_user_data(self):
        url = "https://lobby2.luckykatgames.net/userdata"

        try:
            response = self.session.get(url=url)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def skip_tutorial(self):
        url = "https://lobby2.luckykatgames.net/userdata/ftueskip"

        try:
            response = self.session.post(url=url)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def set_recruit(self):
        url = "https://lobby2.luckykatgames.net/userdata/setrecruit"
        input_data = {"dogIndex": 0, "colourIndex": 0, "bodyIndex": 0}

        try:
            response = self.session.post(url=url, json=input_data)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def link_wallet(self, public_key: str):
        url = "https://lobby2.luckykatgames.net/wallet-link/link"
        input_data = {"publicKey": public_key}

        try:
            response = self.session.post(url=url, json=input_data)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def check_wallet(self):
        url = 'https://lobby2.luckykatgames.net/wallet-link/get'

        try:
            response = self.session.get(url=url)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def get_matchmaking(self):
        url = "https://lobby2.luckykatgames.net/matchmaking"

        try:
            response = self.session.get(url=url)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            res = json.loads(response.text)
            return res
        return None

    def ocs(self, stats: MatchStats):
        url = "https://lobby2.luckykatgames.net/ocs"
        data = {
            "moveDistance": int(stats.move_distance),
            "boostDistance": int(stats.boost_distance),
            "dmgDealt": stats.dmg_dealt,
            "kills": stats.kills,
            "firstBlood": stats.first_blood,
            "dmgReceived": stats.dmg_received
        }
        compressed_data = compressor.Compress(json.dumps(data))
        input_data = {"data": compressed_data}

        try:
            response = self.session.post(url=url, json=input_data)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def match_end(self, room_id: str, stats: MatchStats):

        url = f"https://lobby2.luckykatgames.net/session/match_end?id={room_id}"

        self.match_end_data["playerData"]["name"] = self.username
        self.match_end_data["playerData"]["stats"]["kills"] = stats.kills
        self.match_end_data["playerData"]["stats"]["killStreakTime"] = int(
            datetime.now().timestamp() * 1000)
        self.match_end_data["playerData"]["stats"]["botKills"] = stats.kills
        self.match_end_data["playerData"]["stats"]["deaths"] = stats.deaths
        self.match_end_data["playerData"]["stats"]["timeDead"] = stats.time_dead

        self.match_end_data["playerData"]["stats"]["score"] = stats.score
        self.match_end_data["playerData"]["stats"]["dmgDealt"] = stats.dmg_dealt
        self.match_end_data["playerData"]["stats"]["dmgReceived"] = stats.dmg_received
        self.match_end_data["playerData"]["stats"]["firstBlood"] = stats.first_blood
        self.match_end_data["playerData"]["stats"]["moveDistance"] = stats.move_distance
        self.match_end_data["playerData"]["stats"]["moveDistanceInt"] = int(
            stats.move_distance)
        self.match_end_data["playerData"]["stats"]["boostDistance"] = stats.boost_distance
        self.match_end_data["playerData"]["stats"]["boostDistanceInt"] = int(
            stats.boost_distance)

        self.match_end_data["playerData"]["stats"]["dmgDealtWith"]["0"] = stats.dmg_dealt
        self.match_end_data["playerData"]["stats"]["dmgReceivedBy"]["0"] = stats.dmg_received
        self.match_end_data["playerData"]["stats"]["dmgDealtWithTurret"]["standard"] = stats.dmg_dealt

        self.match_end_data["matchStats"]["kills"] = stats.kills
        self.match_end_data["matchStats"]["botKills"] = stats.kills
        self.match_end_data["matchStats"]["firstBlood"] = stats.first_blood
        self.match_end_data["matchStats"]["dmgDealt"] = stats.dmg_dealt
        self.match_end_data["matchStats"]["dmgReceived"] = stats.dmg_received
        self.match_end_data["matchStats"]["boostDistance"] = int(stats.boost_distance)

        self.match_end_data["matchStats"]["dmgdealtwith_Basic"] = stats.dmg_dealt
        self.match_end_data["matchStats"]["dmgreceivedby_Basic"] = stats.dmg_received
        self.match_end_data["matchStats"]["dmgdealtwith_turret_standard"] = stats.dmg_dealt

        self.match_end_data["matchStats"]["killwith_turret_standard"] = stats.kills
        self.match_end_data["matchStats"]["killwith_chassis_balanced"] = stats.kills
        self.match_end_data["matchStats"]["killwith_tracks_balanced"] = stats.kills

        if stats.kills == 10:
            self.match_end_data["matchData"]["reason"] = 'score'
        else:
            self.match_end_data["matchData"]["reason"] = 'time'
        
        self.match_end_data["matchData"]["teamScores"]["0"] = stats.kills

        for i in range(1, 5):
            self.match_end_data["matchData"]["playersJson"][i] = bot_generator.genereate_bot()
        
        compressed_data = compressor.Compress(
            json.dumps(self.match_end_data))
        input_data = {"data": compressed_data}

        try:
            response = self.session.post(url=url, json=input_data)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None
