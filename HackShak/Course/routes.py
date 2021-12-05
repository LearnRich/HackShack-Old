from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from HackShak import __ADMIN_ROLE, __TEACHER_ROLE
from flask_login import current_user, login_required
from HackShak import db
from HackShak.Users.utils import roles_required
from HackShak.models import Course, Teacher, QuestSubmission, SubmissionStatus
from HackShak.Course.forms import CourseForm

courses = Blueprint('courses', __name__)

@courses.route('/course/create/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def course_create():
	form = CourseForm()
	teacher = Teacher.query.get(current_user.id)
	if form.validate_on_submit():
		course = Course(
			course_code = form.course_code.data,
			course_name = form.course_name.data, 
			description=form.description.data, 
			block=form.block.data, 
			term=form.term.data, 
			grade=form.grade.data,
			bc_curriculum = form.bc_curriculum.data
		)
		db.session.add(course)
		course.teachers.append(teacher)
		db.session.commit()

		flash(f'Course [{course.course_name}] has been created', 'success')
		return redirect(url_for('teachers.teacher_courses_current'))
	return render_template('course_create.html', form=form, title='New Course', legend='New Course')

@courses.route('/course/<int:course_id>/details')
@login_required
@roles_required([__TEACHER_ROLE])
def course_details(course_id):
	course = Course.query.get_or_404(course_id)
	return render_template('course_details.html', course=course)

@courses.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def course_update(course_id):
	form = CourseForm()
	course = Course.query.get_or_404(course_id)
	teacher = Teacher.query.get_or_404(current_user.id)

	if teacher not in course.teachers:
		abort(403)

	if form.validate_on_submit():
		course.course_code = form.course_code.data
		course.course_name = form.course_name.data
		course.grade = form.grade.data
		course.term = form.term.data
		course.block = form.block.data
		course.bc_curriculum = form.bc_curriculum.data
		db.session.commit()
		flash(f'Course [{course.course_name}] has been update', 'success')
		return redirect(url_for('teachers.teacher_courses_current'))
	elif request.method == 'GET':
		form.course_code.data = course.course_code
		form.course_name.data = course.course_name
		form.description.data = course.description
		form.block.data = course.block
		form.term.data = course.term
		form.grade.data = course.grade
		form.bc_curriculum.default = course.bc_curriculum

	return render_template('course_create.html', form=form, title='Update Course', legend='Update Course')

@courses.route('/course/<int:course_id>/studentlist')
@login_required
@roles_required([__TEACHER_ROLE])
def course_studentlist(course_id):
	course=Course.query.get_or_404(course_id)
	return render_template('course_studentlist.html', course=course)

@courses.route('/course/<int:course_id>/quests/submissions')
@login_required
@roles_required([__TEACHER_ROLE])
def course_quest_submissions(course_id):
	course=Course.query.get_or_404(course_id)
	submissions = QuestSubmission.query.filter_by(course_id=course_id, status=SubmissionStatus.SUBMITTED).all()
	print(submissions)
	return render_template('course_quest_submissions.html', course=course, submissions=submissions)

@courses.route('/course/<int:course_id>/quests/maps')
@login_required
@roles_required([__TEACHER_ROLE])
def course_quests_maps(course_id):
	course=Course.query.get_or_404(course_id)
	return render_template('course_quests_maps.html', course=course)
