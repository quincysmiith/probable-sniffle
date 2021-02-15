from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import url_for
from .forms import PercDiffForm, WeightForm
from .helpers import google_sheets_connection

main = Blueprint('main', __name__)

@main.route('/')
def main_index():
    return render_template("index.html")

@main.route('/percdiff', methods = ['GET', 'POST'])
def render():

    form = PercDiffForm()
    return render_template("percdiff.html", form = form)



@main.route('/weightlog', methods = ["GET", "POST"])
def log_health_page():

    weight_form = WeightForm()

    if weight_form.validate_on_submit():
        gc = google_sheets_connection()
        sh = gc.open("Weight Logs")
        worksheet = sh.worksheet("Sheet1")

        user = weight_form.user.data
        weight = weight_form.weight.data
        my_date = weight_form.date.data

        worksheet.append_row([user, my_date, weight])

        return redirect(url_for('main.log_health_page'))

    

    # exercise_form = 

    return render_template("healthlog.html", weight_form = weight_form)