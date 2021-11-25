from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required, login_user, logout_user
from HackShak import db, bcrypt, __STUDENT_ROLE, __TEACHER_ROLE, __ADMIN_ROLE
from HackShak.models import Role, RoleAssignment, User, Student, Teacher, Announcement
from HackShak.Users.forms import LoginForm, UpdateProfileForm, RegistrationForm
from HackShak.Users.utils import roles_required, save_picture, splitme
import re

users = Blueprint('users', __name__)

@users.route('/register/student/', methods=['GET', 'POST'])
def register_student_user():
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():

		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Student(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		role = Role(__STUDENT_ROLE)
		RoleAssignment.create(role.name, user.id)

		flash(f'Account has been created. Please inform the user about login infomration', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='User Registration', form=form)

@users.route('/register/teacher/', methods=['GET', 'POST'])
@login_required
@roles_required(__ADMIN_ROLE)
def register_teacher_user():
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():

		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Teacher(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		role = Role(__TEACHER_ROLE)
		RoleAssignment.create(role.name, user.id)

		flash(f'Account has been created. Please inform the user about login infomration', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='User Registration', form=form)


# Register Admin
# At this time the only way to create an admin user is to access the DB directly || to add that user to the create_db script and rebuild the system

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
	return redirect(url_for('main.home'))

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
	if current_user.grad_year  in years:
		default_pos = years.index(current_user.grad_year)
	else:
		years.insert(0, current_user.grad_year)

	form.grad_year.choices = years
	form.grad_year.default = default_pos

	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.avatar_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.grad_year = form.grad_year.data
		current_user.alias = form.alias.data
		current_user.preferred_firstname = form.preferred_firstname.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.profile'))
	elif request.method == 'GET':
		form.username.data = current_user .username
		form.email.data = current_user.email 	

	
	avatar_file = url_for('static', filename='profile_pics/' + current_user.avatar_file)
	return render_template('edit_profile.html', title='Edit Profile', 
							avatar_file=avatar_file, form=form)

@users.route('/teacher/profile/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def teacher_profile():
	teacher = Teacher.query.get_or_404(current_user.id)
	avatar_file = url_for('static', filename='profile_pics/' + current_user.avatar_file)
	return render_template('profile_teacher.html', title='Account', avatar_file=avatar_file, teacher=teacher)

@users.route('/teacher/profile/update', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def update_teacher_profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.avatar_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.alias = form.alias.data
		current_user.preferred_firstname = form.preferred_firstname.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.profile'))
	elif request.method == 'GET':
		form.username.data = current_user .username
		form.email.data = current_user.email 	
	
	avatar_file = url_for('static', filename='profile_pics/' + current_user.avatar_file)
	return render_template('edit_profile.html', title='Edit Profile', 
							avatar_file=avatar_file, form=form)


@users.route('/user/<string:username>/remove/')
@login_required
@roles_required(['admin', 'manager'])
def remove_user(username):
	user = User.query.get_or_404(username=username)
	if user.author != current_user:
		abort(403)
	db.session.delete(user)
	db.session.commit()
	flash(f"The User {user.username} has been deleted.")
	return redirect(url_for('main.home'))

@users.route('/user/<string:username>/')
def user_announcements(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	announcements = Announcement.query.filter_by(announcement_author=user)\
		.order_by(Announcement.date_posted.desc())\
		.paginate(page=page, per_page=5)
	return render_template('user_announcements.html', announcements=announcements, user=user)

