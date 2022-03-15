from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import db, bcrypt, __STUDENT_ROLE, __TEACHER_ROLE, __ADMIN_ROLE
from ..models import Role, RoleAssignment, Student, Course, Teacher
from ..Registration.forms import StudentRegistrationForm, TeacherRegistrationForm
from ..Auth.utils import roles_required

reg_bp = Blueprint('reg_bp', __name__,
    url_prefix='/registration/',
    template_folder='templates'
)

@reg_bp.route('/student/', methods=['GET', 'POST'])
def register_student():
	form = StudentRegistrationForm()
	if form.validate_on_submit():
		print("Valid Form")
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Student(username=form.username.data,
			firstname=form.firstname.data,
			lastname=form.lastname.data,
			email=form.email.data,
			grad_year=form.grad_year.data,
			password=hashed_password)
		db.session.add(user)
		db.session.commit()
		print(user)

		course = Course.query.filter_by(invite=form.invite.data).first()
		if course:
			course.students.append(user)
			db.session.commit()
		else:
			flash(f"An error occured and were unable to enroll in course. Please tell you teacher.", 'warning')

		role = Role(__STUDENT_ROLE)
		RoleAssignment.create(role.name, user.id)

		flash(f'Account has been created. Please inform the user about login information', 'success')
		return redirect(url_for('users.login'))
	else: 
		for fieldName, errorMessages in form.errors.items():
			for err in errorMessages:
				print(f"{fieldName}:{err}")
	return render_template('registration_student.html', title='Student Registration', form=form)

@reg_bp.route('/teacher/', methods=['GET', 'POST'])
@login_required
@roles_required(__ADMIN_ROLE)
def register_teacher():
	if not current_user.is_authenticated:
		return redirect(url_for('main_bp.home'))
	form = TeacherRegistrationForm()
	if form.validate_on_submit():

		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Teacher(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		role = Role(__TEACHER_ROLE)
		RoleAssignment.create(role.name, user.id)

		flash(f'Account has been created. Please inform the user about login infomration', 'success')
		#return redirect(url_for('auth_bp.login'))
	return render_template('register.html', title='User Registration', form=form)
