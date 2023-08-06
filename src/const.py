# -*- coding: utf-8 -*-

from enum import Enum

class GameState(Enum):
    PLAYER_LOOSE = -1
    DRAW = 0
    PLAYER_WIN = 1
    NOT_FINISH = 10
    PAUSE = 20