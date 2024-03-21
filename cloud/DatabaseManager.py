import sqlite3
from User import User


class UsersDataBase:

    CREATE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );"""

    def __init__(self):
        self.db = Database()
        self.db.connect()
        self.create_table()

    def create_table(self):
        self.db.execute_query(self.CREATE_TABLE_QUERY)

    def add_user(self, user: User):
        query = "INSERT INTO users (username, password) VALUES (?, ?);"
        return self.db.execute_query(query, (user.username, user.password))

    def get_user(self, username):
        query = "SELECT * FROM users WHERE username = ?;"
        user_data = self.db.fetch_query(query, (username,))
        if user_data:
            user_data = user_data[0]
            return User(user_data[1], user_data[2])
        return None


class Database:

    DB_NAME = "rossCloud.db"

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        if not self.connection:
            self.connect()
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return False

    def fetch_query(self, query, params=None):
        if not self.connection:
            self.connect()
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error fetching data:", e)
            return None