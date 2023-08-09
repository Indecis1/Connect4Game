# -*- coding: utf-8 -*-

import json
import numpy as np
from numpy.lib.stride_tricks import as_strided

from src.IStorable import IStorable
from src.util import Rect
from src.player import Player
from src.token_2 import Token
from src.const import GameState as GameState

class Board(IStorable):
    """
    Represent the game's board
    """
    def __init__(self):
        self._calculus_board = np.zeros((6, 7), dtype= int)
        self.board = np.array([[None] * 7] * 6, dtype= object)
        self._vertical_filters = np.zeros((1, 4, 4), dtype= int)
        self._horizontal_filters = np.zeros((1, 4, 4), dtype= int)
        self._diagonal_filters = np.zeros((2, 4, 4), dtype= int)
        self._filters = np.array([[]], dtype= int)
        self.__init_filter()

    def __init_filter(self) -> None:
        """
        Init the filter use to find if a player win
        :return:
        """
        for i in range(4):
            vertical_filter = np.zeros((1, 4, 4), dtype= int)
            vertical_filter[:, :, i] = np.ones(4, dtype= int)
            self._vertical_filters = np.append(self._vertical_filters, vertical_filter, axis=0)

            horizontal_filter = np.zeros((1, 4, 4), dtype= int)
            horizontal_filter[:, i, :] = np.ones(4, dtype= int)
            self._horizontal_filters= np.append(self._horizontal_filters, horizontal_filter, axis=0)
            if i == 0:
                self._vertical_filters = np.delete(self._vertical_filters, 0, axis=0)
                self._horizontal_filters = np.delete(self._horizontal_filters, 0, axis=0)

        diagonal_filter = np.eye(4, 4, 0).reshape(1, 4, 4)
        self._diagonal_filters = np.append(self._diagonal_filters, diagonal_filter, axis=0)
        self._diagonal_filters = np.append(self._diagonal_filters, diagonal_filter[:, :, ::-1], axis=0)
        self._filters = np.stack((self._vertical_filters, self._horizontal_filters, self._diagonal_filters), axis=0)

    def __could_add_token_to_column(self, column_position: int) -> bool:
        """
        Check if we could add a token to the colum
        :param column_position: The position of the column in the board where we want to add a token
        :return: if we can or cannot add a new token to this column
        """
        column = self.board[:, column_position]
        if column[0] is None:
            return True
        return False

    def __position_to_add_token(self, column_position: int) -> int:
        """
        Find the position to add a new token to a column if any
        :param column_position: The position of the column in the board where we want to add a token
        :return: The position where we should place the token if any otherwise return -1
        """
        column = self.board[:, column_position]
        empty_positions = np.where(column == None)[0]
        if empty_positions.size == 0:
            return -1
        return max(empty_positions)

    def add_token(self, column_position: int, player: Player) -> bool:
        """
        Add a new token to column [0-6]
        :param column_position: The position of the column in the board where we want to add a token
        :param player: The player who want to add a token
        :return: a bool that represent if we had add a token or not
        """
        position_to_add = self.__position_to_add_token(column_position)
        if position_to_add < 0:
            # The column is full we can't add the token
            return False
        token = Token(player)
        self.board[position_to_add, column_position] = token
        self._calculus_board[position_to_add, column_position] = player.id
        return True

    def _calculus_board_of_player(self, player_id: int) -> np.ndarray :
        return np.where(self._calculus_board == player_id, 1, 0)

    def check_game_state_for_player(self, player: Player) -> tuple[GameState, Rect]:
        """
        Check if a player won the game
        :param player: The player we want to check the state
        :return: a number representing the state of the game, the top left and bottom right corner of the winning position
        """
        player_calculus_board = self._calculus_board_of_player(player.id)
        board_strides = player_calculus_board.strides * 2
        views: np.ndarray = as_strided(player_calculus_board, shape=(3, 4, 4, 4), strides=board_strides)
        for i in range(views.shape[0]):
            for j in range(views.shape[1]):
                filter_sum = np.sum(self._filters * views[i, j, :, :], axis=(2, 3))
                winning_filter_position = np.where(filter_sum == 4)
                if winning_filter_position[0].size != 0:
                    rbc_winning_position = np.where(self._filters[winning_filter_position[0][0], winning_filter_position[1][0], :, :] == 1)
                    win_board_position = Rect(top=i + rbc_winning_position[0][0], left=j + rbc_winning_position[1][0], bottom=i + 3, right=j + rbc_winning_position[1][rbc_winning_position[1].size - 1])
                    return GameState.PLAYER_WIN, win_board_position
        if np.where(self.board == None)[0].size == 0:
            return GameState.DRAW, Rect(-1, -1, -1, -1)
        return GameState.NOT_FINISH, Rect(-1, -1, -1, -1)

    def check_game_state(self, players: list[Player]) -> tuple[bool, Rect]:
        for player in players:
            player_state = self.check_game_state_for_player(player)
            if player_state[0] != GameState.NOT_FINISH:
                return True, player_state[1]
        return False, Rect(-1 , -1, -1 , -1)

    @staticmethod
    def load_from_json(data: dict, errors: list[str]) -> list[IStorable]:
        board_obj = data.get("board", None)
        if board_obj is None:
            errors.append("Board key not found in the saved game")
            return []
        board = Board()
        pass

    def save_to_json(self, data_to_saved: dict, errors: list[str]) -> dict:
        pass

    def calculus_board_to_str(self, player_id: int):
        board_str = ""
        board = self._calculus_board(player_id)
        for i in range(board.shape[0]):
            board_str += "|".join(["X" if board[i, :] == 1 else " "]) + "\n"
            board_str += "-"* (2 * board.shape[1] - 1) + "\n"
        return board_str

    def board_to_str(self):
        board_str = ""
        board = self.board
        for i in range(board.shape[0]):
            for elt in board[i, :]:
                if elt is None:
                    board_str += "|" + " "
                else:
                    board_str += "|" + elt.token_to_str()
            board_str += "\n"
            board_str += "-"* (2 * board.shape[1] - 1) + "\n"
        return board_str


