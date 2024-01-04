import json
import os
import tempfile
import unittest

from src.game import Game
from src.player import Player


class GameTest(unittest.TestCase):

    def setUp(self) -> None:
        players = {}
        play_order = []
        player = Player("Player 1", "red")
        players[player.id] = player
        play_order.append(player.id)
        player = Player("Player 2", "green")
        players[player.id] = player
        play_order.append(player.id)
        self.game = Game(players=players, play_order=play_order)

    def tearDown(self) -> None:
        self.game = None

    def test_save(self):
        errors: list[str] = []
        data = {}
        self.game.save_to_json(data, errors)
        self.assertTrue(len(errors) == 0)
        json_str = json.dumps(data)
        json_dict = json.loads(json_str)
        game = Game.load_from_json(json_dict, errors)[0]
        self.assertTrue(len(errors) == 0)
        self.assertEqual(self.game, game)


if __name__ == '__main__':
    unittest.main()
