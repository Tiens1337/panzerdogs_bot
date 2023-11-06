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

from concurrent.futures import ThreadPoolExecutor, wait
import threading

import models.db_initializer
from models.account import AccountData

DEFAULT_PASS = 'ASD123qwe'


def start_in_thread(acc: AccountData):
    rand_proxy = False
    while True:
        sleep(random.randint(0, 20)) # for more smooth start

        firebaseApi = FirebaseApi()
        panzerdogsApi = {}
        if acc.pd_username is None:
            username = credentials_generator.get_random_username()
            email = credentials_generator.generate_email(username)

            resp = firebaseApi.register_new_user(email, DEFAULT_PASS)
            if resp is None:
                logger.error(f'{acc.id}: Failed to register new user in firebase')
                continue
            
            proxy = ""
            if rand_proxy:
                proxy = proxies.get_random_in_requests_format()
            else: 
                proxy = proxies.convert_proxy_to_requests_format(acc.proxy)

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
                    acc.pd_password = DEFAULT_PASS
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

        for i in range(10):
            match_stats = MatchStats()
            logger.info(f"{acc.id}: Starting fight {i}...")

            resp = panzerdogsApi.get_matchmaking()
            if resp is None or resp.get("error"):
                logger.error(f"{acc.id}: Failed to get matchmaking")
                exit()

            room_id = resp["roomId"]
            logger.info(f"{acc.id}: Match started, match id: {room_id}")
            time.sleep(60)

            match_stats.update()
            resp = panzerdogsApi.ocs(match_stats)
            logger.info(f"{acc.id}: Ocs success: {resp['success']}")
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


def start():
    accs = list(AccountData.select())
    models.connector.connection.close()
    # for acc in accs:
        # if acc.id < 16 : continue # todo
        # x = threading.Thread(target=start_in_thread, args=(acc,))
        # logger.info(f'starting thread for acc {acc.id}')
        # x.start()
        # sleep(10)
    
    with ThreadPoolExecutor(max_workers=200) as executor:

        future = {executor.submit(start_in_thread, acc)
                    for acc in accs}
        wait(future)

        print('================')

    while True:
        pass


if __name__ == '__main__':
    start()
