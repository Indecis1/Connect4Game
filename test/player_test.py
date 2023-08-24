import json
import unittest

from src.player import Player
from src.const import SaveConst

class PlayerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.player1 = Player("Player 1", "red")
        self.player2 = Player("Player 2", "green")

    def tearDown(self) -> None:
        self.player1 = None
        self.player2 = None

    def test_save_one_player(self):
        data = {}
        errors: list[str] = []
        data = self.player1.save_to_json(data, errors)
        self.assertTrue(len(errors) == 0)
        self.assertEqual(data[SaveConst.PLAYER.value][self.player1.id], self.player1)

    def test_save_two_players(self):
        data = {}
        errors: list[str] = []
        data = self.player1.save_to_json(data, errors)
        data = self.player2.save_to_json(data, errors)
        self.assertTrue(len(errors) == 0)
        self.assertEqual(data[SaveConst.PLAYER.value][self.player1.id], self.player1)
        self.assertEqual(data[SaveConst.PLAYER.value][self.player2.id], self.player2)

    def test_load_one_player(self):
        data = {}
        errors: list[str] = []
        data = self.player1.save_to_json(data, errors)
        self.assertTrue(len(errors) == 0)
        json_str = json.dumps(data)
        json_dict = json.loads(json_str)
        players = Player.load_from_json(json_dict, errors)
        self.assertEqual(players[0], self.player1)

    def test_load_two_players(self):
        pass

if __name__ == '__main__':
    unittest.main()
