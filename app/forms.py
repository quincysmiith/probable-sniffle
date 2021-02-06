from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


class PercDiffForm(FlaskForm):
    orig = FloatField("Orignal value", validators = [DataRequired()])
    new = FloatField("New value", validators = [DataRequired()])
    submit = SubmitField('Submit')


class WeightForm(FlaskForm):
    user = StringField("User", validators = [DataRequired()])
    weight = FloatField("Weight", validators = [DataRequired()])
    date = StringField("Date", validators = [DataRequired()])
    submit = SubmitField('Submit')