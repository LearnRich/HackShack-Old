from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required, login_user, logout_user
from HackShak import db, bcrypt, __STUDENT_ROLE, __TEACHER_ROLE, __ADMIN_ROLE
from HackShak.models import Role, RoleAssignment, User, Student, Course
from HackShak.Users.forms import LoginForm, UpdateProfileForm, RegistrationForm
from HackShak.Users.utils import roles_required, save_picture, splitme
import re

users = Blueprint('users', __name__)

@users.route('/register/student/', methods=['GET', 'POST'])
def register_student_user():
	form = RegistrationForm()
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

@users.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		print(current_user, "is authenticated")
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		print(user)
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			print("logging user in")
			login_user(user, form.remember_me.data)
			print(current_user)
			next_page = request.args.get('next')

			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else: 
			flash('Login Unsuccessful, Please check username and password', 'danger')
	return render_template('login.html', title='User Login', form=form)

@users.route('/logout/')
def logout():
	logout_user()
	return redirect(url_for('users.login'))

@users.route('/profile/', methods=['GET', 'POST'])
@login_required
@roles_required([__STUDENT_ROLE])
def profile():
	student = Student.query.get_or_404(current_user.id)
	avatar_file = url_for('static', filename='profile_pics/' + current_user.avatar_file)
	return render_template('profile.html', title='Account', avatar_file=avatar_file, student=student)

@users.route('/profile/update', methods=['GET', 'POST'])
@login_required
@roles_required([__STUDENT_ROLE])
def update_profile():
	student = Student.query.get_or_404(current_user.id)
	form = UpdateProfileForm()

	years = list(range(datetime.today().year, datetime.today().year+6))
	default_pos = 0
	if student.grad_year  in years:
		default_pos = years.index(student.grad_year)
	else:
		years.insert(0, student.grad_year)

	form.grad_year.choices = years
	form.grad_year.default = default_pos

	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			student.avatar_file = picture_file
		student.username = form.username.data
		student.email = form.email.data
		student.grad_year = form.grad_year.data
		student.alias = form.alias.data
		student.preferred_firstname = form.preferred_firstname.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.profile'))
	elif request.method == 'GET':
		form.username.data = student .username
		form.email.data = student.email 	

	
	avatar_file = url_for('static', filename='profile_pics/' + student.avatar_file)
	return render_template('profile_update.html', title='Edit Profile', 
							avatar_file=avatar_file, form=form)

@users.route('/user/<string:username>/remove/')
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def remove_user(username):
	user = User.query.get_or_404(username=username)
	if user.author != current_user:
		abort(403)
	db.session.delete(user)
	db.session.commit()
	flash(f"The User {user.username} has been deleted.")
	return redirect(url_for('main.home'))


