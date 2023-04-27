import sqlite3
from config import PATH_TO_PLAYER_DATA

connection = sqlite3.connect(PATH_TO_PLAYER_DATA)
connection.execute("PRAGMA foreign_keys=ON;")
connection.row_factory = sqlite3.Row


def get_database_connection():
    return connection
