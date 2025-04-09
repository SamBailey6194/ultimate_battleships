from random import randint


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
S = Ship placement.
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


def update_board(user, board, row, col):
    """
    Function to update board that has been attacked
    """
    if board.grid == "M" or "H":
        print(f"{user} you have already shot here, please pick a new spot.")
        return True
    elif board.grid[row][col] == ".":
        print(f"""{user} missed! Try again next time. Still {board.num_ships}
left to hit
            """)
        board.grid[row][col] = "M"
        return True
    elif board.grid[row][col] == "S":
        print(f"""{user} Hit! Well done. Just {board.num_ships-1} left to
destroy.
            """)
        board.grid[row][col] = "H"
        return True
    else:
        print("""Remember: The top left corner is row: 0, col: 0.
Please bear that in mind when entering rows and columns.
                """)
        return False


def shots_fired(board):
    """
    This asks for user to fire their shots
    """
    print("-" * 35)
    print("""Below you can enter the coordinates you would like to hit.
Please remember the top left corner is row: 0, col: 0.
Please bear that in mind when entering rows and columns.
        """)
    print("-" * 35)
    print("""Key:
          S = Ship
          H = Hit
          M = Miss
        """)
    user = "Sam"
    while True:
        try:
            row = int(input("Enter row: \n"))
            col = int(input("Enter col: \n"))
            if board.grid[row][col] == ".":
                update_board(user, board, row, col)
                board.display_board(show_ships=True)
                return True
        except (ValueError, IndexError):
            print("""Remember: The top left corner is row: 0, col: 0.
Please bear that in mind when entering rows and columns.
                """)


def computer_shots(board):
    """
    Generates random shots by computer
    """
    row = random_point(board.size)
    col = random_point(board.size)
    update_board("Computer", board, row, col)
    board.display_board(show_ships=False)


def main():
    user = user_board()
    computer = computer_board(user.size, user.num_ships)
    user_ships_hit = 0
    computer_ships_hit = 0
    user_ships = user_ships_hit < user.num_ships
    computer_ships = computer_ships_hit < computer.num_ships

    while user_ships and computer_ships:
        shots_fired(computer)
        if any("H" in row for row in computer.grid):
            computer_ships_hit += 1

        computer_shots(user)
        if any("H" in row for row in user.grid):
            user_ships_hit += 1

        print("-" * 35)
        print(f"User hits: {computer_ships_hit}/{computer.num_ships}")
        print(f"Computer hits: {user_ships_hit}/{user.num_ships}")

        if computer_ships_hit == computer.num_ships:
            print("Sam, you win!!!! You beat the computer.")
            break
        elif user_ships_hit == user.num_ships:
            print("Computer wins!!! Unlucky Sam, maybe next time.")
            break
        else:
            print("No one has won yet. Keep playing")
            print("-" * 35)


main()
