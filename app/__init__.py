from flask import Flask, Blueprint

from .views import main
from .helpers import perc_diff


def create_app(config_file="settings.py"):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(main)

    return app
