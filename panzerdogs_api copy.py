from datetime import datetime
import json
import random
import requests
import proxies

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

import compressor


class PanzerdogsApi:
    def __init__(self, auth_token: str, proxy) -> None:
        self.username = None

        with open("match_end.json", "r", encoding="utf-8") as f:
            self.match_end_data = json.load(f)

        software_names = [SoftwareName.ANDROID.value]
        operating_systems = [OperatingSystem.ANDROID.value]

        user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems, limit=100)

        self.session = requests.Session()
        self.session.headers.update({'Sid': 'null',
                                    'Authorization': auth_token,
                                     'Idtoken': auth_token,
                                     'User-Agent': user_agent_rotator.get_random_user_agent(),
                                     'Serverbuild': "48",
                                     "Gamemode": "teamdeathmatch",
                                     "Region": "eu"})
        
        proxy = proxies.parse_proxy_str(proxy)
        self.session.proxies = proxies.convert_proxy_to_requests_format(proxy)

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
    
    def check_wallet():
        pass
    # https://lobby2.luckykatgames.net/wallet-link/get

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

    def ocs(self):
        url = "https://lobby2.luckykatgames.net/ocs"
        data = {"moveDistance": random.randint(20, 80),
                "boostDistance": 15,
                "dmgDealt": (random.randint(30, 70) * 100),
                "kills": random.randint(5, 6),
                "firstBlood": random.randint(0, 1),
                "dmgReceived": random.randint(50, 600)}
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

    def match_end(self, room_id: str):

        url = f"https://lobby2.luckykatgames.net/session/match_end?id={room_id}"

        self.match_end_data["playerData"]["name"] = self.username
        self.match_end_data["playerData"]["stats"]["kills"] = random.randint(6, 10)
        self.match_end_data["playerData"]["stats"]["killStreakTime"] = int(datetime.now().timestamp() * 1000)
        self.match_end_data["playerData"]["stats"]["botKills"] = self.match_end_data["playerData"]["stats"]["kills"]
        self.match_end_data["playerData"]["stats"]["deaths"] = random.randint(0, 1)
        if self.match_end_data["playerData"]["stats"]["deaths"] > 0:
            self.match_end_data["playerData"]["stats"]["timeDead"] = 5
        else:
            self.match_end_data["playerData"]["stats"]["timeDead"] = 0
        self.match_end_data["playerData"]["stats"]["score"] = random.randint(40, 50)
        self.match_end_data["playerData"]["stats"]["dmgDealt"] = (random.randint(50, 80) * 100)
        self.match_end_data["playerData"]["stats"]["dmgReceived"] = random.uniform(200.0, 500.0)
        self.match_end_data["playerData"]["stats"]["firstBlood"] = random.randint(0, 1)
        self.match_end_data["playerData"]["stats"]["moveDistance"] = random.uniform(60.0, 90.0)
        self.match_end_data["playerData"]["stats"]["boostDistance"] = random.uniform(15.0, 20.0)
        self.match_end_data["playerData"]["stats"]["boostDistanceInt"] = int(
            self.match_end_data["playerData"]["stats"]["boostDistance"])

        self.match_end_data["playerData"]["stats"]["dmgDealtWith"]["0"] = self.match_end_data["playerData"]["stats"]["dmgDealt"]
        self.match_end_data["playerData"]["stats"]["dmgReceivedBy"]["0"] = self.match_end_data["playerData"][
            "stats"]["dmgReceived"]
        self.match_end_data["playerData"]["stats"]["dmgDealtWithTurret"][
            "standard"] = self.match_end_data["playerData"]["stats"]["dmgDealt"]

        self.match_end_data["matchStats"]["kills"] = self.match_end_data["playerData"]["stats"]["kills"]
        self.match_end_data["matchStats"]["botKills"] = self.match_end_data["playerData"]["stats"]["kills"]
        self.match_end_data["matchStats"]["firstBlood"] = self.match_end_data["playerData"]["stats"]["firstBlood"]
        self.match_end_data["matchStats"]["dmgDealt"] = self.match_end_data["playerData"]["stats"]["dmgDealt"]
        self.match_end_data["matchStats"]["dmgReceived"] = self.match_end_data["playerData"]["stats"]["dmgReceived"]
        self.match_end_data["matchStats"]["boostDistance"] = self.match_end_data["playerData"]["stats"][
            "boostDistanceInt"]

        self.match_end_data["matchStats"]["dmgdealtwith_Basic"] = self.match_end_data["playerData"]["stats"]["dmgDealt"]
        self.match_end_data["matchStats"]["dmgreceivedby_Basic"] = self.match_end_data["playerData"]["stats"][
            "dmgReceived"]
        self.match_end_data["matchStats"]["dmgdealtwith_turret_standard"] = self.match_end_data["playerData"]["stats"]["dmgDealt"]

        self.match_end_data["matchStats"]["killwith_turret_standard"] = self.match_end_data["playerData"]["stats"]["kills"]
        self.match_end_data["matchStats"]["killwith_chassis_balanced"] = self.match_end_data["playerData"]["stats"]["kills"]
        self.match_end_data["matchStats"]["killwith_tracks_balanced"] = self.match_end_data["playerData"]["stats"]["kills"]

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
