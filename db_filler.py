import models.db_initializer
from models.account import AccountData
from loguru import logger

CREATOR = 'Killto'
IS_REF = True

with open('accs_to_fill.txt', 'r') as f:
    for line in f:
        line = line.replace('\n', '')
        s = line.split('\t')

        AccountData.create(public_key=s[0],
                           private_key=s[1],
                           proxy=s[2],
                           creator=CREATOR,
                           is_referral=IS_REF)


logger.success('DONE')
