from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user

from .. import bcrypt
from ..models import User
from .forms import LoginForm

auth_bp = Blueprint('auth_bp', __name__,
	url_prefix='/auth/',
	template_folder='templates'
)



@auth_bp.route('/login/', methods=['GET', 'POST'])
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

@auth_bp.route('/logout/')
def logout():
	logout_user()
	return redirect(url_for('users.login'))
