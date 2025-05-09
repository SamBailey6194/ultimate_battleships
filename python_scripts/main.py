# This script brings together all the other scripts
# and then calls the functions in the correct order

# Imported dependencies and modules
import time
import sys
# Imported other python scripts
from style import init_styles, StyledText
from user import user_login, user_creation
from board_creation import BoardSetup
from game import Game
from save_load import LoadGames
import leaderboard


def intro():
    """
    Welcomes a the user to the game and then asks if they have
    logged in before or not
    """
    print("-" * 35)
    print(
        f"{StyledText.bold('Ultimate Battleships')} is a\n"
        "strategy guessing game for two players.\n"
        "\n"
        "This program allows you to play \n"
        "against a computer to practice.\n"
        "\n"
        "Once the game starts you will be \n"
        "able to pick a point to hit on the \n"
        "computers board.\n"
        "\n"
        "The aim of the game is to hit all \n"
        f"of the computers {StyledText.magenta('battleships')} before\n"
        "they hit all of yours.\n"
        )
    print("-" * 35)
    time.sleep(1.5)


def user_choice():
    """
    Allows user to declare if they are a returning user or a new user
    Then takes them to login or user creation.
    """
    while True:
        yes = StyledText.green("Y")
        no = StyledText.red("N")
        login_option = input(
            "Have you already got a login?\n"
            f"If yes please enter '{yes}',\n"
            f"if no please enter '{no}':\n"
            ).strip().lower()

        if login_option not in ("y", "n"):
            print(
                f"Please enter '{yes}' or"
                f" '{no}' \n"
                  )
            continue
        elif login_option == "y":
            return user_login()
        elif login_option == "n":
            return user_creation()


def exit_game(player):
    """
    Function that exits the game if player chose to save game instead
    """
    print("-" * 35)
    print(
        f"Thanks for playing {player}. \n"
        "Feel free to come back and access any \n"
        "saved games you have."
        )
    print("-" * 35)


def play_again_option(player):
    """
    Allows user to tell the program if they want to play again or exit the game
    """
    while True:
        play = StyledText.green("P")
        exit_ = StyledText.red("E")
        print("-" * 35)
        play_or_exit = input(
            "If you choose play again, you can either\n"
            "start a new game or load a saved game.\n"
            "\n"
            f"Please enter '{play}' to play again or\n"
            f"'{exit_}' to exit\n"
        ).strip().lower()
        if play_or_exit not in ("p", "e"):
            print(
                f"Please enter '{play}' or"
                f" '{exit_}' \n"
                  )
            continue
        elif play_or_exit == "p":
            return "play again"
        else:
            return "exit programme"


def leaderboard_generation(player, size):
    """
    Function to show leaderboard and allow user to search leaderboard
    """
    print("-" * 35)
    print(f"{player}, see how you did on the leaderboard below")
    print("-" * 35)
    leaderboard.show_lb(size)
    print(
        "When you are done searching the\n"
        "leaderboard you can either play again\n"
        "or exit.\n")


def game_is_save(
        game_id,
        player_board,
        pc_board
        ):
    """
    Refactored code to make full_game and new_game run better
    This handles checking whether a game is being resumed or not
    """
    return (
        game_id is not None and
        player_board is not None and
        pc_board is not None
        )


def save_setup(
        player,
        size,
        player_board,
        pc_board,
        game_id=None
        ):
    """
    Refactored code to make full_game and new_game run better
    This handles setting up the saved game properly.
    """
    return BoardSetup(
        player,
        size,
        player_board,
        pc_board,
        game_id=game_id
        )


def new_game(
        player,
        total_ships=0
        ):
    """
    Function ensures a new game is set up if there are no
    saved games or the user wants to start a new game instead
    of continuing a saved game
    """
    setup = BoardSetup(player, total_ships)
    player_board = setup.user_board()
    pc_board = setup.computer_board()
    total_ships = player_board.total_ships
    return setup, player_board, pc_board, total_ships


def game_starts(
        setup,
        size,
        user_hits,
        computer_hits,
        total_ships=0,
        ):
    """
    Refactored code to make full_game and new_game run better
    This handles starting the game and allowing the user to play
    the game.
    """
    game = Game(setup, user_hits, computer_hits)
    game.shot.reset_coordinates(size)
    battleships = game.gameplay.play_game()
    game.battleships = battleships
    return game


