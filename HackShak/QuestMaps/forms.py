from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class QuestMapForm(FlaskForm):
    title = StringField('Quest Map Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')
