# -*- coding: utf-8 -*-
from __future__ import annotations
from random import Random

import inspect

from src.IStorable import IStorable

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
        player = {}
        for elt in inspect.getmembers(self):
            if not elt[0].startswith('_'):
                if not inspect.ismethod(elt[1]):
                    player.update({elt[0]: elt[1]})
            data["players"].update({self.id: player})
        return data

    def __eq__(self, other):
        return self.id == other.id
