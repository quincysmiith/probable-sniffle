from flask import Blueprint, render_template, redirect, url_for, flash
from flask.helpers import url_for
from .forms import PercDiffForm, WeightForm
from .helpers import google_sheets_connection
from icecream import ic
from dateutil.parser import parse

main = Blueprint("main", __name__)


@main.route("/")
def main_index():
    return render_template("index.html")


@main.route("/percdiff", methods=["GET", "POST"])
def render():

    form = PercDiffForm()
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

    # exercise_form =

    return render_template("healthlog.html", weight_form=weight_form)
