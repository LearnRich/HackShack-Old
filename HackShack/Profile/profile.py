from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required

from .. import db, __STUDENT_ROLE, __TEACHER_ROLE, __ADMIN_ROLE
from ..models import User, Student, Teacher
from .forms import UpdateProfileForm
from ..utils import save_picture
from ..Auth.utils import roles_required

profile_bp = Blueprint(
    'profile_bp',
    __name__,
    url_prefix='/profile/',
    template_folder='templates'
)

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
@roles_required([__STUDENT_ROLE])
def profile():
	student = Student.query.get_or_404(current_user.id)
	avatar_file = url_for('static', filename='profile_pics/' + current_user.avatar_file)
	return render_template('profile.html', title='Account', avatar_file=avatar_file, student=student)

@profile_bp.route('/update', methods=['GET', 'POST'])
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
		return redirect(url_for('pofile_bp.profile'))
	elif request.method == 'GET':
		form.username.data = student .username
		form.email.data = student.email 	

	
	avatar_file = url_for('static', filename='profile_pics/' + student.avatar_file)
	return render_template('profile_update.html', title='Edit Profile', 
							avatar_file=avatar_file, form=form)

# ---- Teacher ----

@profile_bp.route('/teacher/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def teacher_profile():
	teacher = Teacher.query.get_or_404(current_user.id)
	avatar_file = url_for('static', filename='profile_pics/' + current_user.avatar_file)
	return render_template('profile_teacher.html', title='Account', avatar_file=avatar_file, teacher=teacher)

@profile_bp.route('/teacher/update/', methods=['GET', 'POST'])
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
		return redirect(url_for('profile_bp.teacher_profile'))
	elif request.method == 'GET':
		form.username.data = current_user .username
		form.email.data = current_user.email 	
	
	avatar_file = url_for('static', filename='profile_pics/' + current_user.avatar_file)
	return render_template('profile_teacher_update.html', title='Edit Profile', 
							avatar_file=avatar_file, form=form)
