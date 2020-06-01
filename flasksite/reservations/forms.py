from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired

class MakeReservationForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    start_time =StringField('Start Time', validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    submit = SubmitField('Reserve', validators=[DataRequired()])