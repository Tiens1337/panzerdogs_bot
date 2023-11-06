import json
import requests

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

import proxies

KEY = "AIzaSyCArlNof-vMCzyHYOaLyQ881RpVwRaNu-Q"


class FirebaseApi:
    def __init__(self) -> None:
        self.id_token = None
        self.refresh_token = None
        self.token_refresh_time = None

        software_names = [SoftwareName.ANDROID.value]
        operating_systems = [OperatingSystem.ANDROID.value]
        user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems, limit=100)

        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': user_agent_rotator.get_random_user_agent()})
        
        self.session.proxies = proxies.get_random_in_requests_format()

    def post(url, data):
        pass

    def refresh_token(self):
        pass

    def register_new_user(self, email: str, password: str):
        resp = self.signup_new_user()
        if resp is None:
            return None

        resp = self.set_account_info(email, password)
        return resp

    def signup_new_user(self):
        url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={KEY}"

        try:
            response = self.session.post(url=url)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            data = json.loads(response.text)
            self.id_token = data["idToken"]
            self.refresh_token = data["refreshToken"]
            return data
        return None

    def signup(self, email, password):
        url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={KEY}"

        input_data = {
            "email":email,"password":password,"returnSecureToken":True
        }

        try:
            response = self.session.post(url=url, json=input_data)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            data = json.loads(response.text)
            self.id_token = data["idToken"]
            self.refresh_token = data["refreshToken"]
            return data
        return None

    def get_account_info(self, id_token: str):
        url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={KEY}"
        input_data = {
            "idToken": id_token
        }

        try:
            response = self.session.post(url=url, json=input_data)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def set_account_info(self, email: str, password: str):
        if self.id_token is None:
            raise Exception("no idToken")

        url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={KEY}"
        input_data = {
            "returnSecureToken": True,
            "idToken": self.id_token,
            "email": email,
            "password": password
        }

        try:
            response = self.session.post(url=url, json=input_data)
        except Exception as ex:
            print(ex)
            return None

        if response.status_code == 200:
            return json.loads(response.text)
        return None
