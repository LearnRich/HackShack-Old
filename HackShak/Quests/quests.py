from flask import Blueprint, render_template, request, url_for, redirect, flash, abort, jsonify, current_app, send_from_directory
from HackShak import db, __ADMIN_ROLE, __TEACHER_ROLE, __STUDENT_ROLE
from flask_login import current_user, login_required
from HackShak.Auth.utils import roles_required
from HackShak.Quests.forms import QuestForm, SubmissionForm, SubmissionReviewForm
from HackShak.Quests.utils import get_allowed_tags
from HackShak.models import Quest, QuestSubmission, SubmissionStatus, Student, SubmissionLog, SubmissionLogCategory, Campaign, QuestSubmissionFile
from HackShak.schemas import QuestSchema
from bleach import clean, sanitizer
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import os
import json



quests = Blueprint('quests', __name__)

# |------------------------------------|
# | Routes related to quest list pages |
# |------------------------------------|

@quests.route('/quests/map/')
@login_required
def quests_maps():
	return redirect(url_for('main.home'))

@quests.route('/quests/all')
@login_required
def quests_all():
	page = request.args.get('page', 1, type=int)
	quests = Quest.query.paginate(page=page, per_page=20)
	return render_template('quests-all.html', quests=quests)

@quests.route('/quests/available/')
@login_required
@roles_required([__STUDENT_ROLE])
def quest_available():
	student = Student.query.get_or_404(current_user.id)
	# ARGG THIS ONE IS HARD.
	# Get Submitted submission
	# Get Completed Submission
	# check course maps for where quest submissions have been met
	# Then get next quest
	return redirect(url_for('quests.quests_all'))

@quests.route('/quests/inprogress/')
@login_required
@roles_required([__STUDENT_ROLE])
def quest_inprogress():
	student = Student.query.get_or_404(current_user.id)
	in_progress = student.submissions.filter_by(status=SubmissionStatus.IN_PROGRESS)
	# also need to double check for current course/term
	return redirect(url_for('quests.quests_all'))

@quests.route('/quests/completed/')
@login_required
@roles_required([__STUDENT_ROLE])
def quest_completed():
	student = Student.query.get_or_404(current_user.id)
	# also need to filter for current course/term
	completed = student.submissions.filter(QuestSubmission.status.in_([SubmissionStatus.COMPLETED, SubmissionStatus.SUBMITTED]))
	return redirect(url_for('quests.quests_all'))

@quests.route('/quests/pastcourses/')
@login_required
@roles_required([__STUDENT_ROLE])
def quest_past():
	student = Student.query.get_or_404(current_user.id)
	# Filter by course not in current term
	completed = student.submissions.filter_by(status=SubmissionStatus.COMPLETED)
	return redirect(url_for('quests.quests_all'))

# |------------------------------------------|
# | Routes related to individual quest pages |
# |------------------------------------------|

@quests.route('/quest/<int:quest_id>/')
@login_required
def quest(quest_id): 
	quest = Quest.query.get_or_404(quest_id)
	return render_template('quest.html', title=quest.title, quest=quest, legend='Quest')


