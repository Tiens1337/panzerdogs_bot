from loguru import logger
from time import sleep
import threading
import time
from firebase_api import FirebaseApi
from panzerdogs_api import PanzerdogsApi
import credentials_generator
from match_stats import MatchStats
import random
import proxies
import config

from concurrent.futures import ThreadPoolExecutor, wait
import threading

import models.db_initializer
from models.account import AccountData


def start_in_thread(acc: AccountData):
    rand_proxy = False
    while True:
        sleep(random.randint(0, 60)) # for more smooth start

        firebaseApi = FirebaseApi()
        panzerdogsApi = {}

        proxy = ""
        if rand_proxy:
            proxy = proxies.get_random_in_requests_format()
        else: 
            proxy_str = proxies.parse_proxy_str(acc.proxy)
            proxy = proxies.convert_proxy_to_requests_format(proxy_str)

        if acc.pd_username is None:
            username = credentials_generator.get_random_username()
            email = credentials_generator.generate_email(username)

            resp = firebaseApi.register_new_user(email, config.DEFAULT_PASS)
            if resp is None:
                logger.error(f'{acc.id}: Failed to register new user in firebase')
                continue

            panzerdogsApi = PanzerdogsApi(resp["idToken"], proxy)
            resp = panzerdogsApi.register(username)
            if resp is None:
                logger.error(f'{acc.id}: Failed to register new user in game')
                rand_proxy = True
                continue

            resp = panzerdogsApi.set_recruit()
            if resp is None:
                logger.error(f'{acc.id}: Failed to set recruit')
                rand_proxy = True
                continue

            resp = panzerdogsApi.link_wallet(acc.public_key)
            if resp is None:
                logger.error(f'{acc.id}: Failed to link wallet')
                rand_proxy = True
                continue

            while True:
                try:
                    acc.pd_username = username
                    acc.pd_email = email
                    acc.pd_password = config.DEFAULT_PASS
                    acc.save()
                    break
                except Exception as e:
                    logger.error(f'{acc.id}: database is locked')
                    sleep(5)


        else:
            resp = firebaseApi.signup(acc.pd_email, acc.pd_password)
            if resp is None:
                logger.error(f'{acc.id}: Failed to sign up in firebase')
                rand_proxy = True
                continue
            panzerdogsApi = PanzerdogsApi(resp["idToken"], acc.proxy)

        for i in range(3):
            match_stats = MatchStats()
            logger.info(f"{acc.id}: Starting fight {i}")

            resp = panzerdogsApi.get_matchmaking()
            if resp is None or resp.get("error"):
                logger.error(f"{acc.id}: Failed to get matchmaking")
                exit()

            room_id = resp["roomId"]
            logger.info(f"{acc.id}: Match started, match id: {room_id}")
            time.sleep(60)

            match_stats.update()
            resp = panzerdogsApi.ocs(match_stats)
            # logger.info(f"{acc.id}: Ocs success: {resp['success']}")
            time.sleep(60)

            match_stats.update()
            resp = panzerdogsApi.ocs(match_stats)
            # logger.info(f"Ocs success: {resp['success']}")
            resp = panzerdogsApi.match_end(room_id, match_stats)
            if resp['success']:
                logger.success(f"{acc.id}: Match successfully ended, added XP: {resp['xpData']['addedXP']}")
            else:
                logger.error(f"{acc.id}: Match ended with error")
            time.sleep(10)
        logger.success("Job done!")
        break


def start():
    accs = list(AccountData.select())
    models.connector.connection.close()
    
    with ThreadPoolExecutor(config.MAX_WORKERS) as executor:
        future = {executor.submit(start_in_thread, acc)
                    for acc in accs}
        wait(future)
        logger.success('====== DONE ======')


if __name__ == '__main__':
    start()
