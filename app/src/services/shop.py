from db import DB

db = DB()

class Shop:
    @staticmethod
    def buy(username: str, id: int):
    
        product = db.get_product(id)
        balance = db.get_balance(username)
        balance = float(balance['balance'])

        if None == product:
            return "Product not found"

        value = float(product['price'])

        if value > balance:
            return "Insufficient funds"

        db.update_balance(username, -1*value)
        db.add_to_inventory(username,id)

        if 5 == id:
            return "Congratulations, you solved the challenge"
        
        return ""

    @staticmethod
    def sell(username: str, id: int):
        product_inventory = db.get_product_from_inventory(username, id)
        balance = db.get_balance(username)
        balance = float(balance['balance'])

        if None == product_inventory:
            return "Product doesn't exist in inventory"
        
        product = db.get_product(id)
        value = float(product['price'])

        db.update_balance(username, value)
        db.remove_from_inventory(username,id)

        return ""