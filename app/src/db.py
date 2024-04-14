import psycopg2
import os


class DB:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(database="vulnerable",
                                     host=os.environ['DB_HOST'],
                                     user=os.environ['DB_USERNAME'],
                                     password=os.environ['DB_PASSWORD'])
        self.cur = self.conn.cursor()
        self.seed()

    def seed(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        seed_path = os.path.join(file_dir, "db.sql")
        self.cur.execute(open(seed_path, "r").read())
        self.conn.commit()

    def get_users(self):
        self.cur.execute("SELECT * FROM users;")
        return self.cur.fetchall()

    def get_user(self, username):
        self.cur.execute("SELECT * FROM users "
                         "WHERE username=%s;",
                         (username,))
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