def game_result(
        game,
        player
        ):
    """
    Refactored code to make full_game and new_game run better
    This handles checking the result of the game.
    """
    battleships = game.battleships
    size = game.player_board.size

    if battleships == "saved" or battleships == "exit":
        return "exit game"
    elif battleships == "game over":
        leaderboard.update_lb(player, size, game.user_hits, game.computer_hits)
        leaderboard_generation(player, size)
        return "game completed"


def full_game(
        player,
        game_id=None,
        size=0,
        total_ships=0,
        player_board=None,
        pc_board=None,
        user_hits=0,
        computer_hits=0
        ):
    """
    Refactored code to make full_game and new_game run better
    This handles the starting point of the game and the result.
    """
    if game_is_save(game_id, player_board, pc_board):
        setup = save_setup(
            player,
            size,
            player_board,
            pc_board,
            game_id=game_id,
            )
    else:
        setup, player_board, pc_board, total_ships = new_game(
            player,
            total_ships
            )

    game = game_starts(
        setup,
        player_board.size,
        user_hits,
        computer_hits,
        total_ships=total_ships
        )

    return game_result(game, player)


def load_games_check(username, loads=None, saves=None):
    """
    Function that checks if user has any saved games
    """
    if saves:
        while True:
            yes = StyledText.green("Y")
            no = StyledText.red("N")
            print("-" * 35)
            access_games = input(
                f"{username}, would you like to access any of \n"
                "your saved games?\n"
                "\n"
                f"If yes please enter '{yes}', \n"
                f"if no please enter '{no}':\n"
                ).strip().lower()
            print("-" * 35)

            if access_games not in ("y", "n"):
                print(
                    f"Please enter '{StyledText.green("Y")}' or"
                    f" '{StyledText.red("N")}' \n"
                    )
                continue
            elif access_games == "y":
                saved_game_data = loads.access_saved_games()
                (
                    game_id,
                    username,
                    player_board,
                    computer_board,
                    _,
                    user_hits,
                    computer_hits,
                    available_coordinates
                    ) = saved_game_data

                if player_board and computer_board:
                    return True, {
                        "game_id": game_id,
                        "username": username,
                        "player_board": player_board,
                        "computer_board": computer_board,
                        "user_hits": user_hits,
                        "computer_hits": computer_hits,
                        "size": player_board.size,
                        "total_ships": player_board.total_ships,
                        "available_coordinates": available_coordinates
                    }
            elif access_games == "n":
                print("Let's start a new game instead.")
                print("-" * 35)
                return False, None

    else:
        print("-" * 35)
        print(f"Currently no saved games for {username}")
        print("-" * 35)
        return False, None


def main():
    """
    Run all program functions
    """
    print(StyledText.bold("Welcome to Ultimate Battleships!\n"))
    intro()

    username = None
    while username is None:
        username = user_choice()
        if username is None:
            print("-" * 35)
            print("Login failed. Please try again.")
            print("-" * 35)

    load_games = LoadGames(
        game_id=None,
        username=username,
        player_board=None,
        computer_board=None,
        games=None,
        player_colour=None,
        computer_colour=None
        )
    games_saved, _ = load_games.load_saved_games()

    while True:
        loaded_game, game_data = load_games_check(
            username, load_games, games_saved
            )
        if loaded_game:
            result = full_game(
                player=game_data["username"],
                game_id=game_data["game_id"],
                size=game_data["size"],
                total_ships=game_data["total_ships"],
                player_board=game_data["player_board"],
                pc_board=game_data["computer_board"],
                user_hits=game_data["user_hits"],
                computer_hits=game_data["computer_hits"]
            )
        else:
            result = full_game(username)

        if result == "exit game" or result == "game completed":
            if play_again_option(username) == "play again":
                games_saved, _ = load_games.load_saved_games()
                continue
            else:
                exit_game(username)
                sys.exit()


# Checks to see if code is being used as a module or main program
if __name__ == "__main__":
    init_styles()
    main()
