# This script brings together all the other scripts
# and then calls the functions in the correct order

# Imported dependencies and modules
import time
import sys
# Imported other python scripts
from style import StyledText
from user import user_login, user_creation
from board_creation import BoardSetup
from game import Game
from game_logic import Gameplay
from save_load import LoadGames
import leaderboard


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
        yes = StyledText.green("Y")
        no = StyledText.red("N")
        login_option = input(
            "Have you already got a login?\n"
            f"If yes please enter '{yes}', if no"
            f" please enter '{no}':\n"
            ).strip()

        if login_option not in ("Y", "N"):
            print(
                f"Please enter '{yes}' or"
                f" '{no}' \n"
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
        play = StyledText.green("P")
        exit_ = StyledText.red("E")
        play_or_exit = input(
            "Would you like to play again or exit the game?\n"
            f"Please enter '{play}' to play again or"
            f"'{exit_}' to exit: \n"
        )
        if play_or_exit not in ("P", "E"):
            print(
                f"Please enter '{play}' or"
                f" '{exit_}' \n"
                  )
            continue
        elif play_or_exit == "P":
            load_games_check(player)
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
    leaderboard.show_lb(size)
    print("-" * 35)
    print(
        "When you are done searching the leaderboard you can either play again"
        " or exit.\n")
    play_again_option(player)


def full_game(
        player, game_id=None, size=None, total_ships=0,
        player_board=None, pc_board=None,
        user_hits=0, computer_hits=0
        ):
    """
    Starts or resumes the game and checks when the game finishes
    """
    setup = BoardSetup(
        player,
        size,
        total_ships,
        player_board,
        pc_board,
        game_id=game_id
        )
    game = Game(setup, user_hits, computer_hits)
    gameplay = Gameplay(game)
    battleships = gameplay.play_game()

    if battleships == "saved" or battleships == "exit":
        if play_again_option(player):
            return True
    elif battleships == "game over":
        leaderboard.update_lb(player, size, game.user_hits, game.computer_hits)
        leaderboard_generation(player, size)


def new_game(
        player,
        total_ships=0,
        player_board=None,
        pc_board=None,
        ):
    """
    Function ensures a new game is set up if there are no
    saved games or the user wants to start a new game instead
    of continuing a saved game
    """
    setup = BoardSetup(player, total_ships, player_board, pc_board)
    user = setup.user_board()
    computer = setup.computer_board(user.size, user.num_ships)
    full_game(
        player,
        total_ships=user.num_ships,
        player_board=user,
        pc_board=computer
        )


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
                f"{username}, would you like to access any of your"
                " saved games?\n"
                f"If yes please enter '{yes}', if no"
                f" please enter '{no}':\n"
                ).strip()
            print("-" * 35)

            if access_games not in ("Y", "N"):
                print(
                    f"Please enter '{StyledText.green("Y")}' or"
                    f" '{StyledText.red("N")}' \n"
                    )
                continue
            elif access_games == "Y":
                saved_game_data = loads.access_saved_games()
                (
                    game_id,
                    username,
                    player_board,
                    computer_board,
                    _,
                    user_hits,
                    computer_hits
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
                        "total_ships": player_board.num_ships
                    }
            elif access_games == "N":
                print("-" * 35)
                print("Let's start a new game instead.")
                print("-" * 35)
                new_game(username)
                return False, None

    else:
        print("-" * 35)
        print(f"Currently no saved games for {username}")
        print("-" * 35)
        new_game(username)
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
            continue_loaded_game = full_game(
                player=game_data["username"],
                game_id=game_data["game_id"],
                size=game_data["size"],
                total_ships=game_data["total_ships"],
                player_board=game_data["player_board"],
                pc_board=game_data["computer_board"],
                user_hits=game_data["user_hits"],
                computer_hits=game_data["computer_hits"],
            )
        else:
            continue_loaded_game = new_game(username)

        if not continue_loaded_game:
            break


# Checks to see if code is being used as a module or main program
if __name__ == "__main__":
    StyledText.init_styles()
    main()
