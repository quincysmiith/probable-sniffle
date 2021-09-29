import os

import gspread
import boto3
import pathlib
from dateutil import parser
import urllib.parse
import json
from haralyzer import HarParser

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

# <-------------- Helper functions for Har file parsing -------------->

def allowed_har_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'har'} #ALLOWED_EXTENSIONS


def parse_query_string(query_parameters: str) -> dict:
    """Converts a string that contains query parameters to a dictionary.
    Key value pairs must be seperated by "&"
    Keys and values must be seperated by "="

    Args:
        query_parameters (str): [description]

    Returns:
        dict: dictionary object representing the key value pairs from the original input
        string.
    """

    return_dict = {}

    for i in query_parameters.split("&"):
        # print(i)
        items = i.split("=", 1)
        # print(items)
        try:
            key = items[0]
            value = urllib.parse.unquote(items[1])
            if key == "t":
                value = parser.parse(value[:-7])
            return_dict.update({key: str(value)})
        except:
            pass
            # print("Failed to add to dict:")
            # print(items)
        # print()

    try:
        my_product_dict = parse_product_list(return_dict["products"])
        return_dict.update({"products": my_product_dict})
    except:
        pass

    return return_dict


def parse_product_list(product_string: str) -> dict:
    """Parses a product string and turns it into a dictionary format.

    Args:
        product_string (str): A product string from an adobe call that
        lists all the products listed on a search results page

    Returns:
        dict: [description]
    """

    if product_string[0] == ";":
        product_string = product_string[1:]

    main_dict = {}
    for num, i in enumerate(product_string.split(",;")):

        item_dict = {}

        if len(i.split(";;")) == 3:
            a_list = i.split(";;")
            item_dict.update({"Product": a_list[0]})
            item_dict.update({"Price": a_list[1]})

            # print(a_list[2])

            evar_list = a_list[2].split("|")

            evar_dict = {}
            for evar in evar_list:
                try:
                    items = evar.split("=", 1)
                    evar_dict.update({items[0]: items[1]})
                except:
                    pass
                    # print("Failed to parse")
                    # print(items)

        if len(i.split(";;")) == 1:
            a_list = i.split("|")
            item_dict.update({"Category": a_list[0]})

            evar_list = a_list[1:]

        if len(i.split(";;")) == 2:
            a_list = i.split(";;")[0]
            #print(a_list)
            first_variables = a_list.split(";")
            #print(first_variables)

            item_dict.update({"Product": first_variables[0]})
            item_dict.update({"Quantity": first_variables[1]})
            item_dict.update({"Price": first_variables[2]})

            evar_list = i.split(";;")[1].split("|")

        evar_dict = {}
        for evar in evar_list:
            try:
                items = evar.split("=", 1)
                evar_dict.update({items[0]: items[1]})
            except:
                print("Failed to parse")
                print(items)

        item_dict.update({"eVars": evar_dict})

        main_dict.update({num: item_dict})

    return main_dict


def extract_adobe_from_har(file_path_to_har_file):
    list_to_print = []

    with open(file_path_to_har_file, "r") as f:
        har_parser = HarParser(json.loads(f.read()))

    for har_page in har_parser.pages:

        ## POST requests
        post_requests = har_page.post_requests

        # filter for adobe hits
        adobe_post_hits = []
        for request in post_requests:
            if "https://woolworthsfoodgroup.sc.omtrdc" in request["request"]["url"]:
                adobe_post_hits.append(request)
                # print(json.dumps(request, indent=4))

        for adobe_post_hit in adobe_post_hits:
            query = parse_query_string(adobe_post_hit["request"]["postData"]["text"])

            list_to_print.append(query)

        ## GET requests
        get_requests = har_page.get_requests

        # filter adobe requests
        for request in get_requests:
            if "https://woolworthsfoodgroup.sc.omtrdc" in request["request"]["url"]:
                # print(request["request"]["url"])

                my_url = request["request"]["url"]
                parsed = urllib.parse.urlparse(my_url)

                data_sent = urllib.parse.unquote(str(parsed.query))
                query = parse_query_string(parsed.query)

                list_to_print.append(query)

    new_list = sorted(list_to_print, key=lambda k: k["t"])


    return new_list