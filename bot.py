from loguru import logger
from time import sleep
import threading
import time
from firebase_api import FirebaseApi
from panzerdogs_api import PanzerdogsApi
import models.db_initializer
from models.account import AccountData
import credentials_generator


DEFAULT_PASS = 'ASD123qwe'


def start_in_thread(acc: AccountData):
    while True:
        sleep(15)

        firebaseApi = FirebaseApi()
        panzerdogsApi = {}
        if acc.pd_username is None:
            username = credentials_generator.get_random_username()
            email = credentials_generator.generate_email(username)

            resp = firebaseApi.register_new_user(email, DEFAULT_PASS)
            if resp is None:
                logger.error('Failed to register new user in firebase')
                continue

            panzerdogsApi = PanzerdogsApi(resp["idToken"])
            resp = panzerdogsApi.register(username)
            if resp is None:
                logger.error('Failed to register new user in game')
                continue

            resp = panzerdogsApi.set_recruit()
            if resp is None:
                logger.error('Failed to set recruit')
                continue

            resp = panzerdogsApi.link_wallet(acc.public_key)
            if resp is None:
                logger.error('Failed to link wallet')
                continue

            acc.wb_username = username
            acc.wb_email = email
            acc.wb_password = DEFAULT_PASS
            acc.save()

        else:
            resp = firebaseApi.signup(acc.pd_email, acc.pd_password)
            panzerdogsApi = PanzerdogsApi(resp["idToken"])

        for i in range(10):
            logger.info(f"Starting fight {i}...")

            resp = panzerdogsApi.get_matchmaking()
            if resp is None or resp.get("error"):
                logger.error("Failed to get matchmaking")
                exit()

            room_id = resp["roomId"]
            logger.info(f"Match started, match id: {room_id}")
            time.sleep(60)

            resp = panzerdogsApi.ocs()
            logger.info(f"Ocs success: {resp['success']}")
            time.sleep(60)

            resp = panzerdogsApi.match_end(room_id)
            logger.info(f"Match ended, success: {resp['success']}")
            time.sleep(10)

        logger.success("Job done!")


def start():
    accs = list(AccountData.select())
    models.connector.connection.close()
    for acc in accs:
        # if acc.id < 16 : continue # todo
        x = threading.Thread(target=start_in_thread, args=(acc,))
        logger.info(f'starting thread for acc {acc.id}')
        x.start()
        sleep(3000000)

    while True:
        pass


if __name__ == '__main__':
    start()
