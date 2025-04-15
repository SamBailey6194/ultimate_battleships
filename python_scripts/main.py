# Imported dependencies and modules
import time
# Imported other python scripts
from user import user_choice
from battleships import Game


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
    user_choice()


def main():
    """
    Run all program functions
    """
    print("Welcome to Ultimate Battleships!\n")
    intro()
    game = Game()
    game.play_game()


# Checks to see if code is being used as a module or main program
if __name__ == "__main__":
    main()
