import psycopg2
import os


class DB:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(database="vulnerable",
                                     host=os.environ['DB_HOST'],
                                     user=os.environ['DB_USERNAME'],
                                     password=os.environ['DB_PASSWORD'])
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        self.seed()

    def seed(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        seed_path = os.path.join(file_dir, "db.sql")
        self.cur.execute(open(seed_path, "r").read())
        self.conn.commit()

    def get_users(self):
        self.cur.execute("SELECT * FROM users;")
        return self.cur.fetchall()

    def get_user(self, username, password):
        self.cur.execute("SELECT * FROM users "
                         "WHERE username=%s AND password=%s;",
                         (username, password))
        return self.cur.fetchall()

    def add_user(self, username, password) -> tuple | None:
        self.cur.execute("INSERT INTO users(username, password) "
                         "VALUES(%s, %s) RETURNING user_id;", (username, password))
        self.conn.commit()
        return self.cur.fetchone()

    def purchase(self, username, product):
        self.cur.execute("INSERT INTO user_products (username, product) "
                         "VALUES (%s, %s) "
                         "ON CONFLICT DO UPDATE "
                         "SET quantity = quantity + 1;",
                         (username, product))
        self.conn.commit()

    def get_product(self, id: int) -> list[dict[any, any]]:
        self.cur.execute("SELECT * FROM products "
                         "WHERE product_id=%d"
                        ,(id))
        
        self.conn.commit()
        return self.cur.fetchone()
    
    def get_balance(self, username: str) -> list[dict[any, any]]:
        self.cur.execute("SELECT balance FROM users "
                         "WHERE username=%s"
                        ,(username))
        
        self.conn.commit()
        return self.cur.fetchone()
    
    def update_balance(self, username: str, value: float) -> list[dict[any, any]]:
        self.cur.execute("UPDATE users "
                         "SET balance = balance + %f "
                         "WHERE username=%s "
                        ,(value, username))
        
        self.conn.commit()
    
    def add_to_inventory(self, username: str, id: int) -> list[dict[any, any]]:
        self.cur.execute("INSERT INTO inventory (product_id, user_id) "
                         "VALUES (%d, (SELECT LIMIT 1 user_id FROM users WHERE username=%s)) "
                        ,(id, username))

        self.conn.commit()
    
    def remove_from_inventory(self, username: str, id: int) -> list[dict[any, any]]:
        self.cur.execute("DELETE FROM inventory "
                         "WHERE product_id=%d AND (SELECT LIMIT 1 user_id FROM users WHERE username=%s) "
                        ,(id, username))

        self.conn.commit()