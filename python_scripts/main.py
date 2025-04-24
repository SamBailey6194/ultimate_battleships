# Imported dependencies and modules
import colorama
from colorama import Fore, Style
import time
import sys
# Imported other python scripts
from user import user_login, user_creation
from battleships import Board, Game
import leaderboard
from sheets import saved_games

# Initialise colorama
colorama.init(autoreset=True)

# Global variables for main.py
game = Game()
lb = leaderboard
save = saved_games


def intro():
    """
    Welcomes a the user to the game and then asks if they have
    logged in before or not
    """
    print("-" * 35)
    print(
        "Battleships is a strategy guessing game for two players.\n"
        "This program allows you to play against a computer to practice.\n"
        "Once the game starts you will be able to pick a point to hit on the\n"
        "computers board.\n"
        "The aim of the game is to hit all of the computers battleships\n"
        "before they hit all of yours."
        )
    print("-" * 35)
    time.sleep(1.5)


def user_choice():
    """
    Allows user to declare if they are a returning user or a new user
    Then takes them to login or user creation.
    """
    while True:
        login_option = input(
            "Have you already got a login?\n"
            f"If yes please enter '{Fore.GREEN}Y{Style.RESET_ALL}', if no"
            f" please enter '{Fore.RED}N{Style.RESET_ALL}':\n"
            ).strip()

        if login_option not in ("Y", "N"):
            print(
                f"Please enter '{Fore.GREEN}Y{Style.RESET_ALL}' or"
                f" '{Fore.RED}N{Style.RESET_ALL}' \n"
                  )
            continue
        elif login_option == "Y":
            return user_login()
        elif login_option == "N":
            return user_creation()


def leaderboard_generation(player, size):
    """
    Function to show leaderboard and allow user to search leaderboard
    """
    print("-" * 35)
    print(f"{player}, see how you did on the leaderboard below")
    print("-" * 35)
    lb.show_lb(size)
    print("-" * 35)
    user_search = input(
        "Can't see your score on the leaderboard you can search for it using\n"
        " the serachbox below.\n"
        "Type your username here to see where you stand:\n"
        )
    print("-" * 35)
    print("-" * 35)
    lb.search_lb(user_search, size)
    print("-" * 35)


def play_again_option():
    """
    Allows user to tell the program if they want to play again or exit the game
    """
    play_or_exit = input(
        "When you are done searching the leaderboard you can either play again"
        " or exit.\n"
        f"Please enter '{Fore.GREEN}P{Style.RESET_ALL}' to play again or"
        f"'{Fore.RED}E{Style.RESET_ALL}' to exit: \n"
    )


def play_game(
        player, user=None, computer=None, total_ships=None,
        computer_ships_hit=None, user_ships_hit=None
        ):
    """
    Starts or resumes the game and checks when the game finishes
    """
    if not user or not computer:
        user = game.user_board(player)
        computer = game.computer_board(user.size, user.num_ships)
        total_ships = user.num_ships

    while True:
        game.player_turn(player, computer)
        computer_ships_hit = game.hit_counter(computer.grid)

        game.computer_turn(user)
        user_ships_hit = game.hit_counter(user.grid)

        game.update_game_status(
            player, user, computer, user_ships_hit, computer_ships_hit
            )

        if game.game_over_check(
            player, user_ships_hit, computer_ships_hit, total_ships
                ):
            break
        else:
            game.save_game_state(
                player, user.size, total_ships, user, computer,
                computer_ships_hit, user_ships_hit
                )

    lb.update_lb(player, user.size, computer_ships_hit, user_ships_hit)
    leaderboard_generation(player, user.size)
    play_again_option()


