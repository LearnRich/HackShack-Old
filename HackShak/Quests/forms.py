from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

class QuestForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	description = TextAreaField('Description')
	xp = IntegerField('XP', validators=[DataRequired()])
	campaign = StringField('Campaign')
	expiry = StringField('Expiry')
	repeatable = StringField('Repeatable')
    # requirements -> this should be multiple foriegn keys 
	details = TextAreaField('Details', validators=[DataRequired()])
	submission_instructions = TextAreaField('Submission Instructions', validators=[DataRequired()])
	submit = SubmitField('Save')