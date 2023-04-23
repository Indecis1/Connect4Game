# -*- coding: utf-8 -*-

from random import Random

class Player:

    def __init__(self, name: str, color: str, token: str = "Circle"):
        self.name = name
        self.color = color
        self.token = token
        self.possible_ids = list(range(1, 10))
        self.id = None
        self.__init_id()

    def __init_id(self):
        ran = Random()
        ran.randint(1, 10)
        choice_id = ran.choice(self.possible_ids)
        self.possible_ids.remove(choice_id)
        self.id = choice_id

