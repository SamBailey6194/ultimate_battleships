# Imported dependencies and modules
from random import randint, choice
import colorama
from colorama import Fore, Style
import time
# Imported other python scripts
from sheets import saved_games
from main import play_again_option

# Initialise colorama
colorama.init(autoreset=True)


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


class Game:
    """
    Class that runs the game, allowing user to place ships, randomly generates
    a computers board and then asks user to guess while randomly generating
    computers guesses and checks for hits and misses.
    """
    def __init__(self, ships_placed=0, ships_hit=0):
        self.ships_placed = ships_placed
        self.ships_hit = ships_hit
        self.username = None

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
                        f"range. It must be a number between 0 and {size - 1}."
                        )
            except (ValueError, IndexError):
                print(
                    "Remember: The top left corner is row: 0, col: 0."
                    "Please bear that in mind when entering rows and columns."
                    )

    def place_ships(self, board):
        """
        Allows user to place their ships where they choose too
        """
        print("-" * 35)
        print(
            "Now you have chosen the size board you want to play on.\n"
            "Please place your ships. Each ship takes up one space.\n"
            "The top left corner is row: 0, col: 0.\n"
            "Please bear that in mind when entering rows and columns.\n"
            "S = Ship placement.")
        print("-" * 35)
        self.ships_placed = 0
        while self.ships_placed < board.num_ships:
            try:
                print("-" * 35)
                row = self.validate_coordinates(
                    "Enter row to place ship at: \n", board.size
                    )
                print("-" * 35)
                print("-" * 35)
                col = self.validate_coordinates(
                    "Enter col to place ship at: \n", board.size
                    )
                print("-" * 35)
                if board.grid[row][col] == ".":
                    board.grid[row][col] = f"{Fore.BLUE}S{Style.RESET_ALL}"
                    self.ships_placed += 1
                    print(f"Ship placed at {row}, {col}")
                    board.display_board(show_ships=True)
                elif board.grid[row][col] == "S":
                    print(
                        "Ship already palced there,"
                        " please select another place."
                        )
            except (ValueError, IndexError):
                print(
                    "Remember: The top left corner is row: 0, col: 0.\n"
                    "Please bear that in mind when entering rows and columns."
                    )

    def random_ship_placement(self, board):
        """
        Places the ships randomly on the board
        """
        self.ships_placed = 0
        while self.ships_placed < board.num_ships:
            row = self.random_point(board.size)
            col = self.random_point(board.size)
            if board.grid[row][col] == ".":
                board.grid[row][col] = f"{Fore.BLUE}S{Style.RESET_ALL}"
                self.ships_placed += 1

        return board

    def user_board(self, player):
        """
        User board is generated blank to allow user to place their ships
        """
        my_board = Board()
        my_board.board_size()
        self.place_ships(my_board)
        print("-" * 35)
        print(f"{player}'s final board \n")
        my_board.display_board(show_ships=True)
        return my_board

    def computer_board(self, user_size, user_ships):
        """
        Generates a board with random placement of ships
        """
        pc_board = Board(size=user_size, num_ships=user_ships)
        pc_board.board_creation()
        self.random_ship_placement(pc_board)
        print("-" * 35)
        print("Computer's board \n")
        pc_board.display_board(show_ships=False)
        return pc_board

    def update_board(self, player, board, row, col):
        """
        Function to update board that has been attacked
        """
        if not (0 <= row < len(board.grid) and 0 <= col < len(board.grid[0])):
            print(f"Invalid coordinates: ({row}, {col})")
            return False

        self.ships_hit
        if board.grid[row][col] in ("M", "H"):
            time.sleep(1)
            print(
                f"{player} you have already shot here, please pick a new spot."
                )
            return False
        elif board.grid[row][col] == "S":
            board.grid[row][col] = f"{Fore.RED}H{Style.RESET_ALL}"
            self.ships_hit += 1
            ships = board.num_ships - sum(row.count("H") for row in board.grid)
            time.sleep(1)
            print(f"{player} Hit! Just {ships} left to destroy.", flush=True)
            return True
        elif board.grid[row][col] == ".":
            ships = board.num_ships - sum(row.count("H") for row in board.grid)
            time.sleep(1)
            print(f"{player} missed! Still {ships} left to hit", flush=True)
            board.grid[row][col] = f"{Fore.GREEN}M{Style.RESET_ALL}"
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
        # Variables that help the random shots not include coordinates
        # the computer has already shot at
        size = target_board.size
        coordinates = [
            (row, col) for row in range(size) for col in range(size)
            ]
        available_coordinates = coordinates.copy()

        while True:
            if is_user:
                print("-" * 35)
                row = self.validate_coordinates(
                    "Enter row to shoot at: \n", size
                    )
                print("-" * 35)
                print("-" * 35)
                col = self.validate_coordinates(
                    "Enter col to shoot at: \n", size
                    )
                print("-" * 35)
            else:
                shot = self.random_coordinate(available_coordinates)
                row, col = shot
                available_coordinates.remove(shot)
            if self.update_board(player_name, target_board, row, col):
                break

    def hit_counter(self, grid):
        """
        Counts the hits for each shot a player takes
        """
        return sum(row.count("H") for row in grid)

    def player_turn(self, username, opponent):
        """
        Player turn taken
        """
        player = username
        time.sleep(1.5)
        print("-" * 35)
        print("Time to take your shot! Fire!!!!!!")
        print("-" * 35)
        self.shots_fired(player, opponent, is_user=True)
        time.sleep(1.5)

    def computer_turn(self, opponent):
        """
        Computer turn taken
        """
        print("-" * 35)
        print("Computer's turn, let's hope they miss!!!")
        print("-" * 35)
        time.sleep(1.5)
        self.shots_fired("Computer", opponent, is_user=False)

    def update_game_status(
            self, player, user, computer, user_ships_hits, computer_ships_hits
            ):
        """
        Updates the game board after shots are taken
        """
        time.sleep(1.5)
        print("-" * 35)
        print(
            "Key:\n"
            f"{Fore.BLUE}S{Style.RESET_ALL} = Ship\n"
            f"{Fore.RED}H{Style.RESET_ALL} = Hit\n"
            f"{Fore.GREEN}M{Style.RESET_ALL} = Miss\n"
            )
        print("-" * 35)
        print(f"{player}'s board:")
        user.display_board(show_ships=True)
        print("-" * 35)
        print("Computer's board:")
        computer.display_board(show_ships=False)
        print("-" * 35)
        time.sleep(1)
        print("-" * 35)
        print(
            f"{player} hits: {Fore.GREEN}{computer_ships_hits}"
            f"{Style.RESET_ALL}/{Fore.RED}{computer.num_ships}"
            f"{Style.RESET_ALL}"
            )
        print(
            f"{player} hits: {Fore.GREEN}{user_ships_hits}"
            f"{Style.RESET_ALL}/{Fore.RED}{user.num_ships}"
            f"{Style.RESET_ALL}"
            )
        print("-" * 35)
        time.sleep(1.5)

    def game_over_check(
            self, player, user_ships_hit, computer_ships_hit,
            total_ships
            ):
        """
        Checks after shots taken if the game is over and congratulates winner
        """
        user_hits = computer_ships_hit == total_ships
        computer_hits = user_ships_hit == total_ships
        if user_hits and computer_hits:
            print("Both players took out each other. Game is a tie")
            return True
        elif user_hits:
            print(f"{player}, you win!!!! You beat the computer.")
            return True
        elif computer_hits:
            print(f"Computer wins!!! Unlucky {player}, maybe next time.")
            return True
        else:
            return False

    def continue_game(self, player):
        """
        Continues game if no one has won yet
        """
        print("-" * 35)
        print(
            f"No winner yet. Game continues. Come on {player} you can win!!!"
            )
        print("-" * 35)

    def convert_board(self, board):
        """
        Converts board into a state that can be saved into Google Sheets
        """
        return "\n".join([
            ",".join(row) for row in board.grid]
            )

    def save_game_state(
            self, player, board_size, num_ships, user_board, computer_board,
            user_hits, computer_hits
            ):
        """
        Prompts the user if they want to save the game or continue
        """
        save = saved_games
        while True:
            save_continue = input(
                f"{player} would you like to continue or save the game and"
                " return later? \nIf you choose to save or exit, the program"
                " will exit and you will \nhave to run it again and log back"
                f" in.\nPlease enter '{Fore.GREEN}C{Style.RESET_ALL}' for"
                f" continue, '{Fore.YELLOW}S{Style.RESET_ALL}' for save or"
                f" '{Fore.RED}E{Style.RESET_ALL}' to exit: \n"
            )

            if save_continue not in ("C", "S", "E"):
                print(
                    f"Please enter '{Fore.GREEN}C{Style.RESET_ALL}',"
                    f" '{Fore.YELLOW}S{Style.RESET_ALL}' or"
                    f" '{Fore.RED}E{Style.RESET_ALL}'"
                    )
                continue
            elif save_continue == "C":
                self.continue_game(player)
                return True
            elif save_continue == "S":
                user_board_convert = self.convert_board(user_board)
                computer_board_convert = self.convert_board(computer_board)

                username_row = None
                for username, row in enumerate(save.get_all_values()):
                    if row[0] == player:
                        username_row = username + 1
                        break

                if username_row:
                    save.update(f"A{username_row}:G{username_row}", [
                        [player, board_size, num_ships, user_board_convert,
                            computer_board_convert, user_hits, computer_hits]
                    ])
                else:
                    save.append_row([
                            player, board_size, num_ships, user_board_convert,
                            computer_board_convert, user_hits, computer_hits
                            ])
                break
            elif save_continue == "E":
                break

        play_again_option(player)
