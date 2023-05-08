from db_connection import get_database_connection
from entities.player_data import PlayerData


class DataNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PlayerDataRepository:
    """Repository for player save data. Handles the communications with sqlite db. 

    Attributes:
        name: Name of the player.
        wins: Number of wins.
        losses: Number of losses.
        card_sets: Card sets available to the player.
        _connection: db connection.
    """
    def __init__(self, connection) -> None:
        self.name = ''
        self.wins = 0
        self.losses = 0
        self.card_sets = []
        self._connection = connection

    def find_player_data(self, name, row_num):
        """Find a player's data based on their name and save slot row number.
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            select Users.name, wins, losses, row_number, CardSets.name as cs_name
            from Users
            left join UserCardSets on UserCardSets.user_id = Users.id
            left join CardSets on UserCardSets.cardset_id = CardSets.id
            where Users.name = ? and row_number=?;
        """, (name,row_num))
        data = cursor.fetchall()
        if len(data) == 0:
            raise DataNotFoundException(
                f'No data found for player name "{name}"')
        card_sets = [d['cs_name'] for d in data]
        return PlayerData(data[0]['name'], data[0]['wins'],
                          data[0]['losses'], data[0]['row_number'], card_sets)

    def find_all_player_names(self):
        """Find all available player names, row numbers, wins and losses in the db.
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            select name, row_number, wins, losses
            from Users;
        """)

        return {c['row_number']: {'name': c['name'], 'wins': c['wins'],
                                  'losses': c['losses']} for c in cursor.fetchall()}

    def create_player_data(self, name, row_num):
        "Create player data using a name and a row number to associate with it."
        cursor = self._connection.cursor()
        cursor.execute("""
            insert into Users
            (name,row_number) values
            (?,?);
        """, (name, row_num))
        new_player_id = cursor.lastrowid

        cursor.execute("""
            select id
            from Cardsets;
        """)
        card_set_ids = cursor.fetchall()
        for set_id in card_set_ids:
            cursor.execute("""
            insert into UserCardSets
            (user_id,cardset_id) values
            (?,?);
        """, (new_player_id, set_id['id']))

        self._connection.commit()

    def delete_player_data(self, name, row_num):
        """Delete player data with specific name and row number.
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            delete from Users
            where name=? and row_number=?;
        """, (name,row_num))
        self._connection.commit()

    def increment_player_wins(self, name, row_num):
        """Increment player data wins with specific name and row number.
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            update Users set wins = wins + 1
            where name=? and row_number=?;
        """, (name,row_num))
        self._connection.commit()

    def increment_player_losses(self, name, row_num):
        """Increment player data losses with specific name and row number.
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            update Users set losses = losses + 1
            where name=? and row_number=?;
        """, (name,row_num))
        self._connection.commit()


player_data_repository = PlayerDataRepository(get_database_connection())
