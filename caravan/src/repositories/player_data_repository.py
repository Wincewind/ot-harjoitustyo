from db_connection import get_database_connection
from entities.player_data import PlayerData

class DataNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PlayerDataRepository:
    def __init__(self, connection) -> None:
        self.name = ''
        self.wins = 0
        self.losses = 0
        self.card_sets = []
        self._connection = connection

    def find_player_data(self,name):
        cursor = self._connection.cursor()
        cursor.execute("""
            select Users.name, wins, losses, row_number, CardSets.name as cs_name
            from Users
            left join UserCardSets on UserCardSets.user_id = Users.id
            left join CardSets on UserCardSets.cardset_id = CardSets.id
            where Users.name = ?;
        """,(name,))
        data = cursor.fetchall()
        if len(data) == 0:
            raise DataNotFoundException(f'No data found for player name "{name}"')
        card_sets = [d['cs_name'] for d in data]
        return PlayerData(data[0]['name'],data[0]['wins'],data[0]['losses'],data[0]['row_number'],card_sets)
    
    def find_all_player_names(self):
        cursor = self._connection.cursor()
        cursor.execute("""
            select name, row_number
            from Users;
        """)
        return {c['row_number']:c['name'] for c in cursor.fetchall()}
    
    def create_player_data(self,name,row_num):
        cursor = self._connection.cursor()
        cursor.execute("""
            insert into Users
            (name,row_number) values
            (?,?);
        """,(name,row_num))
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
        """,(new_player_id,set_id['id']))

        self._connection.commit()

    def delete_player_data(self,name):
        cursor = self._connection.cursor()
        cursor.execute("""
            delete from Users
            where name=?;
        """,(name,))
        self._connection.commit()

player_data_repository = PlayerDataRepository(get_database_connection())
