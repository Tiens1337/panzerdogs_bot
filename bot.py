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
        if config.MAX_WORKERS > 10:
            sleep(random.randint(0, 20)) # for more smooth start

        firebaseApi = FirebaseApi()
        panzerdogsApi = {}

        proxy = ""
        if rand_proxy:
            proxy = proxies.get_random_in_requests_format()
        else: 
            proxy_str = proxies.parse_proxy_str(acc.proxy)
            proxy = proxies.convert_proxy_to_requests_format(proxy_str)

        if not acc.is_registred:
            username = credentials_generator.get_random_username()
            if acc.pd_email is None:
                email = credentials_generator.generate_email(username)
            else:
                email = acc.pd_email

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
            if resp is None or not resp["success"]:
                logger.error(f'{acc.id}: Failed to link wallet')
                rand_proxy = True
                continue

            while True:
                try:
                    acc.pd_username = username
                    acc.pd_email = email
                    acc.pd_password = config.DEFAULT_PASS
                    acc.is_registred = True
                    acc.save()
                    logger.success(f'{acc.id}: {email} registred')
                    break
                except Exception as e:
                    logger.error(f'{acc.id}: database is locked: {e}')
                    sleep(5)


        else:
            resp = firebaseApi.signup(acc.pd_email, acc.pd_password)
            if resp is None:
                logger.error(f'{acc.id}: Failed to sign up in firebase')
                rand_proxy = True
                continue
            panzerdogsApi = PanzerdogsApi(resp["idToken"], acc.proxy)
            logger.info(f'{acc.id}: signed in')

        while True:
            wallet_info = panzerdogsApi.check_wallet()
            if wallet_info is not None and wallet_info['success']:
                logger.info(f"{acc.id}: wallet already linked")
                break
        
            resp = panzerdogsApi.link_wallet(acc.public_key)
            if resp is None or not resp["success"]:
                logger.error(f'{acc.id}: Failed to link wallet')
                rand_proxy = True
                sleep(5)
            logger.info(f"{acc.id}: linked wallet {acc.public_key}")
            break
        
        if config.ONLY_LINK_WALLETS:
            return

        for i in range(5):
            match_stats = MatchStats()
            logger.info(f"{acc.id}: Starting fight {i}")

            resp = panzerdogsApi.get_matchmaking()
            if resp is None or resp.get("error"):
                logger.error(f"{acc.id}: Failed to get matchmaking")
                continue

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
    while True:
        accs = list(AccountData.select())
        models.connector.connection.close()
        
        with ThreadPoolExecutor(config.MAX_WORKERS) as executor:
            future = {executor.submit(start_in_thread, acc)
                        for acc in accs}
            wait(future)

        if config.ONLY_LINK_WALLETS:
            logger.success('ALL WALLETS HAS BEEN LINKED')
            break


if __name__ == '__main__':
    start()
