# -*- coding: utf-8 -*-
from __future__ import annotations
from random import Random

from src.core.IStorable import IStorable
from src.core.const import *


class Player(IStorable):
    POSSIBLE_IDS = list(range(1, 10))

    SHAPE = {
        "cross": "X",
        "circle": "O"
    }

    def __init__(self, name: str, color: str, token: str = "Circle", player_id: int = -1):
        self.name = name
        self.color = color
        self.token = token
        if player_id < 0:
            self.__init_id()
        else:
            self.id = player_id

    def __init_id(self):
        ran = Random()
        ran.randint(1, 10)
        choice_id = ran.choice(self.POSSIBLE_IDS)
        Player.POSSIBLE_IDS.remove(choice_id)
        self.id = choice_id

    @staticmethod
    def load_from_json(json_obj: dict, errors: list[str]) -> list[Player]:
        players: list[Player] = []
        players_obj = json_obj.get(SaveConst.PLAYER.value, None)
        if players_obj is None:
            errors.append("players key not found in the saved game")
            return []
        for player_id in players_obj:
            player = Player(**players_obj[player_id])
            players.append(player)
        return players

    def save_to_json(self, data: dict, errors: list[str]) -> dict:
        player = {
            "player_id": self.id,
            "name": self.name,
            "color": self.color,
            "token": self.token
        }
        if data.get(SaveConst.PLAYER.value, None) is not None:
            data[SaveConst.PLAYER.value].update({self.id: player})
        else:
            data[SaveConst.PLAYER.value] = {self.id: player}
        return data

    def __eq__(self, other):
        if type(other) == Player:
            return self.id == other.id and \
                self.name == other.name and\
                self.color == other.color and \
                self.token == other.token
        elif type(other) == dict:
            return self.id == other.get("player_id", -1) and \
                self.color == other.get("color", None) and \
                self.name == other.get("name", None) and \
                self.token == other.get("token", None)
        else:
            return False
