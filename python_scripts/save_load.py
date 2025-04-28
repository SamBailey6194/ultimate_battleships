# This script holds the loading saved games and
# saving games functions

# Imported dependencies and modules
import colorama
from colorama import Fore, Style
from sheets import saved_games
import re
# Imported other python scripts
from board_creation import Board

# Initialise colorama
colorama.init(autoreset=True)

# Global variables for board_creation
save = saved_games
water = f"{Fore.BLUE}~{Style.RESET_ALL}"
ship = f"{Fore.MAGENTA}S{Style.RESET_ALL}"
hit = f"{Fore.RED}H{Style.RESET_ALL}"
miss = f"{Fore.GREEN}M{Style.RESET_ALL}"


class Load_Games:
    """
    Class that loads the user games associated with the username
    and asks if they want to load any saved games they have
    then converts the string for the boards into grids to allow the user
    to continue the game
    """

    def __init__(
            self,
            game_id=None,
            username=None,
            player_board=None,
            computer_board=None,
            games=None,
            player_colour=None,
            computer_colour=None
            ):
        self.game_id = game_id
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
        return player_games, self.game_id

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
        return self.user_choose_save()

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
                    return None
            except ValueError:
                print("Please enter a number shown next to the game.")
                return None

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
        self.games, _ = self.load_saved_games()

        if not self.games:
            return None

        self.list_saves()

        user_selection = self.user_choose_save()

        self.game_id = user_selection["Game Id"]

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
            self.game_id,
            self.player_board,
            self.computer_board,
            self.games,
            self.player_board.num_ships,
            user_selection["User Hits"],
            user_selection["Computer Hits"]
            )


class Save:
    """
    Class that holds the save game functions
    """

    def __init__(
            self,
            game_id,
            player,
            size,
            total_ships,
            player_board,
            pc_board,
            user_hits,
            computer_hits
            ):
        self.game_id = game_id
        self.player = player
        self.size = size
        self.total_ships = total_ships
        self.player_board = player_board
        self.pc_board = pc_board
        self.user_hits = user_hits
        self.computer_hits = computer_hits

    def prompt_user_save(self):
        """
        Refactored function to hold the user prompt
        """
        allowed_inputs = {
            "C": "continue",
            "S": "save",
            "E": "exit"
            }
        while True:
            save_continue = input(
                f"{self.player} would you like to continue or save the game"
                " and return later? \n"
                f"Please enter '{Fore.GREEN}C{Style.RESET_ALL}' for"
                f" continue, '{Fore.YELLOW}S{Style.RESET_ALL}' for save or"
                f" '{Fore.RED}E{Style.RESET_ALL}' to exit: \n"
            ).strip().upper()

            if save_continue in allowed_inputs:
                return allowed_inputs[save_continue]

            print(
                    f"Please enter '{Fore.GREEN}C{Style.RESET_ALL}',"
                    f" '{Fore.YELLOW}S{Style.RESET_ALL}' or"
                    f" '{Fore.RED}E{Style.RESET_ALL}'"
                    )

    def convert_board(self, board):
        """
        Converts board into a state that can be saved into Google Sheets
        """
        return "\n".join([
            ",".join(row) for row in board.grid]
            )

    def remove_colorama_codes(self, board):
        """
        When saving removes the colorama ANSI codes for the boards, so the
        boards are saved cleanly
        """
        colorama_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        clean_board = []

        # Making sure the board is a list of strings
        if isinstance(board, str):
            board = board.splitlines()

        for row in board:
            clean_row = " ".join([
                colorama_escape.sub('', row)
                ])
            clean_board.append(clean_row)

        return clean_board

    def cleaned_board(self, board):
        """
        Helper function that cleans the boards
        """
        board_conversion = self.convert_board(board)
        return "\n".join(self.remove_colorama_codes(board_conversion))

    def save_board(self):
        """
        Refactored function to save the game board state
        """
        self.player_board = self.cleaned_board(self.player_board)
        self.pc_board = self.cleaned_board(self.pc_board)

    def games_exists_check(self):
        """
        Refactored code to check if the game exists
        """
        for game_data, row in enumerate(saved_games.get_all_values()):
            if row[0] == self.game_id:
                return True, game_data + 1
        return False, None

    def overwrite_save(self, game_row):
        """
        Refactor function that overwrites a loaded in game
        """
        saved_games.update(f"A{game_row}:G{game_row}", [
            [
                self.game_id,
                self.player,
                self.size,
                self.total_ships,
                self.player_board,
                self.pc_board,
                self.user_hits,
                self.computer_hits
                ]
                ])
        print(
            "Loaded game has been saved over.\n"
            "You can access this game next time you log in."
            )

    def save_new_game(self):
        """
        Refactor function that saves a new game
        """
        saved_games.append_row([
            self.game_id,
            self.player,
            self.size,
            self.total_ships,
            self.player_board,
            self.pc_board,
            self.user_hits,
            self.computer_hits
            ])
        print(
            "New game has been saved.\n"
            "You can access this game next time you log in."
            )

    def save_game_state(self):
        """
        Prompts the user if they want to save the game or continue
        """
        save_continue = self.prompt_user_save()

        if save_continue == "continue":
            print("-" * 35)
            print(
                "No winner yet. Game continues.\n"
                f"Come on {self.player} you can win!!!"
                )
            print("-" * 35)
            return "continue"

        elif save_continue == "save":
            self.save_board()

            game_exists, game_row = self.games_exists_check()

            if game_exists:
                self.overwrite_save(game_row)
            else:
                self.save_new_game()
            return "save"

        elif save_continue == "exit":
            return "exit"
