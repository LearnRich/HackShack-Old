from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required, login_user, logout_user
from HackShak import db, bcrypt, __STUDENT_ROLE, __TEACHER_ROLE, __ADMIN_ROLE
from HackShak.models import Role, RoleAssignment, User, Teacher, Announcement
from HackShak.Users.forms import LoginForm, UpdateProfileForm, RegistrationForm
from HackShak.Users.utils import roles_required, save_picture, splitme

teachers = Blueprint('teachers', __name__)

@teachers.route('/register/teacher/', methods=['GET', 'POST'])
@login_required
@roles_required(__ADMIN_ROLE)
def register_teacher():
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


@teachers.route('/teacher/profile/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def teacher_profile():
	teacher = Teacher.query.get_or_404(current_user.id)
	avatar_file = url_for('static', filename='profile_pics/' + current_user.avatar_file)
	return render_template('profile_teacher.html', title='Account', avatar_file=avatar_file, teacher=teacher)

@teachers.route('/teacher/profile/update', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def teacher_profile_update():
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


@teachers.route('/teacher/courses/current')
@login_required
@roles_required([__TEACHER_ROLE])
def teacher_courses_current():
	teacher = Teacher.query.get_or_404(current_user.id)
	active_courses = []
	for course in teacher.courses:
		if not course.archived: 
			active_courses.append(course)
	return render_template('teacher_courses_current.html', courses=active_courses)

@teachers.route('/teacher/courses/completed')
@login_required
@roles_required([__TEACHER_ROLE])
def teacher_courses_completed():
	teacher = Teacher.query.get_or_404(current_user.id)
	completed_courses = []
	for course in teacher.courses:
		if course.archived: 
			completed_courses.append(course)
	return render_template('teacher_courses_completed.html', courses=completed_courses)