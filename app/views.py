from flask import Blueprint, render_template, redirect, url_for, flash
from flask.helpers import url_for
from .forms import PercDiffForm, WeightForm, YogaForm
from .helpers import (
    google_sheets_connection,
    perc_diff,
    save_htmls_names_to_sheet,
    tidy_acceptable_users,
)
from icecream import ic
from dateutil.parser import parse
from datetime import datetime

main = Blueprint("main", __name__)


@main.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@main.route("/")
def main_index():
    return render_template("index.html")


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


@main.route("/gtmhunter", methods=["GET", "POST"])
def gtmhunter():

    return render_template("404.html")


@main.route("/viewhtml/<id>")
def viewhtml(id):

    # save_htmls_names_to_sheet()
    html_list = get_html_list_from_sheets()

    single_html = html_list[id]

    return render_template("htmlviewer.html", single_html)


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
