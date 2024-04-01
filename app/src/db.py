import psycopg2
import os


class DB:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(database="vulnerable",
                                     host=os.environ['DB_HOST'],
                                     user=os.environ['DB_USERNAME'],
                                     password=os.environ['DB_PASSWORD'])
        self.cur = self.conn.cursor()

    def seed(self):
        self.cur.exectute(open("../db.sql", "r").read())
        self.conn.commit()

    def get_users(self):
        self.cur.execute("SELECT * FROM users;")
        return self.cur.fetchall()

    def get_user(self, username, password):
        self.cur.execute("SELECT * FROM users"
                         "WHERE username=%s AND password=%s;",
                         (username, password))
        return self.cur.fetchall()

    def add_user(self, username, password):
        self.cur.execute("INSERT INTO users(username, password)"
                         "VALUES(%s, %s);", (username, password))
        self.conn.commit()

    def purchase(self, username, product):
        self.cur.execute("INSERT INTO user_products (username, product)"
                         "VALUES (%s, %s)"
                         "ON CONFLICT DO UPDATE "
                         "SET quantity = quantity + 1;",
                         (username, product))
        self.conn.commit()
