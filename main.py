# Imported dependencies and modules
from random import randint
import colorama
import gspread
from google.oauth2.service_account import Credentials
import time
# Imported other python scripts
import user

# Giving python access to google sheet
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ultimate_battleships')
scores = {"computer": 0, "player": 0}


def intro():
    """
    Allow user to create a user name or access a previous
    saved game stored in the google sheet
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
    user.user_choice()


def main():
    """
    Run all program functions
    """
    print("Welcome to Ultimate Battleships!\n")
    intro()


# Checks to see if code is being used as a module or main program
if __name__ == "__main()__":
    main()
