from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class CampaignForm(FlaskForm):
    title = StringField('Campaign Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')
