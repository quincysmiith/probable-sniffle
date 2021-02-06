from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import url_for
from .forms import PercDiffForm, WeightForm

main = Blueprint('main', __name__)

@main.route('/')
def main_index():
    return render_template("index.html")

@main.route('/percdiff', methods = ['GET', 'POST'])
def render():

    form = PercDiffForm()
    return render_template("percdiff.html", form = form)



@main.route('/healthlog')
def log_health_page():

    weight_form = WeightForm()

    # exercise_form = 

    return render_template("healthlog.html", weight_form = weight_form)


@main.route('/weightlog', methods = ['POST'])
def save_weight():
    # some logic to save entered data

    return redirect(url_for('main.log_health_page'))