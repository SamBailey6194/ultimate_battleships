# Imported dependencies and modules
from random import randint
import colorama
import gspread
from google.oauth2.service_account import Credentials
# Imported other python scripts
import user

# Giving python access to google sheet
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ultimate_battleships')
scores = {"computer": 0, "player": 0}


def intro():
    """
    Allow user to create a user name or access a previous
    saved game stored in the google sheet
    """
    print("-" * 35)
    print("""Battleships is a strategy guessing game for two players.
This program allows you to play against a computer to practice.
Once the game starts you will be able to pick a point to hit on
the computers board.
The aim of the game is to hit all of the computers battleships
before they hit all of yours.
          """)
    print("-" * 35)
    user.user_choice()


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
                print(" ".join(["." if cell == "S" else cell for cell in row]))
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
            print("""Invalid option please pick a valid option of
1, 2 or 3.
                """)
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
        print("""Now you are logged in. You can play the game.
First though you need to select what size board you want to play on.
All options are a square grid. Each size has a different amount of battleships
to place. Your options are as follows:\n
            1 = 5x5 with 4 battleships
            2 = 10x10 with 8 battleships
            3 = 15x15 with 12 battleships
          """)
        print("-" * 35)

        while True:
            try:
                size = int(input("""Please enter 1, 2 or 3 depending on
the size board you would like to play on: \n"""))
                if self.validate_board_size(size):
                    self.display_board()
                    break
            except ValueError:
                print("Please input 1, 2, or 3.")
        return size


def random_point(size):
    """
    Helper method to generate random integer between 0 and board size
    """
    return randint(0, size-1)


def place_ships(board):
    """
    Allows user to place their ships where they choose too
    """
    print("-" * 35)
    print("""Now you have chosen the size board you want to play
on. Please place your ships. Each ship takes up one space.
The top left corner is row: 0, col: 0.
Please bear that in mind when entering rows and columns.
        """)
    print("-" * 35)
    ships_placed = 0

    while ships_placed < board.num_ships:
        try:
            row = int(input("Enter row: \n"))
            col = int(input("Enter col: \n"))
            if board.grid[row][col] == ".":
                board.grid[row][col] = "S"
                ships_placed += 1
                print(f"Ship placed at {row}, {col}")
                board.display_board(show_ships=True)
            elif board.grid[row][col] == "S":
                print("""Ship already palced there, please select another
place.
                    """)
        except (ValueError, IndexError):
            print("""Remember: The top left corner is row: 0, col: 0.
Please bear that in mind when entering rows and columns.
                """)


def random_ship_placement(board):
    """
    Places the ships randomly on the board
    """
    ships_placed = 0

    while ships_placed < board.num_ships:
        row = random_point(board.size)
        col = random_point(board.size)
        if board.grid[row][col] == ".":
            board.grid[row][col] = "S"
            ships_placed += 1

    return board


def user_board():
    """
    User board is generated blank to allow user to place their ships
    """
    my_board = Board()
    my_board.board_size()
    place_ships(my_board)
    print("-" * 35)
    print("Your final board \n")
    my_board.display_board(show_ships=True)
    return my_board


def computer_board(user_size, user_ships):
    """
    Generates a board with random placement of ships
    """
    pc_board = Board(size=user_size, num_ships=user_ships)
    pc_board.board_creation()
    random_ship_placement(pc_board)
    print("-" * 35)
    print("Computer's board \n")
    pc_board.display_board(show_ships=False)
    return pc_board


def main():
    """
    Run all program functions
    """
    print("Welcome to Ultimate Battleships!\n")
    intro()
    user = user_board()
    computer_board(user.size, user.num_ships)


# Checks to see if code is being used as a module or main program
if __name__ == "__main()__":
    main()
