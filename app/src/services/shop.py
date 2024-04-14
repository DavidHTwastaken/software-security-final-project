from db import DB
from flask import session
import logging

log = logging.getLogger('app.shop')

db = DB()


class Shop:
    @staticmethod
    def buy(username: str, id: int):
        try:
            log.info(f"The id is {id} of type {type(id)}")
            product = db.get_product(id)
            balance = db.get_balance(username)
            balance = float(balance['balance'])

            if None == product:
                return "Product not found"

            value = float(product['price'])

            if value > balance:
                return "Insufficient funds"

            balance = balance - value

            db.update_balance(username, balance)
            db.add_to_inventory(username,id)
            session['balance'] = balance
            log.info(f"The current balance is {balance}")

            if 5 == int(id):
                return "Congratulations, you solved the challenge"
            
            return ""
        except Exception as e:
            return e

    @staticmethod
    def sell(username: str, id: int):
        try:
            product_inventory = db.get_product_from_inventory(username, id)

            if None == product_inventory:
                return "Product doesn't exist in inventory"
            
            product = db.get_product(product_inventory['product_id'])
            value = float(product['price'])
            balance = db.get_balance(username).get('balance')
            balance = float(balance)
            balance = balance + value
            db.update_balance(username, balance)
            db.remove_from_inventory(username,id)
            
            balance = db.get_balance(username)
            session['balance'] = float(balance.get('balance'))
            log.info(f"The current balance is {balance}")

            return ""
        except Exception as e:
            return e
