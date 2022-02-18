import psycopg2


class PostreSQL:
    def __init__(self, host, user, password, db_name):
        self.connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name
        )
        self.connection.autocommit = True

        self.cursor = self.connection.cursor()
        self.cursor.executor(
            """CREATE TABLE IF NOT EXIST users(
                id serial PRIMARY KEY,
                user_id intager NOT NULL);"""
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