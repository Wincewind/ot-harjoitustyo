import sqlite3
from db_connection import get_database_connection
from config import AVAILABLE_CARDSETS

def drop_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        drop table if exists Users;
    """)
    cursor.execute("""
        drop table if exists UserCardSets;
    """)
    cursor.execute("""
        drop table if exists CardSets;
    """)

    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        create table Users (
            id integer primary key,
            name text,
            wins integer default 0,
            losses integer default 0,
            row_number integer
        );
    """)
    cursor.execute("""
        create table CardSets (
            id integer primary key,
            name text
        );
    """)
    cursor.execute("""
        create table UserCardSets (
            id integer primary key,
            user_id integer references Users(id) on delete cascade,
            cardset_id integer references CardSets(id) on delete cascade
        );
    """)
    for card_set in AVAILABLE_CARDSETS:
        cursor.execute("""
            insert into CardSets
            (name) values
            (?);
        """,(card_set,))
    connection.commit()

def init_db():
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)


if __name__=='__main__':
    #drop_tables(get_database_connection())
    init_db()
