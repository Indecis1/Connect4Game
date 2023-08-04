import unittest
import numpy as np

from src.board import Board
from src.player import Player
from src.util import Rect
from src.token import Token


class BoardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.player1 = Player("Player 1", "red")
        self.player2 = Player("Player 2", "green")

    def tearDown(self) -> None:
        self.board = None
        self.player1 = None
        self.player2 = None

    def test_add_one_token(self):
        board = np.array([[None] * 7] * 6, dtype= object)
        board[5, 6] = Token(self.player1)
        self.board.add_token(6, self.player1)
        self.assertTrue(np.equal(self.board.board, board, dtype=object).all())

    def test_add_multiple_token(self):
        board = np.array([[None] * 7] * 6, dtype= object)
        board[5,6] = Token(self.player1)
        board[5,5] = Token(self.player2)
        board[4,6] = Token(self.player1)
        board[5,3] = Token(self.player2)
        board[5,4] = Token(self.player1)
        self.board.add_token(6, self.player1)
        self.board.add_token(5, self.player2)
        self.board.add_token(6, self.player1)
        self.board.add_token(3, self.player2)
        self.board.add_token(4, self.player1)
        self.assertTrue(np.equal(self.board.board, board, dtype=object).all())


    def test_game_won(self):
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
        print(result[1])
        self.assertTrue(result[0])
        self.assertEqual(result[1], Rect(2, 6, 5, 6))

if __name__ == '__main__':
    unittest.main()
