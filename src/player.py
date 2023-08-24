# -*- coding: utf-8 -*-
from __future__ import annotations
from random import Random

import inspect

from src.IStorable import IStorable
from src.const import *

class Player(IStorable):

    POSSIBLE_IDS = list(range(1, 10))

    SHAPE = {
        "cross": "X",
        "circle": "O"
    }

    def __init__(self, name: str, color: str, token: str = "Circle"):
        self.name = name
        self.color = color
        self.token = token
        self.id = None
        self.__init_id()

    def __init_id(self):
        ran = Random()
        ran.randint(1, 10)
        choice_id = ran.choice(self.POSSIBLE_IDS)
        Player.POSSIBLE_IDS.remove(choice_id)
        self.id = choice_id

    @staticmethod
    def load_from_json(json_obj: dict, errors: list[str]) -> list[Player]:
        players: list[Player] = []
        players_obj = json_obj.get("players", None)
        if players_obj is None:
            errors.append("players key not found in the saved game")
            return []
        for player_id in players_obj:
            player = Player(**players_obj[player_id])
            players.append(player)
        return players

    def save_to_json(self, data: dict, errors: list[str]) -> dict:
        if data.get(SaveConst.PLAYER.value, None) is not None:
            data[SaveConst.PLAYER.value].update({self.id: self})
        else:
            data[SaveConst.PLAYER.value] = {self.id: self}
        return data

    def __eq__(self, other):
        if not type(other) == Player:
            return False
        return self.id == other.id and \
        self.color == other.color and \
        self.token == other.token
