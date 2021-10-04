from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required, login_user, logout_user
from HackShak import db, bcrypt, __STUDENT_ROLE
from HackShak.Users.models import Role, RoleAssignment, User
from HackShak.Users.forms import LoginForm, UpdateProfileForm, RegistrationForm
from HackShak.Users.utils import roles_required, save_picture, splitme
from HackShak.Announcements.models import Announcement

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():

		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		# I should be validating the role ... but too lazy to do it atm!!! Come back and fix this.
		# Should only be a role that currently extist
		# If this becomes a check box to allow multiple roles, cahnge this 
		role = Role(__STUDENT_ROLE)
		RoleAssignment.create(role.name, user.id)

		flash(f'Account has been created. Please inform the user about login infomration', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='User Registration', form=form)

@users.route('/login', methods=['GET', 'POST'])
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

@users.route('/logot')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('profile.html', title='Account', 
							image_file=image_file, form=form)

@users.route('/user/<string:username>/remove')
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

@users.route('/user/<string:username>')
def user_announcements(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	announcements = Announcement.query.filter_by(author=user)\
		.order_by(Announcement.date_posted.desc())\
		.paginate(page=page, per_page=5)
	return render_template('user_announcements.html', posts=announcements, user=user)

