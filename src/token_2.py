# -*- coding: utf-8 -*-

from src.player import Player

class Token:

    SHAPE = {
        "circle": "O",
        "cross": "X"
    }

    def __init__(self, player: Player):
        self.player = player

    def __eq__(self, other):
        if type(other) is not Token:
            return False
        return self.player == other.player

    def token_to_str(self) -> str:
        return Token.SHAPE.get(self.player.token.lower(), " ")
        