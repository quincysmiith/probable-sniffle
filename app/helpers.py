import os

import gspread
import boto3
import pathlib

from .models import Html_Location


def google_sheets_connection():
    """Helper function to pull json credentials
    file from storage and authorise gspread library
    for Google Sheets manipulation.

    Returns:
        Authorised gspread account
        gc = gspread.service_account()
    """

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

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

    gc = gspread.service_account(filename="creds.json")

    return gc


def perc_diff(original_value: float, new_value: float) -> dict:
    """Calculates the volume difference and percentage difference
    of 2 values.

    Args:
        original_value (float): [description]
        new_value (float): [description]

    Returns:
        dict: [description]
    """

    volume_diff = new_value - original_value
    perc_diff = (new_value - original_value) / original_value
    perc_diff = perc_diff * 100

    if original_value == new_value:
        change_direction = "no change"
        volume_diff_txt = f"The new value of {new_value} and the original value of {original_value} are the same"
        perc_diff_txt = " "
    elif original_value < new_value:
        change_direction = "increase"
        volume_diff_txt = f"The new value of {new_value} is {volume_diff} bigger than the original value of {original_value}"
        perc_diff_txt = f"The new value of {new_value} is {perc_diff:.2f}% larger than the original value of {original_value}"
    elif original_value > new_value:
        change_direction = "decrease"
        volume_diff_txt = f"The new value of {new_value} is {volume_diff} smaller than the original value of {original_value}"
        perc_diff_txt = f"The new value of {new_value} is {perc_diff:.2f}% lower than the original value of {original_value}"

    return_dict = {}

    return_dict["change_direction"] = change_direction
    return_dict["volume_diff"] = volume_diff_txt
    return_dict["perc_diff"] = perc_diff_txt

    return return_dict


def do_spaces_auth():
    """Returns an authorised client for use with 
    interacting with Digital Ocean spaces
    """

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

    return client


def list_htmls_in_space():
    """[summary]
    """

    client = do_spaces_auth()
    to_return = []

    response = client.list_objects(Bucket="marquin-space-object-storage-01")
    for obj in response["Contents"]:
        if "web-resources/htmls/" in obj["Key"] and ".html" in obj["Key"]:
            temp = Html_Location([(obj["Key"])])
            to_return.append(temp)
            print(obj["Key"])

    return to_return


def save_htmls_names_to_sheet():
    """[summary]
    """

    gc = google_sheets_connection()
    sh = gc.open("html viewer")
    worksheet = sh.worksheet("Sheet1")

    html_list = list_htmls_in_space()

    range_to_update = "A1:B" + str(len(html_list))

    # for i in html_list:
    # worksheet.append_row(i)

    worksheet.update(range_to_update, html_list)

    return None


def get_html_list_from_sheets():
    """Retrives a list of html files from Google sheets
    that have been uploaded to Digital Ocean spaces
    """

    gc = google_sheets_connection()
    sh = gc.open("html viewer")
    worksheet = sh.worksheet("Sheet1")

    htmls = worksheet.col_values(1)

    htmls = [Html_Location(i) for i in htmls]

    return htmls


def tidy_acceptable_users(user: str):
    """Ensures that a given username is valid

    Args:
        username (str): [description]
    """

    assert type(user) == str, "User must be a string"

    if user.lower() in ["marquin", "quinny", "m", "quin"]:
        user = "marquin"
    if user.lower() in ["caroline", "caz", "cas", "c"]:
        user = "caroline"

    return user
