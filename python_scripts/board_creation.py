# Imported dependencies and modules
import time


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
        for row in self.grid:
            if not show_ships:
                # Replace ships "S" with "."
                print(" ".join(["." if "S" in cell else cell for cell in row]))
            else:
                # Show full board with ships
                print(" ".join(row))

    def board_creation(self):
        """
        Generates the board size the user selected as a 2D list
        """
        self.grid = [["."] * self.size for _ in range(self.size)]
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
                    "would like to play on: \n"
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
