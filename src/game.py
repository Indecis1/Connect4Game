# -*- coding: utf-8 -*-
from __future__ import annotations

import json

from src.const import GameState
from src.board import Board
from src.player import Player
from src.IStorable import IStorable

class Game(IStorable):
    """
    This class implements the game logic player, board init and orchestrates the game
    """

    def __init__(self, players: dict[int, Player] = None,
                 board: Board = None,
                 game_state: GameState = GameState.NOT_FINISH,
                 play_order: list[int] = None):
        if play_order is None:
            play_order = []
        if players is None:
            players = {}
        if board is None:
            board = Board()
        self.players = players
        self.board = board
        self.game_state = game_state
        self.play_order = play_order

    def play_in_column(self, column_position: int, player_id: int) -> bool:
        return self.board.add_token(column_position, player_id)

    def create_player(self, name: str, color: str, token: str) -> int:
        """
        Create a new player
        :param name: The name of the player
        :param color: The color of the tokens
        :param token: The shape of the token
        :return: id of the player
        """
        player = Player(name, color, token=token)
        self.players[player.id] = player
        return player.id

    @staticmethod
    def load_from_json(data: dict, errors: list[str]) -> list[Game]:
        try:
            game_state = GameState(data["game"]["game_state"])
            play_order = data["game"]["play_order"]
            player_list = Player.load_from_json(data, errors)
            board = Board.load_from_json(data, errors)[0]
            players = {}
            for player in player_list:
                players[player.id] = player
            return [Game(players, board, game_state, play_order)]
        except Exception as ex:
            errors.append("game could not be init from the game save, {}".format(ex))
            return []
        pass

    def save_to_json(self, data_to_saved: dict, errors: list[str]) -> dict:
        data_to_saved["game"] = {}
        for player_id in self.players:
            self.players[player_id].save_to_json(data_to_saved, errors)
        data_to_saved = self.board.save_to_json(data_to_saved, errors)
        data_to_saved["game"]["game_state"] = self.game_state
        data_to_saved["game"]["play_order"] = self.play_order
        return data_to_saved

    def save(self, filepath: str, errors: list[str]) -> bool:
        data_to_saved = {}
        try:
            self.save_to_json(data_to_saved, errors)
            if len(errors) == 0:
                with open(filepath, "w", encoding="utf-8") as file:
                    json.dump(data_to_saved, file, indent=4)
                return True
        except Exception as ex:
            errors.append("Cannot save, {}".format(ex))
            return False

    @staticmethod
    def load(filepath: str, errors: list[str]) -> Game:
        data = {}
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        return Game.load_from_json(data, errors)[0]

    def game_loop(self):
        """
        The Game loop
        :return:
        """
        print("Welcome on the Connect 4 Game: \n")
        print(self.board.board_to_str(self.players), end="\n")
        i = 0
        if len(self.play_order) == 0:
            return
        player = self.players.get(self.play_order[i], None)
        print("{} playing ...\n".format(player.name))
        if player is None:
            return
        while self.game_state == GameState.NOT_FINISH:
            try:
                user_input = int(input("Column number to play: ").strip())
                if user_input < 0 or user_input > 6:
                    print("The column number should be between 0-6")
                    continue
                is_token_added = self.board.add_token(user_input, player.id)
                result = self.board.check_game_state_for_player(player)
                if result[0] != GameState.NOT_FINISH:
                    print(self.board.board_to_str(self.players), end="\n")
                    break
                if is_token_added:
                    i = (i + 1) % len(self.play_order)
                    player = self.players.get(self.play_order[i], None)
            except ValueError:
                print("you should provide a valid number")
            print(self.board.board_to_str(self.players), end="\n")
            print("{} playing ...\n".format(player.name))
        print("player {} won...\n".format(player.name))

if __name__ == '__main__':
    game = Game()
    players_ids = [game.create_player("Player1", "Red", "Circle"), game.create_player("Player2", "Green", "Cross")]
    game.game_loop()



