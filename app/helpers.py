import os
import gspread
import boto3
import pathlib


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
