import psycopg2
from db import DB
from flask import session
import logging

log = logging.getLogger('app.shop')

db = DB()


class Shop:
    @staticmethod
    def buy(username: str, id: int):
        try:
            product = {}
            balance = {}

            try:
                product = db.get_product(id)
                balance = db.get_balance(username)
            except psycopg2.DatabaseError as e:
                log.info(e)
                return "Oopsie, an error occured, check server logs"
            
            working_balance = float(balance.get('balance'))

            if None == product:
                return "Product not found"

            value = float(product.get('price'))

            if value > balance:
                return "Insufficient funds"

            working_balance = working_balance - value

            try:
                db.update_balance(username, working_balance)
                db.add_to_inventory(username,id)

            except psycopg2.DatabaseError as e:
                log.info(e)
                return "Oopsie, an error occured, check server logs"
            
           
            session['balance'] = working_balance
            log.info(f"The current balance is {balance}")

            if 5 == int(id):
                return "Congratulations, you solved the challenge"
            
            return ""
        except Exception as e:
            log.info(e)
            return "Oopsie, an error occured, check server logs"

    @staticmethod
    def sell(username: str, transaction_id: int, product_id: int):
        try:
            product_inventory = [{}]
            product = {}
            balance = {}

            try:
                product_inventory = db.get_product_from_inventory(username, transaction_id)
                product = db.get_product(product_id)
                balance = db.get_balance(username)
            except psycopg2.DatabaseError as e:
                log.info(e)
                return "Oopsie, an error occured, check server logs"
            
            if None == product_inventory:
                return "Product doesn't exist in inventory"
            
            
            log.info(f'the product info is {product}')
            value = float(product.get('price'))
            log.info(f'the value is {value} of type {type(value)}')
            working_balance = float(balance.get('balance'))
            
            working_balance = working_balance + value

            new_balance = {}
            try:
                db.update_balance(username, working_balance)
                db.remove_from_inventory(username,transaction_id)
                new_balance = db.get_balance(username)

            except psycopg2.DatabaseError as e:
                log.info(e)
                return "Oopsie, an error occured, check server logs"
            
            updated_working_balance = float(new_balance.get('balance'))
            session['balance'] = updated_working_balance
            log.info(f"The current balance is {updated_working_balance}")

            return ""
        
        except Exception as e:
            log.info(e)
            return "Oopsie, an error occured, check server logs"
