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
        user_creation()
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


def user_creation():
    """
    Allows a first time visitor to create a login so they can
    save a game start and register a score on the leaderboard
    """
    user_logins_worksheet = SHEET.worksheet("userlogins")

    def username_create():
        """
        Username creation for first time user
        """
        create_username = str(input("Create Username: "))
        check_username(create_username)
        save_user(create_username)

    def password_create():
        """
        Password creation for first time user
        """
        create_password = str(input("Create Password: "))
        check_password(create_password)
        save_user(create_password)

    def save_user(data):
        """
        Add username and password to google worksheet
        """
        user_logins_worksheet.insert_row(data)

    def check_username(data):
        """
        Checks username meets criteria
        """
        if (len(data) > 8):
            print(f"{data} must be less than 8 characters long\n")
            username_create()
        elif re.search("[A-Z]", data) is None:
            print("Username must contain 1 uppercase character\n")
            username_create()
        elif re.search("[a-z]", data) is None:
            print("Username must contain 1 lowercase character\n")
            username_create()
        elif re.search(r"\s", data):
            print("Username can't have any spaces\n")
            username_create()
        elif re.match("[a-z A-Z]", data):
            print(f"{data} is a valid username\n")
        else:
            print(f"{data} is an invalid username\n")
            username_create()

    def check_password(data):
        """
        Checks password meets criteria
        """
        if (len(data) <= 8):
            print(f"{data} must be at least 8 characters long\n")
            password_create()
        elif re.search("[A-Z]", data) is None:
            print("Password must contain 1 uppercase character\n")
            password_create()
        elif re.search("[a-z]", data) is None:
            print("Password must contain 1 lowercase character\n")
            password_create()
        elif re.search(r"[\d]", data) is None:
            print("Password must contain 1 number\n")
            password_create()
        elif re.search(r"[_!@#$£%&]", data) is None:
            print("Password must contain 1 special character\n")
            password_create()
        elif re.search(r"\s", data):
            print("Password can't have any spaces\n")
            password_create()
        elif re.match(r"[a-z A-Z 0-9 _!@#$£%&]{8}", data):
            print(f"{data} is a valid password\n")
        else:
            print(f"{data} is an invalid password\n")
            password_create()
    print("Username requirements:")
    print("Contain at least 1 uppercase and lowercase character")
    print("No spaces allowed\n")
    username_create()
    print("Password requirements:")
    print("8 characters long")
    print("Contain at least 1 uppercase and lowercase character")
    print("Contain at least 1 number")
    print("Contain 1 special character")
    print("No spaces allowed\n")
    password_create()


print("Welcome to Ultimate Battleships!\n")
intro()
