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

    def __init__(self, height=0, width=0, size=0, num_ships=0):
        self.height = height
        self.width = width
        self.size = size
        self.num_ships = num_ships
        self.grid = []

    def board_creation(self, height, width):
        """
        Generates the board size the user selected
        """
        grid = []
        i = int(0)
        for i in range(width):
            grid.append(".")
        for i in range(height):
            clear_grid = " ".join(grid)
            print(clear_grid)
        return clear_grid

    def validate_board_size(self, data):
        """
        Validates board size input by user
        """
        if data == 1:
            self.height, self.width, self.num_ships = 5, 5, 4
        elif data == 2:
            self.height, self.width, self.num_ships = 10, 10, 8
        elif data == 3:
            self.height, self.width, self.num_ships = 15, 15, 12
        else:
            print("""Invalid option please pick a valid option of
1, 2 or 3.
                """)
            return False
        self.grid = self.board_creation(self.height, self.width)
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
            self.size = int(input("""Please enter 1, 2 or 3 depending on
the size board you would like to play on: \n"""))
            if self.validate_board_size(self.size):
                break


def main():
    """
    Run all program functions
    """
    print("Welcome to Ultimate Battleships!\n")
    intro()
    board = Board()
    board.board_size()


main()
