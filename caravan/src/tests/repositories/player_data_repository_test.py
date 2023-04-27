import unittest
from init_db import init_db
from repositories.player_data_repository import player_data_repository, DataNotFoundException
from entities.player_data import PlayerData


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        init_db()
        player_data_repository.create_player_data('Teppo Tulppu',1)
        player_data_repository.create_player_data('Roope Ankka',2)
        player_data_repository.create_player_data('Pelle Peloton',3)

    def test_create_player_data(self):
        try:
            pl_data = player_data_repository.find_player_data('Aku Ankka')
        except DataNotFoundException as ex:
            self.assertEqual(str(ex), 'No data found for player name "Aku Ankka"')
        player_data_repository.create_player_data('Aku Ankka',0)
        pl_data = player_data_repository.find_player_data('Aku Ankka')

        self.assertEqual(pl_data.name, 'Aku Ankka')
        self.assertEqual((pl_data.wins,pl_data.losses,pl_data._row_number), (0,0,0))

    def test_find_all_names(self):
        self.assertEqual(set(player_data_repository.find_all_player_names().keys()),{1,2,3})
        init_db()
        self.assertEqual(player_data_repository.find_all_player_names(),{})

    def test_delete_player_data(self):
        player_data_repository.delete_player_data('Teppo Tulppu')
        self.assertEqual(set(player_data_repository.find_all_player_names().values()),{'Roope Ankka','Pelle Peloton'})

    #     self.assertEqual(len(users), 2)
    #     self.assertEqual(users[0].username, self.user_kalle.username)
    #     self.assertEqual(users[1].username, self.user_matti.username)

    # def test_find_by_username(self):
    #     user_repository.create(self.user_kalle)

    #     user = user_repository.find_by_username(self.user_kalle.username)

    #     self.assertEqual(user.username, self.user_kalle.username)