from peewee import *
from db import DB

db = DB()

class BaseModel(Model):
    class Meta:
        database = db