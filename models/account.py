from peewee import *
from models.connector import BaseModel


class AccountData(BaseModel):
    public_key = TextField(unique=True)
    private_key = TextField(unique=True)

    creator = TextField(null=True)

    pd_username = TextField(unique=True, null=True)
    pd_email = TextField(unique=True, null=True)
    pd_password = TextField(null=True)

    proxy = TextField(null=False)
