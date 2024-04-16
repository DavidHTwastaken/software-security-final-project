import logging
from peewee import *
import datetime

log = logging.getLogger('app.models')
orm_db = SqliteDatabase('shop.db')

# class BaseModel(Model):
#     class Meta:
#         database = orm_db

class Users(Model):
    user_id = AutoField(primary_key=True)
    username = CharField(unique=True, max_length=50)
    password = CharField(max_length=100)
    balance = DecimalField(default=5)
    token = CharField()
    
    class Meta:
        database = orm_db

class Products(Model):
    product_id = AutoField(primary_key=True)
    name =CharField(unique=True, max_length=200)
    price = DecimalField(max_digits=19,decimal_places=2)
    
    class Meta:
        database = orm_db


class Inventory(Model):
    transaction_id = AutoField(primary_key=True)
    user_id = IntegerField()
    product_id = IntegerField()
    product_name = CharField(max_length=200)
    value = DecimalField()
    purchase_date = DateField(default=datetime.datetime.now())
    lock = CharField(default="")
    
    class Meta:
        database = orm_db

@orm_db.connection_context()
def create_db_schema(): 
    orm_db.create_tables([Users, Products, Inventory])
    products_list = [
        {'name':'Bananas', 'price':5.0},
        {'name':'Milk', 'price':10.0},
        {'name':'Lego Set', 'price':150.0},
        {'name':'Barbie', 'price':50.0},
        {'name':'PS5', 'price':500.0},
    ]

    for product in products_list:
        try:
            Products.create(name=product.get('name'),price=product.get('price'))
        except DatabaseError as e:
            log.info(e)

