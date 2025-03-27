# Imported dependencies and modules
from random import randint
import colorama
import gspread
from google.oauth2.service_account import Credentials
import re

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


def intro():
    """
    Allow user to create a user name or access a previous
    saved game stored in the google sheet
    """
    print("Battleships is a strategy guessing game for two players.")
    print("This program allows you to play against a computer to practice.")
    print("Once the game starts you will be able to pick a point to hit on")
    print("the computers board.")
    print("The aim of the game is to hit all of the computers battleships")
    print("before they hit all of yours.\n")
    print("Have you already got a login?")
    login_option = input("If yes please enter Y, if no please enter N:\n")

    if login_option == "Y":
        login()
    elif login_option == "N":
        user_create()
    elif login_option != "Y" or "N":
        print("Please enter Y or N\n")
        intro()


def login():
    """
    Allows user to login and access a previous game state
    or start a new game from scratch or access the leaderbaord.
    """
    ask_username = str(input("Username: "))
    ask_password = str(input("Passowrd: "))


def user_create():
    """
    Allows a first time visitor to create a login so they can
    save a game start and register a score on the leaderboard
    """
    create_username = str(input("Create Username: "))
    print()
    create_password = str(input("Create Password: "))

    check_username(create_username)
    check_password(create_password)


def check_username(data):
    """
    Checks username meets criteria
    """
    flag = 0
    while True:
        if (len(data) >= 8):
            flag = 1
            break
        elif not re.search(r"\s", data):
            flag = 1
            break
        else:
            flag = 0
            print(f"Valid {data}")
            break
    if flag == 1:
        print(f"Not a valid {data}")


def check_password(data):
    """
    Checks password meets criteria
    """
    flag = 0
    while True:
        if (len(data) <= 8):
            flag = -1
            break
        elif not re.search("[a-z]", data):
            flag = -1
            break
        elif not re.search("[A-Z]", data):
            flag = -1
            break
        elif not re.search("[0-9]", data):
            flag = -1
            break
        elif not re.search("[_@$]", data):
            flag = -1
            break
        elif not re.search(r"\s", data):
            flag = -1
            break
        else:
            flag = 0
            print(f"Valid {data}")
            break
    if flag == -1:
        print(f"Not a valid {data}")


print("Welcome to Ultimate Battleships!\n")
intro()
