import psycopg2


class PostreSQL:
    def __init__(self, db_uri):
        self.connection = psycopg2.connect(db_uri, sslmode='require')
        self.connection.autocommit = True

        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                user_id integer NOT NULL,
                message text);"""
        )

    def load(self, user_id):
        self.cursor.execute(
            f"SELECT id FROM users WHERE user_id = {user_id}"
        )

        return self.cursor.fetchone()

    def add_new_user(self, user_id, message):
        self.cursor.execute(
            f"INSERT INTO users(user_id, message) VALUES(%s, %s)", (user_id, message,)
        )

    def update_message(self, message, user_id):
        self.cursor.execute(
            f"UPDATE users SET message = '{message}' WHERE user_id = {user_id}"
        )

    def get_language(self, user_id):
        self.cursor.execute(
            f"SELECT id FROM users WHERE user_id = {user_id}"
        )

        return self.cursor.fetchone()