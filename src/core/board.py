# -*- coding: utf-8 -*-
from __future__ import annotations
import numpy as np
from numpy.lib.stride_tricks import as_strided

from src.core.IStorable import IStorable
from src.core.util import Rect
from src.core.player import Player
from src.core.const import GameState, SaveConst


class Board(IStorable):
    """
    Represent the game's board
    """

    def __init__(self):
        self._column_height = np.zeros(7, dtype=int)
        self._history = []
        self.board = np.zeros((6, 7), dtype=int)
        self._vertical_filters = np.zeros((1, 4, 4), dtype=int)
        self._horizontal_filters = np.zeros((1, 4, 4), dtype=int)
        self._diagonal_filters = np.zeros((2, 4, 4), dtype=int)
        self._filters = np.array([[]], dtype=int)
        self.__init_filter()

    def __init_filter(self) -> None:
        """
        Init the filter use to find if a player win
        :return:
        """
        for i in range(4):
            vertical_filter = np.zeros((1, 4, 4), dtype=int)
            vertical_filter[:, :, i] = np.ones(4, dtype=int)
            self._vertical_filters = np.append(self._vertical_filters, vertical_filter, axis=0)

            horizontal_filter = np.zeros((1, 4, 4), dtype=int)
            horizontal_filter[:, i, :] = np.ones(4, dtype=int)
            self._horizontal_filters = np.append(self._horizontal_filters, horizontal_filter, axis=0)
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
        return self._column_height[column_position] < 6

    def __position_to_add_token(self, column_position: int) -> int:
        """
        Find the position to add a new token to a column if any
        :param column_position: The position of the column in the board where we want to add a token
        :return: The position where we should place the token if any otherwise return -1
        """
        return self._column_height[column_position]

    def add_token(self, column_position: int, player_id: int) -> bool:
        """
        Add a new token to column [0-6]
        :param column_position: The position of the column in the board where we want to add a token
        :param player_id: id of the player who want to add a token
        :return: a bool that represent if we had add a token or not
        """
        if not self.__could_add_token_to_column(column_position):
            return False
        position_to_add = self.__position_to_add_token(column_position)
        self.board[position_to_add, column_position] = player_id
        self._column_height[column_position] += 1
        self._history.append(column_position)
        return True

    def _calculus_board_of_player(self, player_id: int) -> np.ndarray:
        return np.where(self.board == player_id, 1, 0)

    def check_game_state_for_player(self, player: Player) -> tuple[GameState, Rect]:
        """
        Check if a player won the game :param player: The player we want to check the state :return: a number
        representing the state of the game, the top left and bottom right corner of the winning position
        """
        player_calculus_board = self._calculus_board_of_player(player.id)
        board_strides = player_calculus_board.strides * 2
        views: np.ndarray = as_strided(player_calculus_board, shape=(3, 4, 4, 4), strides=board_strides)
        for i in range(views.shape[0]):
            for j in range(views.shape[1]):
                filter_sum = np.sum(self._filters * views[i, j, :, :], axis=(2, 3))
                winning_filter_position = np.where(filter_sum == 4)
                if winning_filter_position[0].size != 0:
                    rbc_winning_position = np.where(
                        self._filters[winning_filter_position[0][0], winning_filter_position[1][0], :, :] == 1)
                    win_board_position = Rect(top=i + max(rbc_winning_position[0]),
                                              left=j + min(rbc_winning_position[1]),
                                              bottom=i + min(rbc_winning_position[0]),
                                              right=j + max(rbc_winning_position[1]))
                    return GameState.PLAYER_WIN, win_board_position
        if np.where(self.board == 0)[0].size == 0:
            return GameState.DRAW, Rect(-1, -1, -1, -1)
        return GameState.NOT_FINISH, Rect(-1, -1, -1, -1)

    def check_game_state(self, players: list[Player]) -> tuple[bool, Rect]:
        for player in players:
            player_state = self.check_game_state_for_player(player)
            if player_state[0] != GameState.NOT_FINISH:
                return True, player_state[1]
        return False, Rect(-1, -1, -1, -1)

    @staticmethod
    def replay(history: list[int], players: list[int], errors: list[str]) -> Board:
        count = 0
        board = Board()
        for elt in history:
            if board.add_token(elt, players[count % len(players)]):
                count += 1
            else:
                errors.append("Replay: Could not play at column {}, iteration {}".format(elt, count))
        return board

    @staticmethod
    def load_from_json(data: dict, errors: list[str]) -> list[Board]:
        try:
            history = data[SaveConst.BOARD.value][SaveConst.BOARD_HISTORY.value]
            players = data[SaveConst.GAME.value][SaveConst.PLAY_ORDER.value]
            return [Board.replay(history, players, errors)]
        except Exception as ex:
            errors.append("Board could not be init from the game save, {}".format(ex))
            return []

    def save_to_json(self, data_to_saved: dict, errors: list[str]) -> dict:
        if data_to_saved.get(SaveConst.BOARD.value, None) is not None:
            data_to_saved[SaveConst.BOARD.value].update({SaveConst.BOARD_HISTORY.value: self._history})
        else:
            data_to_saved[SaveConst.BOARD.value] = {SaveConst.BOARD_HISTORY.value: self._history}
        return data_to_saved

    def calculus_board_to_str(self, player_id: int):
        board_str = ""
        board = np.where(self.board == player_id, 1, 0)
        for i in range(board.shape[0]):
            board_str += "|".join(["X" if board[i, :] == 1 else " "]) + "\n"
            board_str += "-" * (2 * board.shape[1] - 1) + "\n"
        return board_str

    def __eq__(self, other):
        if type(other) == Board:
            return self._history == other._history
        elif type(other) == dict:
            return self._history == other.get(SaveConst.BOARD.value, {}).get(SaveConst.BOARD_HISTORY.value, None)
        else:
            return False

    def board_to_str(self, players: dict[str, Player]):
        board_str = ""
        board = self.board
        for i in range(board.shape[0]):
            for elt in board[i, :]:
                if elt == 0:
                    board_str += "|" + " "
                else:
                    if players is None:
                        board_str += "| "
                        continue
                    player: Player = players.get(elt, None)
                    if player is None:
                        board_str += "| "
                        continue
                    board_str += "|" + Player.SHAPE.get(player.token, None)
            board_str += "\n"
            board_str += "-" * (2 * board.shape[1] - 1) + "\n"
        return board_str
