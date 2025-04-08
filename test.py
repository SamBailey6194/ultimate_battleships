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

    def board_size(self):
        """
        Asks user which board size they would like to go with and
        then generates the board
        """
        print("""Now you are logged in. You can play the game.
First though you need to select what size board you want to play on.
All options are a square grid. Each size has a different amount of battleships
to place. Your options are as follows:\n
            1 = 5x5 with 4 battleships
            2 = 10x10 with 8 battleships
            3 = 15x15 with 12 battleships\n
          """)
        while True:
            try:
                self.size = int(input("""Please enter 1, 2 or 3 depending on
the size board you would like to play on: \n"""))
            except ValueError:
                print("Invalid input. Please enter a valid option of 1, 2, 3.")
                continue

            if self.size == 1:
                self.board_creation(5, 5)
                self.num_ships = 4
                break
            elif self.size == 2:
                self.board_creation(10, 10)
                self.num_ships = 8
                break
            elif self.size == 3:
                self.board_creation(15, 15)
                self.num_ships = 12
                break
            else:
                print("""Invalid option please pick a valid option of
1, 2 or 3.
                      """)

    def place_ships(self):
        """
        Allows user to place their ships where they choose too
        """
        print("""Now you have chosen the size board you want to play
on. Please place your ships. The top left corner is row: 0, col: 0.
Please bear that in mind when entering rows and columns.
            """)
        


my_board = Board(0, 0, 0, 0)
my_board.board_size()
