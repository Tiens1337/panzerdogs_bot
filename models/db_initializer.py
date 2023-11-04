from models.connector import connection
from models.account import AccountData

cursor = connection.cursor()

with connection:
    connection.create_tables([
        AccountData,
    ])