from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import db, bcrypt, __STUDENT_ROLE, __TEACHER_ROLE, __ADMIN_ROLE
from ..models import Role, RoleAssignment, User, Teacher, Announcement, Student
from ..Auth.forms import LoginForm, UpdateProfileForm, RegistrationForm
from ..Auth.utils import roles_required, save_picture, splitme

teachers_bp = Blueprint(
	'teachers_bp', 
	__name__,
	url_prefix='/teacher/'
)


@teachers_bp.route('/teacher/courses/current')
@login_required
@roles_required([__TEACHER_ROLE])
def teacher_courses_current():
	teacher = Teacher.query.get_or_404(current_user.id)
	active_courses = []
	for course in teacher.courses:
		if not course.archived: 
			active_courses.append(course)
	return render_template('teacher_courses_current.html', courses=active_courses)

@teachers_bp.route('/teacher/courses/completed')
@login_required
@roles_required([__TEACHER_ROLE])
def teacher_courses_completed():
	teacher = Teacher.query.get_or_404(current_user.id)
	completed_courses = []
	for course in teacher.courses:
		if course.archived: 
			completed_courses.append(course)
	return render_template('teacher_courses_completed.html', courses=completed_courses)