@quests.route('/quest/create', methods=['GET','POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def quest_create():
	form = QuestForm()
	if form.validate_on_submit():
		campaign = Campaign.query.get(form.campaign.data)
		# title, description, xp, campaign, repeatable, expiry, details, submission_instructions, quest_author

		quest = Quest()
		quest.title = form.title.data
		quest.description = form.description.data
		quest.details = form.details.data
		quest.submission_instructions = form.submission_instructions.data
		quest.xp = form.xp.data
		quest.repeatable = form.repeatable.data
		quest.author_id = current_user.id
		quest.campaign = campaign

		db.session.add(quest)
		db.session.commit()

		flash('You Quest has been created and shared', 'success')
		return redirect(url_for('quests.quest', quest_id=quest.id))
	return render_template('quest_create.html', form=form, title='New Quest', legend='New Quest')
	


@quests.route('/quest/<int:quest_id>/update/', methods=['GET','POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def quest_update(quest_id):
	quest = Quest.query.get_or_404(quest_id)
	form = QuestForm()
	if form.validate_on_submit():
		quest.title = form.title.data
		quest.description = form.description.data
		quest.xp = form.xp.data
		quest.repeatable = form.repeatable.data
		quest.expirt = form.expiry.data
		quest.details = form.details.data
		quest.submission_instructions = form.submission_instructions.data 
		print(form.requirements.data.replace('\'', '"'))
		quest.update_requirements(json.loads(form.requirements.data.replace('\'', '"')))

		if form.campaign.data:
			quest_campaign = Campaign.query.get(form.campaign.data)
			if quest_campaign:
				quest.campaign = quest_campaign

		db.session.commit()
		flash('Your quest has been updated!', 'success')
		return redirect(url_for('quests.quest', quest_id=quest.id))

	elif request.method == 'GET':
		form.title.data = quest.title
		form.description.data = quest.description
		form.xp.data = quest.xp
		form.requirements.data = ([{"id":x.id} for x in quest.requirements])
		if quest.campaign:
			form.campaign.choices = [(quest.campaign.id, quest.campaign.title)]
			form.campaign.default = quest.campaign.id
		form.repeatable.data = quest.repeatable
		form.expiry.data = quest.expiry
		form.details.data = quest.details
		form.submission_instructions.data = quest.submission_instructions

	else:
		print("The Quest form is not valid")

	return render_template('quest_create.html', title='Update Quest', quest=quest, form=form, legend='Update Quest')

@quests.route('/quest/<int:quest_id>/delete/', methods=['POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def quest_delete(quest_id):
	quest = Quest.query.get_or_404(quest_id)
	try:
		db.session.delete(quest)
		db.session.commit()
		flash('Your quest has been deleted.', 'message')
	except IntegrityError  as e:
		flash('You are attempting to do something to the database that you are not allowed', 'warning')	
		next_page = request.args.get('next')
		return redirect(next_page) if next_page else redirect(url_for('quests.quests_all'))
	return redirect(url_for('quests.quests_all'))

@quests.route('/quest/<int:quest_id>/requirement/add', methods=['POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def quest_requrement_add(quest_id):
	quest = Quest.query.get_or_404(quest_id)
	return redirect(url_for('quests.quest', quest_id=quest.id))

# |------------------------------------------|
# | Routes related to quest submission pages |
# |------------------------------------------|
@quests.route('/quest/submission/start/<int:quest_id>')
@login_required
def quest_submission_start(quest_id):
		#check for existing submission for this quest by this student ( could be in any course )
	quest = Quest.query.get_or_404(quest_id)
	student = Student.query.get_or_404(current_user.id)

	submission = QuestSubmission.query.filter_by(student_id=student.id, quest_id=quest.id).first()

	if submission is None:
		submission = QuestSubmission(
			quest = quest,
			student = student,
			course = student.get_current_enrolled_course(),
			status = SubmissionStatus.IN_PROGRESS
		)
		db.session.add(submission)
	else:
		# Check to see if course is in current term before allowing to 
		submission.status = SubmissionStatus.IN_PROGRESS
	db.session.commit()

	return redirect(url_for('quests.quest_submission', submission_id=submission.id))

@quests.route('/quest/submission/<int:submission_id>/', methods=['GET','POST'])
@login_required
def quest_submission(submission_id):
	# get existing student work 
	submission = QuestSubmission.query.get_or_404(submission_id)
	if submission.student_id != current_user.id:
		abort(403)
	form = SubmissionForm()
	if form.validate_on_submit():
		submission.submission_text = form.submission_text.data
		print(form.files.data)
		for file in form.files.data:
			if file:
				s_filename = secure_filename(file.filename)
				dir_path = os.path.join(current_app.root_path, 'static\submissions', current_user.username, str(submission.id))
				if not os.path.exists(dir_path):
					os.makedirs(dir_path)
				file_path = os.path.join(dir_path, s_filename)
				file.save(file_path)
				submitted_file = QuestSubmissionFile(filename=s_filename, submission_id=submission.id)
				submission.files.append(submitted_file)
		if form.save.data:
			submission.status = SubmissionStatus.IN_PROGRESS
			db.session.commit()
			flash('Your submission has been saved!', 'success')
			return redirect(url_for('quests.quest_submission', submission_id=submission.id))
		elif form.submit.data:
			submission.status = SubmissionStatus.SUBMITTED
			history = SubmissionLog(submission=submission, content=submission.submission_text, user_id=current_user.id)
			submission.submission_text = ""
			db.session.commit()
			flash('Your submission has been submitted for completion!', 'success')
			return redirect(url_for('students.student_quests_available'))
		flash('Your submission has been saved from an unknown form!', 'warning')
		return redirect(url_for('quests.quest_submission', submission_id=submission.id))
	elif request.method == 'GET':
		form.submission_text.data = submission.submission_text
	return render_template('quest_submission.html', submission=submission, form=form, legend='Quest Submission')

@quests.route("/quest/submission/<int:submission_id>/attachment/<int:file_id>")
@login_required
def submission_attachment(submission_id, file_id):
	submission = QuestSubmission.query.get_or_404(submission_id)
	file = QuestSubmissionFile.query.get_or_404(file_id)
	if current_user.has_role(__STUDENT_ROLE):
		if submission.student_id != current_user.id :
			abort(403)
	
	dir_path = os.path.join(current_app.root_path, 'static\submissions', current_user.username, str(submission.id))
	try:
		return send_from_directory(dir_path, file.filename, as_attachment=True, attachment_filename=file.filename)
	except:
		abort(404)


@quests.route('/quest/submission/<int:submission_id>/attachment/<int:file_id>/remove')
@login_required
@roles_required([__STUDENT_ROLE])
def submission_attachment_remove(submission_id, file_id):
	# get existing student work 
	submission = QuestSubmission.query.get_or_404(submission_id)
	file = QuestSubmissionFile.query.get_or_404(file_id)
	if submission.student_id != current_user.id:
		abort(403)
	
	file_path = os.path.join(current_app.root_path, 'static\submissions', current_user.username, str(submission.id), file.filename)
	if os.path.exists(file_path):
		flash(f"{file.filename} was removed from submission", 'success')
		os.remove(file_path)
		submission.files.remove(file)
		db.session.delete(file)
		db.session.commit()
	else:
		flash(f"Unable to remove, could not find file {file.filename}", 'warning')
	return redirect(url_for('quests.quest_submission', submission_id=submission_id))

@quests.route('/quest/submission/<int:submission_id>/drop')
@login_required
@roles_required([__STUDENT_ROLE])
def quest_submission_drop(submission_id):
	# get existing student work 
	submission = QuestSubmission.query.get_or_404(submission_id)
	if submission.student_id != current_user.id:
		abort(403)
	submission.status = SubmissionStatus.DROPPED
	db.session.commit()
	return redirect(url_for('students.student_quests_available'))

@quests.route('/quest/submission/<int:submission_id>/review', methods=['GET','POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def quest_submission_review(submission_id):
	# get attached file(s)
	submission = QuestSubmission.query.get_or_404(submission_id)
	form = SubmissionReviewForm()
	if form.validate_on_submit():
		category = SubmissionLogCategory.FEEDBACK
		if form.feedback_category.data == 'success':
			category = SubmissionLogCategory.SUCCESS
		elif form.feedback_category.data == 'warning':
			category = SubmissionLogCategory.WARNING
		elif form.feedback_category.data == 'danger':
			category = SubmissionLogCategory.DANGER
		feedback = SubmissionLog(
			submission_id=submission.id,
			user_id=current_user.id,
			content=form.feedback_text.data,
			category=category
		)
		submission.awarded_xp = form.awarded_xp.data
		submission.submission_logs.append(feedback)
		submission.status = SubmissionStatus.COMPLETED
		db.session.commit()
		flash('Submission has been returned to student.', 'success')
		return redirect(url_for('quests.quest_submission_review', submission_id=submission.id))
	return render_template('quest_submission_review.html', submission=submission, form=form, legend='Review Quest Submission')

@quests.route('/quest/submission/<int:submission_id>/feedback/remove', methods=['GET','POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def feedback_remove(submission_id):
	feedback = SubmissionLog.query.get_or_404( request.form['hidden_input'])
	db.session.delete(feedback)
	db.session.commit()
	flash("Your feedback has been deleted.")
	return redirect(url_for('quests.quest_submission_review', submission_id=submission_id))

# |------------------------------------|
# | Routes related to quest AJAX Calls |
# |------------------------------------|

@quests.route('/quests/search/', defaults={'limit':None}, methods=['POST'])
@quests.route('/quests/search/<int:limit>', methods=['POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def quests_search(limit):
	json_quest_list = []
	if request.method == 'POST':
		quest_name_qry = request.form['query']
		
		if limit:
			if quest_name_qry == "*":
				quests = Quest.query.limit(limit).all()
			else:
				quests = Quest.query.filter(Quest.title.contains(quest_name_qry)).limit(limit).all()
		else:
			if quest_name_qry == "*":
				quests = Quest.query.all()
			else:
				quests = Quest.query.filter(Quest.title.contains(quest_name_qry)).all()

		quest_schema = QuestSchema()
		for quest in quests:
			output = quest_schema.dump(quest)
			json_quest_list.append(output)

	return jsonify(json_quest_list)

@quests.route('/quests/search/campaign/', defaults={'limit':None}, methods=['POST'])
@quests.route('/quests/search/campaign/<int:limit>', methods=['POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def quests_search_by_campaign(limit):
	json_quest_list = []
	if request.method == 'POST':
		search_qry = request.form['query']
		campaigns = Campaign.query.filter(Campaign.title.contains(search_qry))
		quests = []
		for campaign in campaigns:
			campaign_quests = campaign.quests
			print(campaign_quests)
			quests += campaign.quests
		print(quests)
		if limit:
			quests = quests[:limit]

		quest_schema = QuestSchema()
		for quest in quests:
			output = quest_schema.dump(quest)
			json_quest_list.append(output)

	return jsonify(json_quest_list)
