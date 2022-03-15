from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required
from HackShak import db,__STUDENT_ROLE

from HackShak.models import QuestSubmission, Student, SubmissionStatus, Quest
from HackShak.Auth.utils import roles_required, save_picture, splitme

students = Blueprint('students', __name__)

@students.route('/student/quests/available/')
@login_required
@roles_required([__STUDENT_ROLE])
def student_quests_available():
    student = Student.query.get_or_404(current_user.id)
    available=[]
    # Based on submission work our available quests. 
    enrolled_course = student.get_current_enrolled_course()
    available_quests_list = []
    available_quests_list = student.find_available(enrolled_course.get_primary_quest(), available_quests_list)
    print(available_quests_list)
    return render_template('student_quests_available.html', student=student, available=available_quests_list)

@students.route('/student/quests/inprogress/')
@login_required
@roles_required([__STUDENT_ROLE])
def student_quests_in_progress():
    student = Student.query.get_or_404(current_user.id) 
    enrolled_course = student.get_current_enrolled_course()
    submissions = QuestSubmission.query.filter_by(student_id=student.id, course_id=enrolled_course.id, status=SubmissionStatus.IN_PROGRESS).all()
    return render_template('student_quests_in_progress.html', student=student, submissions=submissions)

@students.route('/student/quests/completed/')
@login_required
@roles_required([__STUDENT_ROLE])
def student_quests_completed():
    student = Student.query.get_or_404(current_user.id)
    current_course = student.get_current_enrolled_course()
    submissions = QuestSubmission.query.filter(QuestSubmission.student_id==student.id,
										QuestSubmission.status.in_((SubmissionStatus.SUBMITTED, SubmissionStatus.COMPLETED))).all()
    return render_template('student_quests_submitted.html', student=student, submissions=submissions )

@students.route('/student/quests/past/')
@login_required
@roles_required([__STUDENT_ROLE])
def student_quests_past():
    student = Student.query.get_or_404(current_user.id)
    return render_template('student_quests_past.html', student=student)

@students.route('/student/badges/')
@login_required
@roles_required([__STUDENT_ROLE])
def badges():
    student = Student.query.get_or_404(current_user.id)
    return render_template('badges.html', student=student)
