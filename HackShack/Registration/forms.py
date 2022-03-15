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

class StudentRegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	invite = StringField('Invite Code', validators=[DataRequired()])
	grad_year = SelectField('Grad Year', choices=list(range(datetime.today().year, datetime.today().year+6)), validate_choice=False)
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Create User')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists')

	def validate_invite(self, invite):
		course = Course.query.filter_by(invite=invite.data).first()
		if not course:
			raise ValidationError('Invalid Invite Code')

class TeacherRegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Create User')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists')
