import ssl
import psycopg2


class Database:
    def __init__(self, dbname, user, password, host):
        self.conn = psycopg2.connect(dbname=dbname, user=user,
                                     password=password, host=host)
        self.cur = self.conn.cursor()

    def load(self, user_id):
        self.cur.execute(f"SELECT id FROM test_db WHERE user_id = {user_id}")

        return self.cur.fetchone()

    def add_new_user(self, user_id):
        self.cur.execute(f"INSERT INTO test_db(user_id) VALUES({user_id})")

        self.conn.commit()