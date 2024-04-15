from peewee import *
from db import DB

db = DB()

class PeeweeDB(PostgresqlDatabase):
    def __init__(self, db):
        self.db = db
        super().__init__('vulnerable')

    def get_conn(self):
        return self.db.connection

orm_db = PeeweeDB(db)

class BaseModel(Model):
    class Meta:
        database = orm_db

class Users(BaseModel):
    user_id = AutoField(primary_key=True)
    username = CharField(unique=True, max_length=50)
    password = CharField(max_length=100)
    balance = DecimalField(default=20.0)

    class Meta:
        table_name = 'users'

class Products(BaseModel):
    user_id = AutoField(primary_key=True)
    class Meta:
        table_name = 'products'

class Inventory(BaseModel):

    class Meta:
        table_name = 'inventory'