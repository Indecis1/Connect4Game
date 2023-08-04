# -*- coding: utf-8 -*-

from src.player import Player

class Token:

    def __init__(self, player: Player):
        self.player = player

    def __eq__(self, other):
        if type(other) is not Token:
            return False
        return self.player == other.player

        