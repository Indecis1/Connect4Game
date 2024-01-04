# -*- coding: utf-8 -*-

from enum import Enum


class GameState(Enum):
    PLAYER_LOOSE = -1
    DRAW = 0
    PLAYER_WIN = 1
    NOT_FINISH = 10
    PAUSE = 20


class SaveConst(Enum):
    BOARD = "Board"
    BOARD_HISTORY = "History"
    GAME = "game"
    GAME_STATE = "game_state"
    PLAY_ORDER = "play_order"
    PLAYER = "players"
