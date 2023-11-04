import random
import config

usernames = []

with open(config.USERNAMES_FILE, 'r') as f:
    for line in f:
        usernames.append(line.replace('\n', ''))


def get_random_username():
    return random.choice(usernames)


def generate_email(username: str):
    email_server = random.choice(config.EMAILS)
    return username+'@'+email_server
