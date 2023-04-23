# -*- coding: utf-8 -*-

import numpy as np

from src.Player import Player
from src.Token import Token

class Board:
    """
    Represent the game's board
    """
    def __init__(self):
        self._calculus_board = np.zeros((6, 7), dtype= int)
        self.board = np.array([[None] * 7] * 6, dtype= object)
        self._vertical_filters = []
        self._horizontal_filters = []
        self._diagonal_filters = []
        self._filters = []
        self.__init_filter()
    def __init_filter(self) -> None:
        """
        Init the filter use to find if a player win
        :return:
        """
        for i in range(7):
            vertical_filter = np.zeros((6, 7), dtype= int)
            vertical_filter[:,i] = np.ones(6)
            self._vertical_filters.append(vertical_filter)
        for i in range(6):
            horizontal_filter = np.zeros((6, 7), dtype= int)
            horizontal_filter[i, :] = np.ones(7)
            self._horizontal_filters.append(horizontal_filter)

            if i != 6:
                diagonal_filter = np.eye(6, 7, i)
                self._diagonal_filters.append(diagonal_filter)
            diagonal_filter = np.eye(6, 7, -i)
            self._diagonal_filters.append(diagonal_filter)
        self._filters.extend(self._vertical_filters)
        self._filters.extend(self._horizontal_filters)
        self._filters.extend(self._diagonal_filters)
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
    def add_token(self, column_position, player: Player) -> bool:
        """
        Add a new token to column
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
    def calculus_board_of_player(self, player: Player):
        return np.where(self._calculus_board == player.id, 1, 0)
    def check_game_state(self, player: Player) -> tuple[int, np.ndarray]:
        """
        Check if a player won the game
        :param player: The player for whom we want to check if he won
        :return: a number representing the state of the game and the filter use to find the winning position if any
        """
        if np.where(self.board == None)[0].size == 0:
            # A draw we couldn't add any more token
            return 0, None
        player_board = self._calculus_board(player)
        for _filter in self._filters:
            filter_token = np.sum(np.multiply(_filter, player_board))
            if filter_token >= 4:
                return 1, _filter
        return -1, None