class Load_Games:
    """
    Class that loads the user games associated with the username
    and asks if they want to load any saved games they have
    then converts the string for the boards into grids to allow the user
    to continue the game
    """

    def __init__(self):
        pass

    def convert_board_to_grid(self, game_board):
        """
        Converts board from google sheets back to a grid
        """
        lines = [
            line for line in game_board.strip().split("\n") if line.strip()
            ]
        grid = [row.split(",") for row in lines]
        max_len = max(len(row) for row in grid)

        for row in grid:
            if len(row) != max_len:
                raise ValueError("Inconsistent row length in saved game grid.")

        return grid

    def load_saved_games(self, username):
        """
        Loads the data from saved games sheet for players to be
        able to load their saved game states
        """
        data = saved_games.get_all_records()
        player_games = [game for game in data if game["Username"] == username]
        return player_games

    def board_size(self, selected):
        """
        Helper function to check board size
        """
        size = int(selected["Board Size"])
        board = Board(size=size)
        board.grid = [["."] * size for _ in range(size)]
        return board

    def access_saved_games(self, player):
        """
        Loads the list of saved games associated with the username logged in
        with
        """
        games = self.load_saved_games(player)

        print("-" * 35)
        print(f"{player} saved games available:")
        for i, save_data in enumerate(games):
            size = save_data["Board Size"]
            num_ships = save_data["Number of Ships"]
            user_hits = save_data["User Hits"]
            computer_hits = save_data["Computer Hits"]
            print(
                f"{i + 1}. Size: {size} | Number of Ships: {num_ships} |"
                f" {player} Hits: {user_hits} | Computer Hits: {computer_hits}"
                )

        while True:
            try:
                option = int(input(
                    "Enter the number next to the game"
                    "you would like to load: \n"
                    ))
                if 1 <= option <= len(games):
                    user_selection = games[option - 1]
                    break
                else:
                    print("Invalid selection, please choose a game")
            except ValueError:
                print("Please enter a number shown next to the game.")

        # Convert strings to grids for selected game
        user_grid = self.convert_board_to_grid(user_selection["User Board"])
        computer_grid = self.convert_board_to_grid(
            user_selection["Computer Board"]
            )

        # Rebuild user board for selected game
        user_board = self.board_size(user_selection)
        user_board.grid = user_grid
        user_board.num_ships = user_selection["Number of Ships"]

        # Rebuild computer board for selected game
        computer_board = self.board_size(user_selection)
        computer_board.grid = computer_grid
        computer_board.num_ships = user_selection["Number of Ships"]

        # Loaded board being displayed
        print(f"{player}'s board: {len(user_grid)}x{len(user_grid[0])}")
        user_board.display_board(show_ships=True)

        print(f"Computer board: {len(computer_grid)}x{len(computer_grid[0])}")
        computer_board.display_board(show_ships=False)

        return (
            user_board, computer_board, user_board.num_ships, user_hits,
            computer_hits
            )


def main():
    """
    Run all program functions
    """
    print(Style.BRIGHT + "Welcome to Ultimate Battleships!\n")
    intro()

    username = None

    while username is None:
        username = user_choice()
        if username is None:
            print("-" * 35)
            print("Login failed. Please try again.")
            print("-" * 35)

    loaded = Load_Games()
    games_saved = loaded.load_saved_games(username)

    if games_saved:
        while True:
            print("-" * 35)
            access_games = input(
                f"{username}, would you like to access any of your"
                " saved games?\n"
                f"If yes please enter '{Fore.GREEN}Y{Style.RESET_ALL}', if no"
                f" please enter '{Fore.RED}N{Style.RESET_ALL}':\n"
                ).strip()
            print("-" * 35)

            if access_games not in ("Y", "N"):
                print(
                    f"Please enter '{Fore.GREEN}Y{Style.RESET_ALL}' or"
                    f" '{Fore.RED}N{Style.RESET_ALL}' \n"
                    )
                continue
            elif access_games == "Y":
                saved_game_data = loaded.access_saved_games(username)
                user_board, computer_board, total_ships = (
                    saved_game_data[:3]
                )
                user_hits, computer_hits = (
                    saved_game_data[3:5]
                )
                if user_board and computer_board:
                    play_game(
                        username, user_board, computer_board, total_ships,
                        user_hits, computer_hits
                        )
                    break
            elif access_games == "N":
                print("-" * 35)
                print("Let's start a new game instead.")
                print("-" * 35)
                play_game(username)
                break
    else:
        print("-" * 35)
        print(f"Currently no saved games for {username}")
        print("-" * 35)
        play_game(username)

    game.exit_game(username)
    sys.exit()


# Checks to see if code is being used as a module or main program
if __name__ == "__main__":
    main()
