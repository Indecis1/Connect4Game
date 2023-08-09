import unittest
import numpy as np

from src.board import Board
from src.player import Player
from src.util import Rect

class BoardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()
        Player.POSSIBLE_IDS = list(range(1, 10))
        self.player1 = Player("Player 1", "red")
        self.player2 = Player("Player 2", "green")

    def tearDown(self) -> None:
        self.board = None
        self.player1 = None
        self.player2 = None

    def test_add_one_token(self):
        board = np.zeros((6, 7), dtype= int)
        board[0, 6] = self.player1.id
        self.board.add_token(6, self.player1)
        self.assertTrue(np.equal(self.board.board, board, dtype=object).all())

    def test_add_multiple_token(self):
        board = np.zeros((6, 7), dtype= int)
        board[0,6] = self.player1.id
        board[0,5] = self.player2.id
        board[1,6] = self.player1.id
        board[0,3] = self.player2.id
        board[0,4] = self.player1.id
        self.board.add_token(6, self.player1)
        self.board.add_token(5, self.player2)
        self.board.add_token(6, self.player1)
        self.board.add_token(3, self.player2)
        self.board.add_token(4, self.player1)
        self.assertTrue(np.equal(self.board.board, board, dtype=object).all())


    def test_game_vertical_won(self):
        self.board.add_token(6, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(5, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(6, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(5, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(6, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(5, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(6, self.player1)
        result = self.board.check_game_state([self.player1, self.player2])
        self.assertTrue(result[0])
        print(result[1])
        self.assertEqual(result[1], Rect(3, 6, 0, 6))

    def test_game_horizontal_won(self):
        self.board.add_token(6, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(6, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(5, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(5, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(4, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(4, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(3, self.player1)
        result = self.board.check_game_state([self.player1, self.player2])
        self.assertTrue(result[0])
        self.assertEqual(result[1], Rect(0, 3, 0, 6))

    def test_game_diagonal_won(self):
        self.board.add_token(6, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(5, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(5, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(3, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(4, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(4, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(4, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(2, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(3, self.player1)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(3, self.player2)
        self.assertFalse(self.board.check_game_state([self.player1, self.player2])[0])
        self.board.add_token(3, self.player1)
        result = self.board.check_game_state([self.player1, self.player2])
        self.assertTrue(result[0])
        self.assertEqual(result[1], Rect(3, 3, 0, 6))

if __name__ == '__main__':
    unittest.main()
