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
user_logins_worksheet = SHEET.worksheet("userlogins")
usernames = user_logins_worksheet.col_values(1)
string = " ".join(map(str, usernames))
print(string)
