# -*- coding: utf-8 -*-

from enum import Enum

class GameState(Enum):
    PLAYER_LOOSE = -1
    DRAW = 0
    PLAYER_WIN = 1
    NOT_FINISH = 10
    PAUSE = 20

class SaveConst(Enum):
    Board = "Board"
    Game = "game"
    PLAYER = "players"

    def __str__(self):
        return self.value
