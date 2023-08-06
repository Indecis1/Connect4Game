# -*- coding: utf-8 -*-

from src.const import GameState
from src.board import Board
from src.player import Player

class Game:
    """
    This class implements the game logic player, board init and orchestrates the game
    """

    def __init__(self):
        self.players = {}
        self.board = Board()
        self.game_state = GameState.NOT_FINISH

    def play_in_column(self, column_position: int, player_id: int) -> bool:
        player = self.players.get(player_id, None)
        if player is None:
            return False
        return self.board.add_token(column_position, player)

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

    def game_loop(self, player_ids: list[int]):
        """
        The Game loop
        :param player_ids: the player id in play order
        :return:
        """
        print("Welcome on the Connect 4 Game: \n")
        print(self.board.board_to_str(), end="\n")
        i = 0
        if len(player_ids) == 0:
            return
        player = self.players.get(player_ids[i], None)
        print("{} playing ...\n".format(player.name))
        if player is None:
            return
        while self.game_state == GameState.NOT_FINISH:
            try:
                user_input = int(input("Column number to play: ").strip())
                if user_input < 0 or user_input > 6:
                    print("The column number should be between 0-6")
                    continue
                is_token_added = self.board.add_token(user_input, player)
                result = self.board.check_game_state_for_player(player)
                if result[0] != GameState.NOT_FINISH:
                    print(self.board.board_to_str(), end="\n")
                    break
                if is_token_added:
                    i = (i + 1) % len(player_ids)
                    player = self.players.get(player_ids[i], None)
            except Exception as e:
                print("you should provide a valid number")
            print(self.board.board_to_str(), end="\n")
            print("{} playing ...\n".format(player.name))
        print("player {} won...\n".format(player.name))

if __name__ == '__main__':
    game = Game()
    player_ids = [game.create_player("Player1", "Red", "Circle"), game.create_player("Player2", "Green", "Cross")]
    game.game_loop(player_ids)



