from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.core import RadioField, SelectField
from wtforms.fields.html5 import DateField  # to be used with Date Pickers at a later time.
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from HackShak.models import User
from flask_login import current_user


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	# user_type= RadioField("User Type", validators=[DataRequired], choices=[('student', 'Student'), ('teacher', 'Teacher')])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	# role = SelectField('Role', choices=[('student', 'Student'), ('reader', 'Reader'), ('reviewer','Reviewer'), ('manager','Manager'), ('admin','Administrator')], validators=[DataRequired()])
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

class UpdateProfileForm(FlaskForm):
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
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
				raise ValidationError('Email already exists')