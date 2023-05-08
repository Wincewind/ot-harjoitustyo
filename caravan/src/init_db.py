from db_connection import get_database_connection
from config import AVAILABLE_CARDSETS


def drop_tables(connection):
    """Drop the Users, UserCardSets and CardSets tables.
    """
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
    """Create Users, CardSets and UserCardSets tables into the db.
    """
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
        """, (card_set,))
    connection.commit()


def init_db():
    """Drop the db's previous tables and create new ones.
    """
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)


if __name__ == '__main__':
    init_db()
