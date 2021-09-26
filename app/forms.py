from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Regexp


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


class YogaForm(FlaskForm):

    user = StringField("User", validators=[DataRequired()])

    activity = SelectField(
        u"Wellness Activity",
        choices=["Yoga", "Meditation", "1 hour reading", "Strength training"],
    )

    submit = SubmitField("Submit completed wellness activity")


class PracticeForm(FlaskForm):

    user = StringField("User", validators=[DataRequired()])

    activity = SelectField(
        u"Wellness Activity", choices=["Poker", "Surfing", "Data Engineering", "Python"]
    )

    submit = SubmitField("Submit completed wellness activity")
