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

        cursor = self.connection.cursor()

        cursor.execute(sql, params)

        data = None

        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        if commit:
            self.connection.commit()

        return data

    def create_table_users(self):
        sql = "CREATE TABLE IF NOT EXISTS Users(id INT, full_name TEXT, video_code TEXT)"
        self.execute(sql, commit=True)

    def insert_data(self, params: tuple=None):
        sql = "INSERT INTO Users(id, full_name, video_code) VALUES (?, ?, ?)"
        self.execute()



