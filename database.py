import psycopg2


class PostreSQL:
    def __init__(self, db_uri):
        self.connection = psycopg2.connect(db_uri, sslmode='require')
        self.connection.autocommit = True

        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                user_id integer NOT NULL);"""
        )

    def load(self, user_id):
        self.cursor.execute(
            f"SELECT id FROM users WHERE user_id = {user_id}"
        )

        return self.cursor.fetchone()

    def add_new_user(self, user_id):
        self.cursor.execute(
            f"INSERT INTO users(user_id) VALUES(%s)", (user_id,)
        )