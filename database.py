import sqlite3 as sq


class Users:
    def __init__(self, path_to_db="user.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sq.connect(self.path_to_db)

    def execute(self, sql: str, params: tuple = None, fetchone: bool = False,
                fetchall: bool = False, commit: bool = False):
        if not params:
            params = tuple()
        connection = self.connection
        cursor = connection.cursor()

        cursor.execute(sql, params)

        data = None

        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        if commit:
            connection.commit()

        return data

    def create_table_users(self):
        sql = "CREATE TABLE IF NOT EXISTS Users(id INT, full_name TEXT, username TEXT)"
        self.execute(sql, commit=True)

    def insert_data(self, params: tuple):
        sql = "INSERT INTO Users(id, full_name, username) VALUES (?, ?, ?)"
        self.execute(sql, params=params, commit=True)

    def check_user(self, id):
        sql = "SELECT * FROM Users WHERE id=?"
        result = self.execute(sql, params=(id,), fetchone=True)
        return result

    def get_all_users(self):
        sql = "SELECT * FROM Users"
        users = self.execute(sql, fetchall=True)

        user_data = ""
        for user in users:
            user_data += f"ID: {user[0]}\nFull Name: {user[1]}\nUsername:{user[2]}\n\n\n"

        # file_path = 'users.txt'
        # with open(file_path, 'w') as file:
        #     file.write(user_data)

        return user_data



