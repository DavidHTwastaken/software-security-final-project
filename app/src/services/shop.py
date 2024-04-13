from app.src.db import DB

db = DB()

class Shop:
    @staticmethod
    def buy(username: str, id: int):
        product = db.get_product(id)
        balance = db.get_balance(username)

        if None == product:
            return "Product not found"

        value = float(product['price'])

        if value > balance:
            return "Insufficient funds"

        db.update_balance(username, value)
        db.add_inventory(username,id)

        if 5 == id:
            return "Congratulations, you solved the challenge"
        
        return ""

    @staticmethod
    def sell(username: str, id: int):
        product = db.get_product_from_inventory(username, id)
        balance = db.get_balance(username)

        if None == product:
            return "Product doesn't exist in inventory"
        
        value = float(product['price'])

        db.update_balance(username, value)
        db.remove_inventory(username,id)

        return ""