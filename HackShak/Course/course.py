from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from werkzeug.utils import validate_arguments
from HackShak import __ADMIN_ROLE, __TEACHER_ROLE
from flask_login import current_user, login_required
from HackShak import db
from HackShak.Auth.utils import roles_required
from HackShak.models import Course, Teacher, QuestSubmission, SubmissionStatus, QuestMap, Student
from HackShak.Course.forms import CourseForm
from random import choice
from string import ascii_letters, digits

courses = Blueprint('courses', __name__)

@courses.route('/course/create/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def course_create():
	form = CourseForm()
	teacher = Teacher.query.get(current_user.id)
	if form.validate_on_submit():
		course = Course(
			code = form.course_code.data,
			title = form.title.data, 
			description=form.description.data, 
			block=form.block.data, 
			term=form.term.data, 
			grade=form.grade.data,
			bc_curriculum = form.bc_curriculum.data
		)
		db.session.add(course)
		course.teachers.append(teacher)
		db.session.commit()

		flash(f'Course [{course.title}] has been created', 'success')
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
		course.title = form.title.data
		course.grade = form.grade.data
		course.term = form.term.data
		course.block = form.block.data
		course.bc_curriculum = form.bc_curriculum.data
		db.session.commit()
		flash(f'Course [{course.title}] has been update', 'success')
		return redirect(url_for('teachers.teacher_courses_current'))
	elif request.method == 'GET':
		form.course_code.data = course.code
		form.title.data = course.title
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

@courses.route('/course/<int:course_id>/activities')
@login_required
@roles_required([__TEACHER_ROLE])
def course_activities(course_id):
	course=Course.query.get_or_404(course_id)
	return render_template('course_activities.html', course=course)


@courses.route('/course/<int:course_id>/activity/add', methods=['POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def course_activity_add(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        selected_activity = request.form
        print(selected_activity)
        for activity_id in selected_activity:
            activity = QuestMap.query.get(activity_id)
            if activity:
                if activity not in course.activities:
                    course.activities.append(activity)
                    flash(f"Activity: {activity.title} has been added to course: {course.title}", 'success')
                else:
                    flash(f"Activity: {activity.title} was already assigned to course: {course.title}", 'warning')
    db.session.commit()
    return redirect(url_for('courses.course_activities', course_id=course.id))


@courses.route('/course/<int:course_id>/activity/<int:activity_id>/remove')
@login_required
@roles_required([__TEACHER_ROLE])
def course_activity_remove(course_id, activity_id):
    course = Course.query.get_or_404(course_id)
    activity = QuestMap.query.get_or_404(activity_id)
    if activity in course.activities:
        course.activities.remove(activity)
        db.session.commit()
        flash(f"Activity have been removed from course: {course.title}", 'success')
    else:
        flash(f"Activity '{activity.title}' wasn't part of course and couldn't be removed", 'warning')
    return redirect(url_for('courses.course_activities', course_id=course.id))

@courses.route('/course/<int:course_id>/activity/setprimary', methods=['POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def course_set_primary_activity(course_id):
    course = Course.query.get_or_404(course_id)
    activity_id = request.form['set_primary']
    print(activity_id)
    activity = QuestMap.query.get_or_404(activity_id)
    course.primary_activity = activity
    db.session.commit()
    flash(f"Activity '{activity.title}' has been set at the primary activity for course", 'success')
    return redirect(url_for('courses.course_activities', course_id=course.id))

@courses.route('/course/<int:course_id>/generate/invite')
@login_required
@roles_required([__TEACHER_ROLE])
def course_generate_invite(course_id):
	course = Course.query.get_or_404(course_id)
	
	valid_invite = False

	while not valid_invite:
		invite = ''.join(choice(ascii_letters + digits) for _ in range(8))
		if not Course.query.filter_by(invite=invite).first():
			valid_invite = True

	course.invite = invite
	db.session.commit()

	return redirect(url_for('courses.course_details', course_id=course.id))

@courses.route('/course/<int:course_id>/student/<int:student_id>/activities')
@login_required
@roles_required([__TEACHER_ROLE])
def course_student_activities(course_id, student_id):
	student = Student.query.get_or_404(student_id)
	avatar_file = url_for('static', filename='profile_pics/' + student.avatar_file)
	course_activities = QuestSubmission.query.filter_by(student_id=student_id, course_id=course_id).all()
	return render_template('course_student_activities.html', student=student, course_activities=course_activities, avatar_file=avatar_file)