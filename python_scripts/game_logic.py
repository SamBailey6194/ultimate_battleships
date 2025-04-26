# This script holds all the game logic within the Game class.
# The reason this script only holds one class, is due
# to the Game class length.

# Imported dependencies and modules
from random import randint, choice
import colorama
from colorama import Fore, Style
import time
import re
# Imported other python scripts
from sheets import saved_games
from board_creation import Board

# Initialise colorama
colorama.init(autoreset=True)

# Global Colorama variables for game_logic
water = f"{Fore.BLUE}~{Style.RESET_ALL}"
ship = f"{Fore.MAGENTA}S{Style.RESET_ALL}"
hit = f"{Fore.RED}H{Style.RESET_ALL}"
miss = f"{Fore.GREEN}M{Style.RESET_ALL}"


class Game:
    """
    Class that runs the game, allowing user to place ships, randomly generates
    a computers board and then asks user to guess while randomly generating
    computers guesses and checks for hits and misses.
    """
    def __init__(
            self, player, total_ships=None, player_board=None, pc_board=None,
            user_hits=0, computer_hits=0, ships_placed=0
            ):
        self.player = player

        if player_board and pc_board:
            self.total_ships = total_ships
            self.player_board = player_board
            self.pc_board = pc_board
            self.user_hits = user_hits
            self.computer_hits = computer_hits
            self.ships_placed = ships_placed

            self.reset_coordinates(self.pc_board.size)

        else:
            self.total_ships = total_ships
            self.player_board = Board()
            self.pc_board = Board()
            self.user_hits = 0
            self.computer_hits = 0
            self.ships_placed = 0
            self.available_coordinates = []

    def random_point(self, size):
        """
        Helper method to generate random integer between 0 and board size
        """
        return randint(0, size-1)

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

    def convert_board(self, board):
        """
        Converts board into a state that can be saved into Google Sheets
        """
        return "\n".join([
            ",".join(row) for row in board.grid]
            )

    def remove_colorama_codes(self, board):
        """
        When saving removes the colorama ANSI codes for the boards, so the boards
        are saved cleanly
        """
        colorama_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        clean_board = []

        # Making sure the board is a list of strings
        if isinstance(board, str):
            board = board.splitlines()

        for row in board:
            clean_row = " ".join([
                colorama_escape.sub('', char) for char in row
                ])
            clean_board.append(clean_row)

        return clean_board

    def hit_counter(self, grid):
        """
        Counts the hits for each shot a player takes
        """
        return sum(row.count(f"{Fore.RED}H{Style.RESET_ALL}") for row in grid)

    def validate_coordinates(self, prompt, size):
        """
        Validates user inputs when asking for coordinates
        """
        while True:
            try:
                value = int(input(prompt))
                if 0 <= value < size:
                    return value
                else:
                    print(
                        "Please remember to enter a coordinate in the correct"
                        " range.\n"
                        f"It must be a number between 0 and {size - 1}."
                        )
            except (ValueError, IndexError):
                print(
                    "Remember: The top left corner is row: 0, col: 0.\n"
                    "Please bear that in mind when entering rows and columns."
                    )

    def player_place_ships(self):
        """
        Allows player to place their ships where they choose too
        """
        print("-" * 35)
        print(
            "Now you have chosen the size board you want to play on.\n"
            "Please place your ships. Each ship takes up one space.\n"
            "The top left corner is row: 0, col: 0.\n"
            "Please bear that in mind when entering rows and columns.\n"
            f"'{ship}' = Ship placement."
            )
        print("-" * 35)
        self.ships_placed = 0
        while self.ships_placed < self.player_board.num_ships:
            try:
                print("-" * 35)
                row = self.validate_coordinates(
                    "Enter row to place ship at: \n", self.player_board.size
                    )
                print("-" * 35)
                print("-" * 35)
                col = self.validate_coordinates(
                    "Enter col to place ship at: \n", self.player_board.size
                    )
                print("-" * 35)

                if self.player_board.grid[row][col] == water:
                    self.player_board.grid[row][col] = ship
                    self.ships_placed += 1
                    print(f"Ship placed at {row}, {col}")
                    self.player_board.display_board(show_ships=True)
                elif self.player_board.grid[row][col] == ship:
                    print(
                        "Ship already palced there,"
                        " please select another place."
                        )
            except (ValueError, IndexError):
                print(
                    "Remember: The top left corner is row: 0, col: 0.\n"
                    "Please bear that in mind when entering rows and columns."
                    )

    def random_ship_placement(self):
        """
        Places the ships randomly on the board
        """
        self.ships_placed = 0
        while self.ships_placed < self.pc_board.num_ships:
            row = self.random_point(self.pc_board.size)
            col = self.random_point(self.pc_board.size)
            if self.pc_board.grid[row][col] == water:
                self.pc_board.grid[row][col] = ship
                self.ships_placed += 1

        return self.pc_board

    def user_board(self):
        """
        User board is generated blank to allow user to place their ships
        """
        self.player_board.board_size()
        self.player_place_ships()
        print("-" * 35)
        print(f"{self.player}'s final board \n")
        self.player_board.display_board(show_ships=True)
        return self.player_board

    def computer_board(self, user_size, user_ships):
        """
        Generates a board with random placement of ships
        """
        self.pc_board.size = user_size
        self.pc_board.num_ships = user_ships
        self.pc_board.board_creation()
        self.random_ship_placement()
        print("-" * 35)
        print("Computer's board \n")
        self.pc_board.display_board(show_ships=False)
        return self.pc_board

    def update_board(self, general, board, row, col):
        """
        Function to update board that has been attacked
        """
        if not (0 <= row < len(board.grid) and 0 <= col < len(board.grid[0])):
            print(f"Invalid coordinates: ({row}, {col})")
            return False

        if board.grid[row][col] in (miss, hit):
            time.sleep(1)
            print(
                f"{general} you have already shot here, please pick a"
                " new spot."
                )
            return False
        elif board.grid[row][col] == ship:
            board.grid[row][col] = hit

            if general == self.player:
                self.user_hits += 1
            else:
                self.computer_hits += 1

            ships = board.num_ships - sum(
                row.count(hit)
                for row in board.grid
                                          )
            time.sleep(1)
            print(
                f"{general} {Fore.RED}Hit{Style.RESET_ALL}!\n"
                f"Just {ships} left to destroy.", flush=True
                )
            return True

        elif board.grid[row][col] == water:
            ships = board.num_ships - sum(
                row.count(hit)
                for row in board.grid
                                          )
            time.sleep(1)
            print(
                f"{general} {Fore.GREEN}Miss{Style.RESET_ALL}!\n"
                f"Just {ships} left to destroy.", flush=True
                )
            board.grid[row][col] = miss
            return True

        else:
            time.sleep(1)
            print(
                "Remember: The top left corner is row: 0, col: 0.\n"
                "Please bear that in mind when entering rows and columns."
                )
            return False

    def shots_fired(self, player_name, target_board, is_user):
        """
        This asks for user to fire their shots and takes a random
        shot for the computer
        """
        size = target_board.size

        if self.available_coordinates is None:
            self.reset_coordinates(size)

        while True:
            if is_user:
                print("-" * 35)
                row = self.validate_coordinates(
                    "Enter row to shoot at: \n", size
                    )
                print("-" * 35)
                col = self.validate_coordinates(
                    "Enter col to shoot at: \n", size
                    )
                print("-" * 35)
            else:
                shot = self.random_coordinate(self.available_coordinates)
                row, col = shot
                self.available_coordinates.remove(shot)

            if self.update_board(player_name, target_board, row, col):
                break

    def player_turn(self):
        """
        Player turn taken
        """
        time.sleep(1.5)
        print("-" * 35)
        print("Time to take your shot! Fire!!!!!!")
        print("-" * 35)
        self.shots_fired(self.player, self.pc_board, is_user=True)
        self.user_hits = self.hit_counter(self.pc_board.grid)
        time.sleep(1.5)

    def computer_turn(self):
        """
        Computer turn taken
        """
        print("-" * 35)
        print("Computer's turn, let's hope they miss!!!")
        print("-" * 35)
        time.sleep(1.5)
        self.shots_fired("Computer", self.player_board, is_user=False)
        self.computer_hits = self.hit_counter(self.player_board.grid)

    def update_game_status(self):
        """
        Updates the game board after shots are taken
        """
        time.sleep(1.5)
        print("-" * 35)
        print(
            "Key:\n"
            f"{water} = {Fore.BLUE}Water{Style.RESET_ALL} \n"
            f"{ship} = {Fore.MAGENTA}Ship{Style.RESET_ALL}\n"
            f"{hit} = {Fore.RED}Hit{Style.RESET_ALL}\n"
            f"{miss} = {Fore.GREEN}Miss{Style.RESET_ALL}\n"
            )
        print("-" * 35)
        print(f"{self.player}'s board:")
        self.player_board.display_board(show_ships=True)
        print("-" * 35)
        print("Computer's board:")
        self.pc_board.display_board(show_ships=False)
        print("-" * 35)
        time.sleep(1)
        print("-" * 35)
        print(
            f"{self.player} hits: {Fore.RED}{self.user_hits}"
            f"{Style.RESET_ALL}/{Fore.MAGENTA}{self.pc_board.num_ships}"
            f"{Style.RESET_ALL}"
            )
        print(
            f"Computer hits: {Fore.RED}{self.computer_hits}"
            f"{Style.RESET_ALL}/{Fore.MAGENTA}{self.player_board.num_ships}"
            f"{Style.RESET_ALL}"
            )
        print("-" * 35)
        time.sleep(1.5)

    def game_over_check(self):
        """
        Checks after shots taken if the game is over and congratulates winner
        """
        player_hits_count = self.user_hits == self.total_ships
        computer_hits_count = self.computer_hits == self.total_ships
        if player_hits_count and computer_hits_count:
            print("Both players took out each other. Game is a tie")
            return True
        elif player_hits_count:
            print(f"{self.player}, you win!!!! You beat the computer.")
            return True
        elif computer_hits_count:
            print(f"Computer wins!!! Unlucky {self.player}, maybe next time.")
            return True
        else:
            return False

    def save_game_state(self):
        """
        Prompts the user if they want to save the game or continue
        """
        save = saved_games
        board_size = self.player_board.size

        while True:
            save_continue = input(
                f"{self.player} would you like to continue or save the game"
                " and return later? \n"
                f"Please enter '{Fore.GREEN}C{Style.RESET_ALL}' for"
                f" continue, '{Fore.YELLOW}S{Style.RESET_ALL}' for save or"
                f" '{Fore.RED}E{Style.RESET_ALL}' to exit: \n"
            ).strip().upper()

            if save_continue not in ("C", "S", "E"):
                print(
                    f"Please enter '{Fore.GREEN}C{Style.RESET_ALL}',"
                    f" '{Fore.YELLOW}S{Style.RESET_ALL}' or"
                    f" '{Fore.RED}E{Style.RESET_ALL}'"
                    )
                continue
            elif save_continue == "C":
                print("-" * 35)
                print(
                    "No winner yet. Game continues.\n"
                    f"Come on {self.player} you can win!!!"
                    )
                print("-" * 35)
                return "continue"
            elif save_continue == "S":
                # Converts boards from grids to strings
                player_board_convert = self.convert_board(
                    self.player_board
                    )
                computer_board_convert = self.convert_board(
                    self.pc_board
                    )

                # Removes the colorama codes from the board strigns
                player_clean_board = self.remove_colorama_codes(
                    player_board_convert
                    )
                computer_clean_board = self.remove_colorama_codes(
                    computer_board_convert
                    )

                stringify_player_board = "\n".join(player_clean_board)
                stringify_computer_board = "\n".join(computer_clean_board)

                username_row = None
                for username, row in enumerate(save.get_all_values()):
                    if row[0] == self.player:
                        username_row = username + 1
                        break

                if username_row:
                    save.update(f"A{username_row}:G{username_row}", [
                        [
                            self.player, board_size, self.ships_placed,
                            stringify_player_board, stringify_computer_board,
                            self.user_hits, self.computer_hits
                         ]
                    ])
                else:
                    save.append_row([
                            self.player, board_size, self.ships_placed,
                            stringify_player_board, stringify_computer_board,
                            self.user_hits, self.computer_hits
                            ])
                return "save"
            elif save_continue == "E":
                return "exit"

    def play_game(self):
        """
        Starts or resumes the game and checks when the game finishes
        """
        while True:
            self.player_turn()
            self.computer_turn()

            self.update_game_status()

            if self.game_over_check():
                break
            else:
                continue_save_exit = self.save_game_state()
                if continue_save_exit == "continue":
                    continue
                elif continue_save_exit == "save":
                    return "saved"
                elif continue_save_exit == "exit":
                    return "exit"

        return "game over"
