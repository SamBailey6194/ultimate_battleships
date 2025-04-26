# This script holds the board creation class
# and loading saved games class

# Imported dependencies and modules
import time
import colorama
from colorama import Fore, Style
from sheets import saved_games

# Initialise colorama
colorama.init(autoreset=True)

# Global variables for board_creation
save = saved_games
water = f"{Fore.BLUE}~{Style.RESET_ALL}"
ship = f"{Fore.MAGENTA}S{Style.RESET_ALL}"
hit = f"{Fore.RED}H{Style.RESET_ALL}"
miss = f"{Fore.GREEN}M{Style.RESET_ALL}"


class Board:
    """
    Main board class. Allows user to set board size, place ships,
    generates a computers board, and allows user to make guesses,
    while generates a random guess for the computer.
    """
    def __init__(self, size=0, num_ships=0):
        self.size = size
        self.num_ships = num_ships
        self.grid = []

    def display_board(self, show_ships=False):
        """
        Print board for user to see correctly
        While hiding where computer's ships are
        Note, this function can also hide where the user put their ships
        """
        grid_nums = "  "+" ".join(f"{num}" for num in range(self.size))
        print(grid_nums)

        for position, row in enumerate(self.grid):
            displayed_row = []
            for cell in row:
                # Replace ships "S" with "~"
                if not show_ships and 'S' in cell:
                    displayed_row.append(water)
                else:
                    # Show full board with ships
                    displayed_row.append(cell)
            print(f"{position} " + " ".join(displayed_row))

    def board_creation(self):
        """
        Generates the board size the user selected as a 2D list
        """
        self.grid = [
            [f"{Fore.BLUE}~{Style.RESET_ALL}"] *
            self.size for _ in range(self.size)
            ]
        return self.grid

    def validate_board_size(self, data):
        """
        Validates board size input by user
        """
        if data == 1:
            self.size, self.num_ships = 5, 4
        elif data == 2:
            self.size, self.num_ships = 10, 8
        elif data == 3:
            self.size, self.num_ships = 15, 12
        else:
            print("Invalid option please pick a valid option of 1, 2 or 3.")
            return False
        self.grid = self.board_creation()
        return True

    def board_size(self):
        """
        Asks user which board size they would like to go with and
        then generates the board and the number of ships for each
        size board.
        """
        print("-" * 35)
        print(
            "Now you are logged in. You can play the game.\n First though you"
            " need to select what size board you want to play on.\n"
            "All options are a square grid.\n"
            "Each size has a different amount of"
            " battleships to place.\n Your options are as follows:\n"
            "- 1 = 5x5 with 4 battleships\n"
            "- 2 = 10x10 with 8 battleships\n"
            "- 3 = 15x15 with 12 battleships\n")
        print("-" * 35)

        while True:
            try:
                size = int(input(
                    "Please enter 1, 2 or 3\n depending on the size board you"
                    " would like to play on: \n"
                    ))
                if self.validate_board_size(size):
                    time.sleep(0.5)
                    print("Generating board . . .")
                    time.sleep(0.5)
                    self.display_board()
                    break
            except ValueError:
                print("Please input 1, 2, or 3.")
        return size


