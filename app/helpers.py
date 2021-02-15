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

    my_dict = {}

    my_dict['type'] = os.getenv("TYPE")
    my_dict['project_id'] = os.getenv("PROJECT_ID")
    my_dict['private_key_id'] = os.getenv("PRIVATE_KEY_ID")
    my_dict['private_key'] = os.getenv("PRIVATE_KEY")
    my_dict['client_email'] = os.getenv("CLIENT_EMAIL")
    my_dict['client_id'] = os.getenv("CLIEhttps://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-accountN_URI")
    my_dict['auth_provider_x509_cert_url'] = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
    my_dict['client_x509_cert_url'] = os.getenv("CLIENT_X509_CERT_URL")


    my_temp = tempfile.NamedTemporaryFile('w+')
    my_temp.write(json.dumps(my_dict))
    my_temp.seek(0)

    #gc = gspread.service_account(filename=my_temp.name)

    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]



    ic(os.environ['GOOGLE_API_CREDS2'])

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(
            os.environ['GOOGLE_API_CREDS2']),
        scopes = scopes)

    gc = gspread.authorize(credentials)
    

    #gc = gspread.service_account(filename='/home/fuzzy/Documents/Projects/flask_app_platform/marquin-personal-tools-5f84ef73756b.json')

    return gc


