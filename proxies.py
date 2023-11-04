import random
import config

proxies = []


def parse_proxy_str(proxy_str: str):
    p = proxy_str.split(':')
    return {
        'ip': p[0],
        'port': p[1],
        'username': p[2],
        'password': p[3]
    }


with open(config.PROXIES_FILE) as f:
    proxies_str = f.read().splitlines()
    for p in proxies_str:
        proxies.append(parse_proxy_str(p))


def convert_proxy_to_requests_format(proxy):
    return {
        'http': f"socks5://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}",
        'https': f"socks5://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
    }


def get_random():
    return random.choice(proxies)


def get_random_in_requests_format():
    return convert_proxy_to_requests_format(random.choice(proxies))