class Load_Games:
    """
    Class that loads the user games associated with the username
    and asks if they want to load any saved games they have
    then converts the string for the boards into grids to allow the user
    to continue the game
    """

    def __init__(
            self, username=None, player_board=None, computer_board=None,
            games=None, player_colour=None, computer_colour=None
            ):
        self.username = username
        self.player_board = player_board
        self.computer_board = computer_board
        self.games = games
        self.player_colour = player_colour
        self.computer_colour = computer_colour

    def convert_board_to_grid(self, game_board):
        """
        Converts board from google sheets back to a grid
        """
        lines = [
            line for line in game_board.strip().split("\n")
            if line.strip()
            ]
        grid = [row.split(",") for row in lines]
        max_len = max(len(row) for row in grid)

        for row in grid:
            if len(row) != max_len:
                raise ValueError("Inconsistent row length in saved game grid.")

        return grid

    def restore_colour(self, grid):
        """
        Restoring colour to the boards after loading in the data
        """
        loaded_grid = []

        for row in grid:
            grid_row = []
            for cell in row:
                if cell == "~":
                    grid_row.append(water)
                elif cell == "S":
                    grid_row.append(ship)
                elif cell == "H":
                    grid_row.append(hit)
                elif cell == "M":
                    grid_row.append(miss)
                else:
                    grid_row.append(cell)

            loaded_grid.append(grid_row)

        return loaded_grid

    def load_saved_games(self):
        """
        Loads the data from saved games sheet for players to be
        able to load their saved game states
        """
        data = saved_games.get_all_records()
        player_games = [
            game for game in data if game["Username"] == self.username
                        ]
        return player_games

    def board_size(self, selected):
        """
        Helper function to check board size
        """
        size = int(selected["Board Size"])
        board = Board(size=size)
        board.grid = [[water] * size for _ in range(size)]
        return board

    def list_saves(self):
        """
        One of the refactoring original access_saved_games function into
        smaller function to handle the listing of the saved games
        """
        print("-" * 35)
        print(f"{self.username} saved games available:")
        for i, save_data in enumerate(self.games):
            size = save_data["Board Size"]
            num_ships = save_data["Number of Ships"]
            user_hits = save_data["User Hits"]
            computer_hits = save_data["Computer Hits"]
            print(
                f"{i + 1}. Size: {size} | Number of Ships: {num_ships} |"
                f" {self.username} Hits: {user_hits} |"
                f" Computer Hits: {computer_hits}"
                )

    def user_choose_save(self):
        """
        One of the refactoring original access_saved_games function into
        smaller function to handle asking user which game they want to save
        """
        while True:
            try:
                option = int(input(
                    "Enter the number next to the game"
                    " you would like to load: \n"
                    ))
                if 1 <= option <= len(self.games):
                    return self.games[option - 1]
                else:
                    print("Invalid selection, please choose a game")
            except ValueError:
                print("Please enter a number shown next to the game.")

    def boards_rebuilt(self, user_selection):
        """
        One of the refactoring original access_saved_games function into
        smaller function to handle rebuilding the boards from the
        save choosen
        """
        # Rebuild user board for selected game
        player_board = self.board_size(user_selection)
        player_board.grid = self.player_colour
        player_board.num_ships = user_selection["Number of Ships"]

        # Rebuild computer board for selected game
        computer_board = self.board_size(user_selection)
        computer_board.grid = self.computer_colour
        computer_board.num_ships = user_selection["Number of Ships"]

        return player_board, computer_board

    def display_boards(self):
        """
        One of the refactoring original access_saved_games function into
        smaller function to handle the displaying the board from the database
        """
        # Loaded board being displayed
        print(
            f"{self.username}'s board:"
            f"{len(self.player_board.grid)}x{len(self.player_board.grid[0])}"
              )
        self.player_board.display_board(show_ships=True)

        print(
            "Computer board:"
            f"{len(self.computer_board.grid)}x"
            f"{len(self.computer_board.grid[0])}"
            )
        self.computer_board.display_board(show_ships=False)

    def access_saved_games(self):
        """
        Loads the list of saved games associated with the username logged in
        with
        """
        self.games = self.load_saved_games()

        if not self.games:
            return None

        self.list_saves()

        user_selection = self.user_choose_save()

        # Restoring the colorama codes to the grid
        self.player_colour = self.restore_colour(
            self.convert_board_to_grid(user_selection["User Board"])
        )
        self.computer_colour = self.restore_colour(
            self.convert_board_to_grid(user_selection["Computer Board"])
        )

        self.player_board, self.computer_board = self.boards_rebuilt(
            user_selection
            )

        self.display_boards()

        return (
            self.player_board,
            self.computer_board,
            self.player_board.num_ships,
            user_selection["User Hits"],
            user_selection["Computer Hits"]
            )
