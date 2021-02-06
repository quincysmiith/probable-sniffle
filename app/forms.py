from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


class PercDiffForm(FlaskForm):
    orig = FloatField("Orignal value", validators = [DataRequired()])
    new = FloatField("New value", validators = [DataRequired()])
    submit = SubmitField('Submit')