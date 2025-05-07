# This script holds all the board creation logic

# Imported dependencies and modules
import time
import datetime
from random import randint
# Imported other python scripts
from style import StyledText, Symbols


class Board:
    """
    Main board class. Allows user to set board size, place ships,
    generates a computers board, and allows user to make guesses,
    while generates a random guess for the computer.
    """
    def __init__(self, size=0, total_ships=0):
        self.size = size
        self.total_ships = total_ships
        self.grid = []

    def display_board(self, show_ships=False):
        """
        Print board for user to see correctly
        While hiding where computer's ships are
        Note, this function can also hide where the user put their ships
        """
        grid_nums = "  "+" ".join(f"{num}" for num in range(self.size))
        water_space = Symbols.water()
        ship_space = Symbols.ship()
        print(grid_nums)

        for position, row in enumerate(self.grid):
            displayed_row = []
            for cell in row:
                # Replace ships "S" with "~"
                if not show_ships and cell == ship_space:
                    displayed_row.append(water_space)
                else:
                    # Show full board with ships
                    displayed_row.append(cell)
            white_grid = (
                f"{position} " + " ".join(displayed_row))
            print(white_grid)

    def board_creation(self):
        """
        Generates the board size the user selected as a 2D list
        """
        water_space = Symbols.water()
        self.grid = [
            [f"{water_space}"] *
            self.size for _ in range(self.size)
            ]
        return self.grid

    def validate_board_size(self, data):
        """
        Validates board size input by user
        """
        if data == 1:
            self.size, self.total_ships = 5, 4
        elif data == 2:
            self.size, self.total_ships = 10, 8
        elif data == 3:
            self.size, self.total_ships = 15, 12
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
        print(
            "Now you are logged in. \n"
            "You can play the game. \n"
            "\n"
            "First though you need to select\n"
            "what size board you want to play on.\n"
            "\n"
            "All options are a square grid.\n"
            "Your options are as follows:\n"
            f"{StyledText.green('1')} = {StyledText.green('5x5')} with"
            f" {StyledText.magenta('4')} battleships\n"
            "\n"
            f"{StyledText.yellow('2')} = {StyledText.yellow("10x10")} with"
            f" {StyledText.magenta('8')} battleships\n"
            "\n"
            f"{StyledText.red('3')} = {StyledText.red('15x15')} with"
            f" {StyledText.magenta('12')} battleships\n")
        print("-" * 35)

        while True:
            try:
                size = int(input(
                    f"Please enter {StyledText.green('1')},"
                    f" {StyledText.yellow('2')} or {StyledText.red('3')}\n"
                    "depending on the size board you\n"
                    "would like to play on: \n"
                    ))
                print("-" * 35)
                if self.validate_board_size(size):
                    time.sleep(0.5)
                    print("Generating board . . .")
                    time.sleep(0.5)
                    self.display_board()
                    break
            except ValueError:
                print(
                    f"Please input {StyledText.green('1')},"
                    f" {StyledText.yellow('2')} or {StyledText.red('3')}\n"
                    )
        return size, self.total_ships


class BoardSetup:
    """
    Class that setsup the game by allowing the user to place ships and
    randomly generates a computers board
    """
    def __init__(
            self,
            player,
            size,
            player_board=None,
            pc_board=None,
            game_id=None
            ):
        # Provides each game with a unique ID so when saving a loaded game
        # it overwirtes the correct game
        self.game_id = (
            game_id or datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            )
        self.player = player
        self.size = size
        self.ships_placed = 0

        if player_board and pc_board:
            self.player_board = player_board
            self.pc_board = pc_board

        else:
            self.player_board = Board()
            self.pc_board = Board()

    def random_point(self, size):
        """
        Helper method to generate random integer between 0 and board size
        """
        return randint(0, size-1)

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
                        f"{StyledText.red(
                            'Please remember to enter a coordinate'
                            'in the correct range.'
                            )}\n"
                        "\n"
                        f"It must be a number between {StyledText.yellow('0')}"
                        f" and {StyledText.yellow(size - 1)}."
                        )
            except (ValueError, IndexError):
                print(
                    f"{StyledText.red('Remember: The top left corner is')}\n"
                    f"row: {StyledText.yellow('0')}\n"
                    f"col: {StyledText.yellow('0')}.\n"
                    "Please bear that in mind when entering rows and columns."
                    )

    def player_place_ships(self):
        """
        Allows player to place their ships where they choose too
        """
        water_space = Symbols.water()
        ship_space = Symbols.ship()
        print("-" * 35)
        print(
            "Now you have chosen the size board\n"
            "you want to play on.\n"
            "\n"
            "Please place your ships.\n"
            "\n"
            "Each ship takes up one space.\n"
            "\n"
            "The top left corner is \n"
            f"row: {StyledText.yellow('0')}\n"
            f"col: {StyledText.yellow('0')}.\n"
            "\n"
            "Please bear that in mind when entering\n"
            "rows and columns.\n"
            f"'{ship_space}' = Ship placement."
            )
        self.ships_placed = 0
        while self.ships_placed < self.player_board.total_ships:
            try:
                print("-" * 35)
                row = self.validate_coordinates(
                    "Enter row to place ship at: \n", self.player_board.size
                    )
                print("-" * 35)
                col = self.validate_coordinates(
                    "Enter col to place ship at: \n", self.player_board.size
                    )
                print("-" * 35)

                if self.player_board.grid[row][col] == water_space:
                    self.player_board.grid[row][col] = ship_space
                    self.ships_placed += 1
                    print(
                        f"Ships Placed:"
                        f" {StyledText.magenta(self.ships_placed)} of"
                        f" {StyledText.magenta(self.player_board.total_ships)}"
                    )
                    print(
                        f"Ship placed at {StyledText.yellow(row)},"
                        f" {StyledText.yellow(col)}"
                        )
                    self.player_board.display_board(show_ships=True)
                elif self.player_board.grid[row][col] == ship_space:
                    print(
                        StyledText.red(
                            "Ship already palced there,"
                            " please select another place."
                            )
                        )
            except (ValueError, IndexError):
                print(
                    f"{StyledText.red('Remember: The top left corner is')}\n"
                    f"row: {StyledText.yellow('0')}\n"
                    f"col: {StyledText.yellow('0')}.\n"
                    "Please bear that in mind when entering rows and columns."
                    )

    def random_ship_placement(self):
        """
        Places the ships randomly on the board
        """
        water_space = Symbols.water()
        ship_space = Symbols.ship()
        self.ships_placed = 0
        while self.ships_placed < self.pc_board.total_ships:
            row = self.random_point(self.pc_board.size)
            col = self.random_point(self.pc_board.size)
            if self.pc_board.grid[row][col] == water_space:
                self.pc_board.grid[row][col] = ship_space
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

    def computer_board(self):
        """
        Generates a board with random placement of ships
        """
        self.pc_board.size = self.player_board.size
        self.pc_board.total_ships = self.player_board.total_ships
        self.pc_board.board_creation()
        self.random_ship_placement()
        print("-" * 35)
        print("Computer's board \n")
        self.pc_board.display_board(show_ships=False)
        return self.pc_board
