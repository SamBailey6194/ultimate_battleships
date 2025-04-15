# Module to give access to google sheet
# Imported dependencies and modules
import gspread
from google.oauth2.service_account import Credentials

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
# List of variables to access specific sheets
user_logins_worksheet = SHEET.worksheet("userlogins")
saved_games = SHEET.worksheet("savedgames")
small_game_lb = SHEET.worksheet("5x5leaderboard")
medium_game_lb = SHEET.worksheet("10x10leaderboard")
big_game_lb = SHEET.worksheet("15x15leaderboard")
