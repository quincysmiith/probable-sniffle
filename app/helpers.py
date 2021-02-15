import os
import tempfile
import json
import gspread
from google.oauth2 import service_account
from icecream import ic

def google_sheets_connection():
    """Helper function to pull create json credentials
    file in temporary file and authorise gspread library
    for Google Sheets manipulation.

    Returns:
        Authorised gspread account
        gc = gspread.service_account()
    """



    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]



    ic(os.environ['GOOGLE_API_CREDS2'])

    ic(os.environ['GOOGLE_API_CREDS2'].replace("'\'", "'"))

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(
            os.environ['GOOGLE_API_CREDS2'].replace("'\'", "'")),
        scopes = scopes)

    gc = gspread.authorize(credentials)
    

    #gc = gspread.service_account(filename='/home/fuzzy/Documents/Projects/flask_app_platform/marquin-personal-tools-5f84ef73756b.json')

    return gc


