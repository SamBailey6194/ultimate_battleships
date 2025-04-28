# This script holds all the game within one class
# after importing the game logic classes

# Imported other python scripts
from board_creation import Board_Setup
from game_logic import Board_After_Shots, Shot_Tracker, Turn_Tracker, Gameplay


class Game:
    """
    Class that handles the running of the game. Players turn, computers turn,
    validating the shots, and checking the game is over or not
    """

    def __init__(self, setup: Board_Setup, user_hits=0, computer_hits=0):
        self.game_id = setup.game_id
        self.player = setup.player
        self.total_ships = setup.total_ships
        self.player_board = setup.player_board
        self.pc_board = setup.pc_board
        self.user_hits = user_hits
        self.computer_hits = computer_hits

        self.board_management = Board_After_Shots(self)
        self.shot = Shot_Tracker(self)
        self.turn = Turn_Tracker(self)
        self.gameplay = Gameplay(self)
