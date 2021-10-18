from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Regexp
from datetime import datetime


class PercDiffForm(FlaskForm):
    orig = FloatField("Orignal value", validators=[DataRequired()])
    new = FloatField("New value", validators=[DataRequired()])
    submit = SubmitField("Submit")


class WeightForm(FlaskForm):

    user = StringField("User", validators=[DataRequired()])
    weight = FloatField(
        "Weight", validators=[DataRequired(), NumberRange(min=0, max=150)]
    )
    date = StringField(
        "Date",
        validators=[
            DataRequired(),
            Regexp(
                "(\d{4}|\d{2})(\/|-|\.)\d{2}(\/|-|\.)\d{2}",
                message="Date should be in format YYYY-MM-DD",
            ),
        ],
    )
    submit = SubmitField("Submit")

    def __init__(self):
        super().__init__()
        # ensure default date in field is always updated.
        if not self.date.data:
            self.date.data = str(datetime.utcnow().date())


class YogaForm(FlaskForm):

    user = StringField("User", validators=[DataRequired()])

    activity = SelectField(
        u"Wellness Activity",
        choices=["Yoga", "Meditation", "1 hour reading", "Strength training"],
    )

    submit = SubmitField("Submit wellness activity")


class MovementPracticeForm(FlaskForm):

    user = StringField("User", validators=[DataRequired()])

    activity = SelectField(
        u"Practice Activity",
        choices=[
            "Handstand",
            "L-sit",
            "Pistol Squat",
            "Poker",
            "Surfing",
            "Data Engineering",
            "Python",
        ],
    )

    submit = SubmitField("Submit practice")
