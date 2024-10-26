from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField
from wtforms.validators import ValidationError, Length, DataRequired

class CheckinForm(FlaskForm):
    first_name     = StringField('First Name', [Length(min=1, max=25), DataRequired()])
    last_name      = StringField('Last Name', [Length(min=1, max=35), DataRequired()])
    conf_num       = StringField('Confirmation Number', [Length(min=6, max=6), DataRequired()])
    flight_time    = TimeField('Flight Departure Time', [DataRequired()], format='%H:%M')
    flight_date    = DateField('Flight Departure Date', [DataRequired()], format='%Y-%m-%d')
    submit         = SubmitField('Check in to flight')

