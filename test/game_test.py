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
        self.game = Game(players = players, play_order= play_order)

    def tearDown(self) -> None:
        self.game = None

    def test_save(self):
        pass

    def test_load(self):
        pass


if __name__ == '__main__':
    unittest.main()
