# Imported dependencies and modules
import time
# Imported other python scripts
from user import user_choice, fetch_username
from battleships import Game
from leaderboard import search_lb


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


def main():
    """
    Run all program functions
    """
    print("Welcome to Ultimate Battleships!\n")
    intro()
    username = user_choice()
    player = fetch_username(username)
    game = Game()
    game.play_game(player)
    print("-" * 35)
    print("""Can't see your score on the leaderboard you can search for it
    using the serachbox below
          """)
    print("-" * 35)
    print("-" * 35)
    # search_lb()
    print("-" * 35)


# Checks to see if code is being used as a module or main program
if __name__ == "__main__":
    main()
