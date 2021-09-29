from flask import Flask, Blueprint
import os


from .views import main
from .helpers import perc_diff




ALLOWED_EXTENSIONS = {'har'}

def create_app(config_file="settings.py"):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(main)

    return app
