# Imported dependencies and modules
import colorama
import gspread
from google.oauth2.service_account import Credentials
import re
import bcrypt

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
user_logins_worksheet = SHEET.worksheet("userlogins")


# Section that asks user for login information and verifies login credentials
# with the database
def user_choice():
    """
    Allows user to declare if they are a returning user or a new user
    Then takes them to login or user creation.
    """
    print("Have you already got a login?")
    login_option = input("If yes please enter Y, if no please enter N:\n")

    if login_option == "Y":
        user_login()
    elif login_option == "N":
        user_creation()
    else:
        print("Please enter Y or N\n")
        user_choice()


def login_credentials(username, password):
    """
    Verifying users login details with the google sheets database
    """
    users = user_logins_worksheet.get_all_records()
    for user in users:
        if user["Username"] == username:
            encrypt_pw = user["Password"].encode()
            if bcrypt.checkpw(password.encode(), encrypt_pw):
                print(f"{user} welcome back to Ultimate Battleships!")
                return "Login successful"
    print("Invalid login credentials, please enter correct details.")
    user_choice()
    return "Invalid login credentials"


def user_login():
    """
    Allows user to login and access a previous game state
    or start a new game from scratch or access the leaderbaord.
    """
    username = str(input("Username: "))
    password = str(input("Password: "))
    result = login_credentials(username, password)
    if result == "Login successful":
        return username
    else:
        return None


# Section that asks user to create login credentials and stores login
# credentials in the database
def encrypt_password(data):
    """
    Using bcrypt to hash and salt the password to safely store it.
    While converting the hash to a string so Google Sheets can read it.
    """
    byte_pwd = data.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byte_pwd, salt)
    return hashed.decode("utf-8")


def check_username(data):
    """
    Checks username meets criteria and if it already exists
    """
    usernames = user_logins_worksheet.col_values(1)
    if data in usernames:
        print(f"{data} is already in use, please create a new one")
        return False
    elif (len(data) >= 8):
        print(f"{data} must be no more than 8 characters long\n")
        return False
    elif re.search("[A-Z]", data) is None:
        print("Username must contain 1 uppercase character\n")
        return False
    elif re.search("[a-z]", data) is None:
        print("Username must contain 1 lowercase character\n")
        return False
    elif re.search(r"\s", data):
        print("Username can't have any spaces\n")
        return False
    elif re.fullmatch("[a-zA-Z]+", data):
        print(f"{data} is a valid username\n")
        return True
    else:
        print(f"{data} is an invalid username\n")
        return False


def check_password(data):
    """
    Checks password meets criteria
    """
    if (len(data) <= 8):
        print(f"{data} must be at least 8 characters long\n")
        return False
    elif re.search("[A-Z]", data) is None:
        print("Password must contain 1 uppercase character\n")
        return False
    elif re.search("[a-z]", data) is None:
        print("Password must contain 1 lowercase character\n")
        return False
    elif re.search(r"[\d]", data) is None:
        print("Password must contain 1 number\n")
        return False
    elif re.search(r"[!@#$£%^&*_-+=:;<>,.?~]", data) is None:
        print("Password must contain 1 special character\n")
        return False
    elif re.search(r"\s", data):
        print("Password can't have any spaces\n")
        return False
    elif re.fullmatch(r"[a-zA-Z0-9!@#$£%^&*_-+=:;<>,.?~]{8,}+", data):
        print(f"{data} is a valid password\n")
        return True
    else:
        print(f"{data} is an invalid password\n")
        return False


def save_user(username, password):
    """
    Save username created in Google Sheets
    """
    hashed_pw = encrypt_password(password)
    user_logins_worksheet.append_row([username, hashed_pw])


def username_create():
    """
    Username creation for first time user
    """
    while True:
        username = str(input("Create Username: "))
        if check_username(username):
            return username


def password_create():
    """
    Password creation for first time user
    """
    while True:
        password = str(input("Create Password: "))
        if check_password(password):
            return password


def user_creation():
    """
    Allows a first time visitor to create a login so they can
    save a game start and register a score on the leaderboard
    """
    print("-" * 35)
    print("""Username requirements:
    Contain at least 1 uppercase and lowercase character
    No spaces allowed
        """)
    print("-" * 35)
    username = username_create()
    print("-" * 35)
    print("""Password requirements:
    8 characters long
    Contain at least 1 uppercase and lowercase character
    Contain at least 1 number
    Contain 1 special character
    No spaces allowed
          """)
    print("-" * 35)
    password = password_create()
    save_user(username, password)
    print("-" * 35)
    print("You can login next time. Enjoy the game.\n")
    print("-" * 35)
    return username


# def get_username():
#     """
#     Allows other python files to retrieve the username
#     """
#     username = user_login() or user_creation()
#     return username
