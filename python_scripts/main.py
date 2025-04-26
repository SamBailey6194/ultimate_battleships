# This script brings together all the other scripts
# and then calls the functions in the correct order

# Imported dependencies and modules
import colorama
from colorama import Fore, Style
import time
import sys
# Imported other python scripts
from user import user_login, user_creation
from game_logic import Game
from board_creation import Load_Games
import leaderboard

# Initialise colorama
colorama.init(autoreset=True)

# Global variables for main.py
lb = leaderboard


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


def exit_game(player):
    """
    Function that exits the game if player chose to save game instead
    """
    print("-" * 35)
    print(
        f"Thanks for playing {player}. Feel free to come back and access"
        " any saved games you have."
        )
    print("-" * 35)


def play_again_option(player):
    """
    Allows user to tell the program if they want to play again or exit the game
    """
    while True:
        play_or_exit = input(
            "Would you like to play again or exit the game?\n"
            f"Please enter '{Fore.GREEN}P{Style.RESET_ALL}' to play again or"
            f"'{Fore.RED}E{Style.RESET_ALL}' to exit: \n"
        )
        if play_or_exit not in ("P", "E"):
            continue
        elif play_or_exit == "P":
            full_game(player)
            continue
        else:
            exit_game(player)
            sys.exit()


def leaderboard_generation(player, size):
    """
    Function to show leaderboard and allow user to search leaderboard
    """
    print("-" * 35)
    print(f"{player}, see how you did on the leaderboard below")
    print("-" * 35)
    lb.show_lb(size)
    # print("-" * 35)
    # user_search = input(
    #   "Can't see your score on the leaderboard you can search for it using\n"
    #     " the serachbox below.\n"
    #     "Type your username here to see where you stand:\n"
    #     )
    # print("-" * 35)
    # lb.search_lb(user_search, size)
    print("-" * 35)
    print(
        "When you are done searching the leaderboard you can either play again"
        " or exit.\n")
    play_again_option(player)


def full_game(
        player, size=None, total_ships=None,
        player_board=None, pc_board=None,
        user_hits=None, computer_hits=None
        ):
    """
    Starts or resumes the game and checks when the game finishes
    """
    game = Game(
        player, total_ships, player_board, pc_board, user_hits, computer_hits
        )
    battleships = game.play_game()

    if player_board:
        if size is None:
            size = player_board.size
        if total_ships is None:
            total_ships = player_board.num_ships

    if battleships == "saved" or battleships == "exit":
        play_again_option(player)
    elif battleships == "game over":
        lb.update_lb(player, size, game.user_hits, game.computer_hits)
        leaderboard_generation(player, size)


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

    loaded = Load_Games(
        username, player_board=None, computer_board=None,
        games=None, player_colour=None, computer_colour=None
        )
    games_saved = loaded.load_saved_games()

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
                saved_game_data = loaded.access_saved_games()
                player_board, computer_board, total_ships = (
                    saved_game_data[:3]
                )
                user_hits, computer_hits = (
                    saved_game_data[3:5]
                )
                if player_board and computer_board:
                    full_game(
                        username,
                        size=player_board.size,
                        total_ships=total_ships,
                        player_board=player_board,
                        pc_board=computer_board,
                        user_hits=user_hits,
                        computer_hits=computer_hits
                        )
            elif access_games == "N":
                print("-" * 35)
                print("Let's start a new game instead.")
                print("-" * 35)
                full_game(username)
    else:
        print("-" * 35)
        print(f"Currently no saved games for {username}")
        print("-" * 35)
        full_game(username)


# Checks to see if code is being used as a module or main program
if __name__ == "__main__":
    main()
