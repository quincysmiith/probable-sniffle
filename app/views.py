from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from .forms import PercDiffForm, WeightForm, YogaForm
from .helpers import (
    google_sheets_connection,
    perc_diff,
    save_htmls_names_to_sheet,
    tidy_acceptable_users,
    allowed_har_file,
    extract_adobe_from_har,
)
from icecream import ic
from dateutil.parser import parse
from datetime import datetime
import os
import pathlib

# directory of script being run
path = os.path.abspath(os.path.dirname(__file__))

# directory to save files
upload_folder = pathlib.Path(path) / 'uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

main = Blueprint("main", __name__)


@main.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@main.route("/")
def main_index():
    return render_template("index.html")


# <------------------- Analytics Utilities ------------------->


@main.route("/percdiff", methods=["GET", "POST"])
def render():

    form = PercDiffForm()

    if form.validate_on_submit():
        orig = float(form.orig.data)
        new = float(form.new.data)

        results = perc_diff(orig, new)
        ic(results)

        return render_template("percdiff.html", form=form, something=results)

    return render_template("percdiff.html", form=form)


@main.route("/adobeparser")
def adobeparser():

    return render_template("adobeparser01.html")


### In progress endpoints


@main.route("/gtmhunter", methods=["GET", "POST"])
def gtmhunter():

    return render_template("404.html")


@main.route("/viewhtml/<id>")
def viewhtml(id):

    # save_htmls_names_to_sheet()
    html_list = get_html_list_from_sheets()

    single_html = html_list[id]

    return render_template("htmlviewer.html", single_html)




@main.route('/harparser', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_har_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, "temp.har"))

            # TO DO: parse har file and return json.
            parsed_har = extract_adobe_from_har(file_path_to_har_file=os.path.join(upload_folder, "temp.har"))
            #parsed_har = "A string"
            
            
            
            return render_template("harparser.html", display_results = parsed_har)

    return render_template("harparser.html")


# <------------------- Wellness Utilities ------------------->


@main.route("/weightlog", methods=["GET", "POST"])
def log_health_page():

    weight_form = WeightForm()

    if weight_form.validate_on_submit():
        gc = google_sheets_connection()
        sh = gc.open("Weight Logs")
        worksheet = sh.worksheet("Sheet1")

        user = weight_form.user.data
        weight = weight_form.weight.data
        a_date = weight_form.date.data
        try:
            my_date = parse(weight_form.date.data)
        except:
            ic("Unable to log the following:")
            ic(user)
            ic(weight)
            ic(a_date)
            return redirect(url_for("main.log_health_page"))
            # raise ValueError("Unable to parse date")

        # Only allow certain user names to submit

        if user.lower() in ["marquin", "quinny", "m", "quin"]:
            user = "marquin"
        if user.lower() in ["caroline", "caz", "cas", "c"]:
            user = "caroline"

        if user in ["marquin", "caroline"]:
            worksheet.append_row([user, str(my_date.date()), weight])

            my_message = f"{user} logged a weight of {weight} kgs on {my_date.date()}."
            flash(my_message)
            ic(my_message)

        return redirect(url_for("main.log_health_page"))

    return render_template("healthlog.html", weight_form=weight_form)


@main.route("/wellness", methods=["GET", "POST"])
def wellness():

    yoga_form = YogaForm()

    if yoga_form.validate_on_submit():
        gc = google_sheets_connection()
        sh = gc.open("Wellness Log")
        worksheet = sh.worksheet("Sheet1")

        user = yoga_form.user.data
        activity = yoga_form.activity.data
        a_date = str(datetime.utcnow().date())

        user = tidy_acceptable_users(user)

        if user in ["marquin", "caroline"]:
            worksheet.append_row([user, activity, a_date])

            my_message = f"{user} logged a {activity} activity on {a_date}."
            flash(my_message)
            ic(my_message)

        return redirect(url_for("main.wellness"))

    return render_template("wellnesslog.html", yoga_form=yoga_form)
