from .models import Inventory2, orm_db, Users, Products, Inventory, DatabaseError
from flask import session
import logging
from uuid import uuid4

log = logging.getLogger('app.shop')

'level one is doing it as is'

'level 2 -> disable selling but keep that endpoint open'

'level 3 -> lock val with atomicity'

class Shop:
    @staticmethod
    @orm_db.connection_context()
    def login(username: str, password: str):
        users_orm = Users.select().where(Users.username==username).execute()

        if 0 == len(users_orm):
            session_token = str(uuid4())
            try:
                Users.create(username=username,password=password,token=session_token,balance=200)
            except DatabaseError as e:
                log.debug(e)
                return None
            return session_token
        
        user = users_orm[0]
        if password != user.password:
            return None
        
        return user.token
    
    @staticmethod
    @orm_db.connection_context()
    def buy(session_token: str, id: int):
        try:
            product = Products.get(Products.product_id==id)
            user = Users.get(Users.token==session_token)
        except DatabaseError as e:
            log.debug(e)
            return "Oopsie, an error occured, check server logs"

        log.debug(f"product is {product} of type {type(product)}")
        log.debug(f"user is {user} of type {type(user)}")

        if user.balance < product.price:
            return "Insufficient funds"
        
        working_balance = user.balance - product.price

        try:
            Inventory.create(user_id=user.user_id, product_id=product.product_id, value=product.price, product_name=product.name)
            Users.update(balance=working_balance).where(Users.user_id==user.user_id).execute()
        except DatabaseError as e:
            log.debug(e)
            return "Oopsie, an error occured, check server logs"
        
        if product.name == "PS5":
            return "Congratulations, you have solved the race condition challenge"
        
        return ""
    
    @staticmethod
    @orm_db.connection_context()
    def sell(session_token: str, transaction_id: int):
        try:
            inventory_product = Inventory.get(Inventory.transaction_id == transaction_id)
            user = Users.get(session_token==Users.token)
        except DatabaseError as e:
            log.debug(e)
            return "Oopsie, an error occured, check server logs"

        new_balance = user.balance + inventory_product.value

        try:
            Inventory.delete().where(Inventory.transaction_id==inventory_product.transaction_id).execute()
            Users.update(balance=new_balance).where(Users.user_id==user.user_id).execute()
        except DatabaseError as e:
            log.info(e)
            return "Oopsie, an error occured, check server logs"        

        return ""

    @staticmethod
    @orm_db.connection_context()
    def get_user(session_token: str):
        users_orm = Users.select().where(session_token==Users.token)
        
        if 0 == len(users_orm):
            return False, 0, None, ""
        
        user = users_orm[0]
        inventory_orm = Inventory.select().where(Inventory.user_id==user.user_id)

        return True, user.balance, [_ for _ in inventory_orm], user.username
    
    @staticmethod
    @orm_db.connection_context()
    def buy2(session_token: str, id: int):
        try:
            product = Products.get(Products.product_id==id)
            user = Users.get(Users.token==session_token)
        except DatabaseError as e:
            log.debug(e)
            return "Oopsie, an error occured, check server logs"

        log.debug(f"product is {product} of type {type(product)}")
        log.debug(f"user is {user} of type {type(user)}")

        if user.balance < product.price:
            return "Insufficient funds"
        
        working_balance = user.balance - product.price

        try:
            Inventory2.create(user_id=user.user_id, product_id=product.product_id, value=product.price, product_name=product.name)
            Users.update(balance=working_balance).where(Users.user_id==user.user_id).execute()
        except DatabaseError as e:
            log.debug(e)
            return "Oopsie, an error occured, check server logs"
        
        return ""
    
    @staticmethod
    @orm_db.connection_context()
    def sell2(session_token: str, transaction_id: int):
        user = Users.get(session_token==Users.token)
        lock = str(uuid4())
        with orm_db.atomic() as transaction:
            try:
                isLocked = Inventory2.update(lock=lock).where(Inventory2.transaction_id==transaction_id).where(Inventory2.user_id==user.user_id).where(Inventory2.lock=="").execute()
                transaction.commit()
            except DatabaseError as e:
                transaction.rollback()
                log.debug(e)
                return "Oopsie, an error occured, check server logs"
            
        if 1 != isLocked:
            return "Lock can't be processed"
        
        try:
            inventory_product = Inventory2.get(Inventory2.transaction_id == transaction_id)
        except DatabaseError as e:
            log.debug(e)
            return "Oopsie, an error occured, check server logs"
        
        if lock != inventory_product.lock:
            return "Lock check failed"
        
        new_balance = user.balance + inventory_product.value

        try:
            Inventory2.delete().where(Inventory2.transaction_id==inventory_product.transaction_id).execute()
            Users.update(balance=new_balance).where(Users.user_id==user.user_id).execute()
        except DatabaseError as e:
            log.debug(e)
            return "Oopsie, an error occured, check server logs" 
        
        return ""
    
    @staticmethod
    @orm_db.connection_context()
    def get_user2(session_token: str):
        users_orm = Users.select().where(session_token==Users.token)
        
        if 0 == len(users_orm):
            return False, 0, None, ""
        
        user = users_orm[0]
        inventory_orm = Inventory2.select().where(Inventory2.user_id==user.user_id)

        return True, user.balance, [_ for _ in inventory_orm], user.username