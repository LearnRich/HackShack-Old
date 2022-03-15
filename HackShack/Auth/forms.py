from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.core import RadioField, SelectField
from wtforms.fields.html5 import DateField  # to be used with Date Pickers at a later time.
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from ..models import User, Course
from flask_login import current_user
from datetime import datetime
import re


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Login')