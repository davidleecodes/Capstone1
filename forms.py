from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Required, ValidationError, Length, NumberRange
from wtforms.fields.html5 import DateField
import datetime


class PetForm(FlaskForm):
    """Form for pet"""
    start_date = DateField('Start date', validators=[
                           Required()], default=datetime.date.today)
    end_date = DateField('End date', validators=[
                         Required()], default=datetime.date.today() + datetime.timedelta(days=1))

    def validate_start_date(form, field):
        if field.data < datetime.date.today():
            raise ValidationError(
                "Start date must today or later.")

    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            raise ValidationError(
                "End date must not be earlier than start date.")


class BookRatingForm(FlaskForm):
    """From for rating bookings"""
    rating = IntegerField('rating', validators=[NumberRange(min=0, max=5)])


class RenterForm(FlaskForm):
    """Form for adding editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    location = StringField('Location', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
