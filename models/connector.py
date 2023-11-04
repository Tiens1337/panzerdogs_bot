import os
from peewee import *
import config

db_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', config.DB))
connection = SqliteDatabase(db_path)


class BaseModel(Model):
    @classmethod
    def safe_get(cls, *query, **filters):
        try:
            result = cls.get(*query, *filters)
            return True, result
        except Exception as e:
            print(e)
            return False, None

    class Meta:
        database = connection