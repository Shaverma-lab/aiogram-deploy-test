import ssl
import psycopg2


class Database:
    def __init__(self, db_uri):
        self.conn = psycopg2.connect(db_uri, sslmode='require')
        self.cur = self.conn.cursor()

    def load(self, user_id):
        self.cur.execute(f"""
            SELECT id FROM test_db WHERE user_id = {user_id}
        """)

        return self.cur.fetchone()

    def add_new_user(self, user_id):
        self.cur.execute(f"""
            INSERT INTO test_db(user_id) VALUES(%s);
        """, (user_id))

        self.conn.commit()