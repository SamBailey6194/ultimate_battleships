# Imported dependencies and modules
import time
import sys
# Imported other python scripts
from user import user_login, user_creation
from battleships import Game
import leaderboard

# Global variables for main.py
game = Game()
lb = leaderboard


def intro():
    """
    Welcomes a the user to the game and then asks if they have
    logged in before or not
    """
    print("-" * 35)
    print("""Battleships is a strategy guessing game for two players.
This program allows you to play against a computer to practice.
Once the game starts you will be able to pick a point to hit on
the computers board.
The aim of the game is to hit all of the computers battleships
before they hit all of yours.
          """)
    print("-" * 35)
    time.sleep(1.5)


def user_choice():
    """
    Allows user to declare if they are a returning user or a new user
    Then takes them to login or user creation.
    """
    while True:
        print("Have you already got a login?")
        login_option = input("If yes please enter Y, if no please enter N:\n")

        if login_option not in ("Y", "N"):
            print("Please enter 'Y' or 'N' \n")
            continue
        elif login_option == "Y":
            return user_login()
        elif login_option == "N":
            return user_creation()


def access_saved_games(player):
    """
    Loads the list of saved games associated with the username logged in with
    """
    


def returning_user(player):
    """
    Asks user if they want to load any of their saved games
    """
    if user_choice() == user_login():
        while True:
            print("-" * 35)
            print(f"""{player}, would you like to access any of your
saved games?
                """)
            access_games = input("""If yes please enter Y,
if no please enter N:\n
                        """)
            print("-" * 35)

            if access_games not in ("Y", "N"):
                print("Please enter 'Y' or 'N' \n")
                continue
            elif access_games == "Y":
                access_saved_games(player)
            elif access_games == "N":
                break


def leaderboard_generation(player, size):
    """
    Function to show leaderboard and allow user to search leaderboard
    """
    print("-" * 35)
    print(f"{player}, see how you did on the leaderboard below")
    print("-" * 35)
    lb.show_lb(size)
    print("-" * 35)
    print("""Can't see your score on the leaderboard you can search for it
using the serachbox below
        """)
    print("-" * 35)
    # print("-" * 35)
    # lb.search_lb()
    # print("-" * 35)


def play_game(player):
    """
    Starts the game and checks when the game finishes
    """
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
                player, user.size, user, computer,
                computer_ships_hit, user_ships_hit
                )

    leaderboard_generation(player, user.size)


def main():
    """
    Run all program functions
    """
    print("Welcome to Ultimate Battleships!\n")
    intro()

    username = None

    while username is None:
        username = user_choice()
        if username is None:
            print("-" * 35)
            print("Login failed. Please try again.")
            print("-" * 35)

    # returning_user(username)
    play_game(username)
    game.exit_game(username)
    sys.exit()


# Checks to see if code is being used as a module or main program
if __name__ == "__main__":
    main()
