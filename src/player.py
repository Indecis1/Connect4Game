# -*- coding: utf-8 -*-

from random import Random

class Player:

    POSSIBLE_IDS = list(range(1, 10))
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

    def __eq__(self, other):
        return self.id == other.id
