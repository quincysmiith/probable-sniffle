import os
import gspread
from google.oauth2 import service_account
from icecream import ic
import boto3
import pathlib


def google_sheets_connection():
    """Helper function to pull create json credentials
    file in temporary file and authorise gspread library
    for Google Sheets manipulation.

    Returns:
        Authorised gspread account
        gc = gspread.service_account()
    """

    my_dict = {}

    my_dict["type"] = os.getenv("TYPE")
    my_dict["project_id"] = os.getenv("PROJECT_ID")
    my_dict["private_key_id"] = os.getenv("PRIVATE_KEY_ID")
    my_dict["private_key"] = os.getenv("PRIVATE_KEY")
    my_dict["client_email"] = os.getenv("CLIENT_EMAIL")
    my_dict["client_id"] = os.getenv("CLIENT_ID")
    my_dict["auth_uri"] = os.getenv("AUTH_URI")
    my_dict["token_uri"] = os.getenv("TOKEN_URI")
    my_dict["auth_provider_x509_cert_url"] = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
    my_dict["client_x509_cert_url"] = os.getenv("CLIENT_X509_CERT_URL")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # ic(os.environ['GOOGLE_API_CREDS3'])

    # ic(os.environ['GOOGLE_API_CREDS2'].replace("'\'", "'"))

    """

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(
            os.environ['GOOGLE_API_CREDS2']),
        scopes = scopes)
    """

    # Download credentials file if not present
    file = pathlib.Path("creds.json")
    if not file.exists():

        # access environment variables
        key = os.getenv("DO_ACCESS_KEY")
        secret = os.getenv("DO_SECRET_KEY")

        session = boto3.session.Session()
        client = session.client(
            "s3",
            region_name="sgp1",
            endpoint_url="https://sgp1.digitaloceanspaces.com",
            aws_access_key_id=key,
            aws_secret_access_key=secret,
        )

        client.download_file(
            "marquin-space-object-storage-01",
            "web-resources/marquin-personal-tools-5f84ef73756b.json",
            "creds.json",
        )
    # else:
    # print ("File not exist")

    gc = gspread.service_account(filename="creds.json")

    # gc = gspread.authorize(credentials)
    """

    f = open("temp2.json", "a")
    #f.write(json.dumps(my_dict))
    json.dump(my_dict, f, indent = 6) 
    f.close()

    gc = gspread.service_account(filename="temp2.json")

    #os.remove("temp2.json")
    """

    # gc = gspread.service_account(filename='/home/fuzzy/Documents/Projects/flask_app_platform/marquin-personal-tools-5f84ef73756b.json')

    return gc
