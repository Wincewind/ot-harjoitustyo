"""Module for initiating connection to the caravan game's player data db.
"""
import sqlite3
from config import PATH_TO_PLAYER_DATA

connection = sqlite3.connect(PATH_TO_PLAYER_DATA)
connection.execute("PRAGMA foreign_keys=ON;")
connection.row_factory = sqlite3.Row


def get_database_connection():
    """Get the iniated player data db connection.

    Returns:
        sqlite3.Connection: Connection object.
    """
    return connection
