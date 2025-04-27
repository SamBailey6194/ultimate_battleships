# This script holds all the game logic classes

# Imported dependencies and modules
from random import choice
import colorama
from colorama import Fore, Style
import time
# Imported other python scripts
from save_load import Save, Load_Games
from board_creation import Board_Setup

# Initialise colorama
colorama.init(autoreset=True)

# Global Colorama variables for game_logic
water = f"{Fore.BLUE}~{Style.RESET_ALL}"
ship = f"{Fore.MAGENTA}S{Style.RESET_ALL}"
hit = f"{Fore.RED}H{Style.RESET_ALL}"
miss = f"{Fore.GREEN}M{Style.RESET_ALL}"


class Board_After_Shots:
    def __init__(self, game):
        self.game = game

    def hit_counter(self, grid):
        """
        Counts the hits for each shot a player takes
        """
        return sum(
            row.count(f"{Fore.RED}H{Style.RESET_ALL}") for row in grid
            )

    def valid_shot(self, row, col, board):
        """
        Refactord code to hold the validate the coordinates shot at
        """
        if not (
            0 <= row < len(board.grid) and 0 <= col < len(board.grid[0])
        ):
            print(f"Invalid coordinates: ({row}, {col})")
            return False
        return True

    def already_shot(self, board, general, row, col):
        """
        Refactored code to hold the explanation a shot has
        already been made there
        """
        if board.grid[row][col] in (miss, hit):
            time.sleep(1)
            print(
                f"{general} you have already shot here, please pick a"
                " new spot."
                )
            return False

    def hit(self, board, general, row, col):
        """
        Refactored code to hold the processing of when
        a shot hits a ship
        """
        if board.grid[row][col] == ship:
            board.grid[row][col] = hit

            if general == self.game.player:
                self.game.user_hits += 1
            else:
                self.game.computer_hits += 1

            ships = board.num_ships - self.hit_counter(board.grid)
            time.sleep(1)
            print(
                f"{general} {Fore.RED}Hit{Style.RESET_ALL}!\n"
                f"Just {ships} left to destroy.", flush=True
                )
            return True

    def miss(self, board, general, row, col):
        """
        Refactored code to hold the processing of when
        a shot misses
        """
        if board.grid[row][col] == water:
            ships = board.num_ships - self.hit_counter(board.grid)
            time.sleep(1)
            print(
                f"{general} {Fore.GREEN}Miss{Style.RESET_ALL}!\n"
                f"Just {ships} left to destroy.", flush=True
                )
            board.grid[row][col] = miss
            return True

    def update_board(self, general, board, row, col, game):
        """
        Function to update board that has been attacked
        """
        if not self.valid_shot(row, col, board):
            return False

        if self.already_shot(board, row, col):
            return False

        if self.hit(board, general, row, col):
            return True

        if self.miss(board, general, row, col):
            return True

        time.sleep(1)
        print(
            "Remember: The top left corner is row: 0, col: 0.\n"
            "Please bear that in mind when entering rows and columns."
            )
        return False

    def key(self):
        """
        Refactored code to hold the board key
        """
        print("-" * 35)
        print(
            "Key:\n"
            f"{water} = {Fore.BLUE}Water{Style.RESET_ALL} \n"
            f"{ship} = {Fore.MAGENTA}Ship{Style.RESET_ALL}\n"
            f"{hit} = {Fore.RED}Hit{Style.RESET_ALL}\n"
            f"{miss} = {Fore.GREEN}Miss{Style.RESET_ALL}\n"
            )
        print("-" * 35)

    def boards_shown(self):
        """
        Refactored code to show the updated boards
        """
        print(f"{self.game.player}'s board:")
        self.game.player_board.display_board(show_ships=True)
        print("-" * 35)
        print("Computer's board:")
        self.game.pc_board.display_board(show_ships=False)
        print("-" * 35)

    def stats(self):
        """
        Refactored code to display the game stats
        """
        print("-" * 35)
        print(
            f"{self.game.player} hits: {Fore.RED}{self.game.user_hits}"
            f"{Style.RESET_ALL}/"
            f"{Fore.MAGENTA}{self.game.pc_board.num_ships}"
            f"{Style.RESET_ALL}"
            )
        print(
            f"Computer hits: {Fore.RED}{self.game.computer_hits}"
            f"{Style.RESET_ALL}/"
            f"{Fore.MAGENTA}{self.game.player_board.num_ships}"
            f"{Style.RESET_ALL}"
            )
        print("-" * 35)

    def update_game_status(self, game):
        """
        Updates the game board after shots are taken
        """
        time.sleep(1.5)
        self.key()
        self.boards_shown()
        self.stats()
        time.sleep(1.5)


