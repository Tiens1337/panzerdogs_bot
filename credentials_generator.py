import random
import config
import os

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import models.db_initializer
from models.account import AccountData

usernames = []

software_names = [SoftwareName.ANDROID.value]
operating_systems = [OperatingSystem.ANDROID.value]

user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=10000)


uagents = {}

def user_agents_process():
    if os.path.isfile('uagents.txt'):
        with open('uagents.txt', 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                s = line.split(':::')
                uagents[int(s[0])] = s[1]

    
    accs = list(AccountData.select())
    models.connector.connection.close()
    with open('uagents.txt', 'a+') as f:
        for acc in accs:
            uagent = uagents.get(acc.id)
            if uagent is None:
                uagent = user_agent_rotator.get_random_user_agent()
                f.write(f'{acc.id}:::{uagent}\n')
                uagents[acc.id] = uagent


def get_uagent(acc_id: int):
    uagent = uagents.get(acc_id)
    if uagent is None:
        uagent = user_agent_rotator.get_random_user_agent()
    return uagent


user_agents_process()



with open(config.USERNAMES_FILE, 'r') as f:
    for line in f:
        usernames.append(line.replace('\n', ''))


def get_random_username():
    return random.choice(usernames)


def generate_email(username: str):
    email_server = random.choice(config.EMAILS)
    return username+'@'+email_server
