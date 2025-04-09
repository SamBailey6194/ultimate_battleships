from random import randint


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
    board = Board()
    ships_placed = 0
    while ships_placed < board.num_ships:
        try:
            row = int(input("Enter row: \n"))
            col = int(input("Enter col: \n"))
            if Board.grid[row][col] == ".":
                Board.grid[row][col] == "@"
                ships_placed += 1
            elif Board.grid[row][col] == "@":
                print("""Ship already palced there, please select another
place.
                    """)
        except (ValueError, IndexError):
            print("""Remember: The top left corner is row: 0, col: 0.
Please bear that in mind when entering rows and columns.
                """)


def user_board():
    """
    User board is generated blank to allow user to place their ships
    """
    my_board = Board()
    my_board.board_size()
    place_ships(my_board)
    print(my_board)
    return my_board


def computer_board():
    """
    Generates a board with random placement of ships
    """
    pc_board = Board(user_board.height, user_board.width, user_board.size,
                     user_board.num_ships)
    pc_board.grid = pc_board.board_creation(pc_board.height, pc_board.width)

    pc_ships_placed = 0
    while pc_ships_placed < pc_board.num_ships:
        row = random_point(pc_board.width)
        col = random_point(pc_board.height)
        if pc_board.grid[row][col] == ".":
            pc_board.grid[row][col] = "@"
            pc_ships_placed += 1
    print(pc_board)
    return pc_board


def main():
    print("Your final board: \n")
    user_board()
    print("Computer's board: \n")
    computer_board()


main()
