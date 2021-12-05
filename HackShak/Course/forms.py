from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired

BC_CURRICULUM_CHOICES = [
    ('ADST-8', 'ADST Grade 8'),
    ('ADST-9', 'ADST Grade 9'),
    ('ADST-ICT-CS-10', 'Computer Studies 10'),
    ('ADST-ICT-MD-10', 'Media Design 10'),
    ('ADST-ICT-WD-10', 'Web Development 10'),
    ('ADST-ICT-CIS-11', 'Computer Information Systems 11'),
    ('ADST-ICT-CP-11', 'Computer Programming 11'),
    ('ADST-ICT-DC-11', 'Digital Communication 11'),
    ('ADST-ICT-GP-11', 'Graphic Production 11'),
    ('ADST-ICT-MD-11', 'Media Design 11'),
    ('ADST-ICT-CIS-12', 'Computer Information Systems 12'),
    ('ADST-ICT-CP-12', 'Computer Programming 12'),
    ('ADST-ICT-DMD-12', 'Digital Media Development 12'),
    ('ADST-ICT-GP-12', 'Graphic Production 12'),
    ('ADST-ICT-MD-12', 'Media Design 12'),
]

class CourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    course_code = StringField('Course Code')
    description = TextAreaField('Description')
    block = IntegerField('Block', validators=[DataRequired()])
    term = StringField('Term', validators=[DataRequired()])
    grade = StringField('Grade', validators=[DataRequired()])
    bc_curriculum = SelectField('Apply BC Curriculum Document', validators=[DataRequired()], choices=BC_CURRICULUM_CHOICES)
    submit = SubmitField('Save')