class Shot_Tracker:
    def __init__(self, game):
        self.game = game
        self.available_coordinates = []

    def random_coordinate(self, coordinates):
        """
        Helper method to generate random coordinates
        """
        return choice(coordinates)

    def reset_coordinates(self, size):
        """
        Resets the coordinates the computer can choose from when starting
        a new game or loading in a saved game
        """
        self.available_coordinates = [
            (row, col) for row in range(size) for col in range(size)
        ]

    def shots_fired(self, player_name, target_board, is_user, game):
        """
        This asks for user to fire their shots and takes a random
        shot for the computer
        """
        board = Board_Setup(
            self.game.player,
            self.game.player_board.ships,
            self.game.player_board,
            self.game.pc_board
            )
        size = target_board.size

        if self.available_coordinates is None:
            self.reset_coordinates(size)

        while True:
            if is_user:
                print("-" * 35)
                row = board.validate_coordinates(
                    "Enter row to shoot at: \n", size
                    )
                print("-" * 35)
                col = board.validate_coordinates(
                    "Enter col to shoot at: \n", size
                    )
                print("-" * 35)
            else:
                shot = self.random_coordinate(self.available_coordinates)
                row, col = shot
                self.available_coordinates.remove(shot)

            if self.game.board_management.update_board(
                player_name,
                target_board,
                row,
                col
            ):
                break


class Turn_Tracker:
    def __init__(self, game):
        self.game = game

    def player_turn(self, game):
        """
        Player turn taken
        """
        time.sleep(1.5)
        print("-" * 35)
        print("Time to take your shot! Fire!!!!!!")
        print("-" * 35)
        self.game.shot.shots_fired(
            self.game.player,
            self.game.pc_board,
            is_user=True,
            game=game
            )
        self.game.user_hits = self.game.board_management.hit_counter(
            self.game.pc_board.grid
            )
        time.sleep(1.5)

    def computer_turn(self, game):
        """
        Computer turn taken
        """
        print("-" * 35)
        print("Computer's turn, let's hope they miss!!!")
        print("-" * 35)
        time.sleep(1.5)
        self.game.shot.shots_fired(
            "Computer",
            self.game.player_board,
            is_user=False,
            game=game
            )
        self.game.computer_hits = self.game.board_management.hit_counter(
            self.game.player_board.grid
            )


class Gameplay:
    def __init__(self, game):
        self.game = game

    def delete_game(self, game):
        """
        Function that deletes a game from the database if it has been
        loaded in and completed
        """
        games = Load_Games(
            self.game.player,
            game_id=None,
            player_board=None,
            computer_board=None,
            games=None,
            player_colour=None,
            computer_colour=None
            )
        all_games = games.load_saved_games()
        all_games = [
            game for game in all_games
            if self.game.game_id != self.game.game_id
            ]

    def game_over_check(self, game):
        """
        Checks after shots taken if the game is over and congratulates
        winner
        """
        player_hits_count = self.game.user_hits == self.game.total_ships
        computer_hits_count = (
            self.game.computer_hits == self.game.total_ships
            )
        if player_hits_count and computer_hits_count:
            print("Both players took out each other. Game is a tie")
            return True
        elif player_hits_count:
            print(
                f"{self.game.player}, you win!!!! You beat the computer."
                )
            return True
        elif computer_hits_count:
            print(
                f"Computer wins!!! Unlucky {self.game.player},"
                " maybe next time."
                )
            return True
        else:
            return False

    def save_game(self, game):
        """
        Saves the game by calling the Save class
        """
        save_state = Save(
            self.game.game_id,
            self.game.player,
            self.game.player_board,
            self.game.pc_board,
            self.game.user_hits,
            self.game.computer_hits
        )
        return save_state.save_game_state()

    def play_game(self, game):
        """
        Starts or resumes the game and checks when the game finishes
        """
        while not self.game_over_check():
            self.game.player_turn()
            self.game.computer_turn()
            self.game.update_game_status()

            continue_save_exit = self.save_game()
            if continue_save_exit == "continue":
                continue
            elif continue_save_exit == "save":
                return "saved"
            elif continue_save_exit == "exit":
                return "exit"

        return "game over"
