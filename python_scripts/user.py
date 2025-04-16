# Imported dependencies and modules
import colorama
import re
import bcrypt
# Giving access to google drive and google sheets
from sheets import user_logins_worksheet


# Section that asks user for login information and verifies login credentials
# with the database
def login_credentials(username, password):
    """
    Verifying users login details with the google sheets database
    """
    users = user_logins_worksheet.get_all_records()
    for user in users:
        if user["Username"] == username:
            encrypt_pw = user["Password"].encode()
            if bcrypt.checkpw(password.encode(), encrypt_pw):
                return "Login successful"
    print("Invalid login credentials, please enter correct details.")
    user_choice()
    return "Invalid login credentials"


def user_login():
    """
    Allows user to login and access a previous game state
    or start a new game from scratch or access the leaderbaord.
    """
    global username
    username = str(input("Username: "))
    password = str(input("Password: "))
    result = login_credentials(username, password)
    if result == "Login successful":
        print(f"Welcome back {username}! Time to play the game.")
    else:
        username = None


def fetch_username():
    """
    Allows username to be accessed in other files
    """
    return username


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


def username_requirements():
    """
    Refactoring user_creation and putting the text for username
    requirements here
    """
    print("-" * 35)
    print("""Username requirements:
    Contain at least 1 uppercase and lowercase character
    No spaces allowed
        """)
    print("-" * 35)


def password_requirements():
    """
    Refactoring user_creation and putting the text for password
    requirements here
    """
    print("-" * 35)
    print("""Password requirements:
    8 characters long
    Contain at least 1 uppercase and lowercase character
    Contain at least 1 number
    Contain 1 special character
    No spaces allowed
          """)
    print("-" * 35)


def user_creation():
    """
    Allows a first time visitor to create a login so they can
    save a game start and register a score on the leaderboard
    """
    username_requirements()
    username = username_create()
    password_requirements()
    password = password_create()
    save_user(username, password)
    # Asks user to login once login credentials are correctly saved
    print("-" * 35)
    print("Login created. Please login now to enjoy the game.\n")
    print("-" * 35)
    user_login()


# Code that asks user if they have a login and then accesses the relevant
# functions above
def user_choice():
    """
    Allows user to declare if they are a returning user or a new user
    Then takes them to login or user creation.
    """
    while True:
        print("Have you already got a login?")
        login_option = input("If yes please enter Y, if no please enter N:\n")

        if login_option not in ("Y", "N"):
            print("Please enter Y or N\n")
            continue
        elif login_option == "Y":
            user_login()
            break
        elif login_option == "N":
            user_creation()
            break
