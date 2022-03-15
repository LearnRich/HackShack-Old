from datetime import datetime
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.core import RadioField, SelectField
from wtforms.fields.html5 import DateField  # to be used with Date Pickers at a later time.
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
import re

from ..models import User




class UpdateProfileForm(FlaskForm):
	picture = FileField('Avatar', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	preferred_firstname = StringField('Preferred first name', validators=[Length(max=50)], \
		description='If you would prefer your teacher to call you by a name other than the name your school records, please put it here.')
	preferred_name_internal = BooleanField('Use Preferred first name internally only')
	alias = StringField('Alias', validators=[Length(max=50)], \
		description='You can leave this blank, or enter anything you like here.')
	grad_year = SelectField('Grad Year', validators=[DataRequired()], validate_choice=False)
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already exists')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already exists.')
	
	def validate_grad_year(self, grad_year):
		year = grad_year.data
		print(year)
		print(re.match('^[1-9]\d{3,}$', str(year)))

		if not re.match('^[1-9]\d{3,}$', str(year)):
			raise ValidationError('That is not a valid year.')