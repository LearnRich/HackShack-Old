from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed

class QuestForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	description = TextAreaField('Description')
	xp = IntegerField('XP', validators=[DataRequired()])
	campaign = SelectField('Campaign', validate_choice=False) 
	expiry = StringField('Expiry')
	repeatable = StringField('Repeatable')
	#requirements = SelectField('Requirements') 
	details = TextAreaField('Details', validators=[DataRequired()])
	submission_instructions = TextAreaField('Submission Instructions', validators=[DataRequired()])
	submit = SubmitField('Save')

class SubmissionForm(FlaskForm):
	submission_text = TextAreaField('Submission Text', validators=[DataRequired()])
	files = FileField('File(s) Upload')
	submit = SubmitField('Save')

class SubmissionReviewForm(FlaskForm):
	feedback_text = TextAreaField('Submission Text')
	awarded_xp = IntegerField('Award XP', validators=[Optional()])
	submit = SubmitField('Save')
