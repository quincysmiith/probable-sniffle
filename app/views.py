from flask import Blueprint, render_template
from .forms import PercDiffForm

main = Blueprint('main', __name__)

@main.route('/')
def main_index():
    return 'Blueprint index endpoint'

@main.route('/percdiff')
def render():

    form = PercDiffForm()
    return render_template("index.html", form = form)

@main.route('/regular_html')
def render_something_else():
    return render_template("test_01.html")