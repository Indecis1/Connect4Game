# -*- coding: utf-8 -*-

from src.board import Board
from src.player import Player

class Game:
    """
    This class implements the game logic player, board init and orchestrates the game
    """

    def __init__(self):
        self.players = []
        self.board = Board()

    def create_player(self, name: str, color: str, token: str) -> None:
        """
        Create a new player
        :param name: The name of the player
        :param color: The color of the tokens
        :param token: The shape of the token
        :return:
        """
        player = Player(name, color, token=token)
        self.players.append(player)

    def loop(self):
        pass
