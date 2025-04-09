class Board:
    """
    Main board class. Allows user to set board size, place ships,
    generates a computers board, and allows user to make guesses,
    while generates a random guess for the computer.
    """

    def __init__(self, height, width, size, num_ships):
        self.height = height
        self.width = width
        self.size = size
        self.num_ships = num_ships

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

    def place_ships(self, user_board):
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
        for i in range(self.num_ships):
            while True:
                row = int(input("Enter row: \n"))
                col = int(input("Enter col: \n"))
                place = row, col
                placement = user_board[row][col]

                if placement == ".":
                    place
                else:
                    print("""Ship already palced there, please select another
place.
                        """)

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
                self.size = int(input("""Please enter 1, 2 or 3 depending on
the size board you would like to play on: \n"""))
            except ValueError:
                print("Invalid input. Please enter a valid option of 1, 2, 3.")
                continue

            if self.size == 1:
                self.num_ships = 4
                self.place_ships(self.board_creation(5, 5))
                break
            elif self.size == 2:
                self.num_ships = 8
                self.place_ships(self.board_creation(10, 10))
                break
            elif self.size == 3:
                self.num_ships = 12
                self.place_ships(self.board_creation(15, 15))
                break
            else:
                print("""Invalid option please pick a valid option of
1, 2 or 3.
                      """)


my_board = Board(0, 0, 0, 0)
my_board.board_size()
