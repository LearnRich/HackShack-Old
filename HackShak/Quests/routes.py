from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from HackShak import __ADMIN_ROLE, __TEACHER_ROLE
from flask_login import current_user, login_required
from HackShak import db
from HackShak.Users.utils import roles_required
from HackShak.Quests.forms import QuestForm, SubmissionForm
from HackShak.Quests.utils import get_allowed_tags
from HackShak.models import Quest, QuestSubmission
from bleach import clean, sanitizer

quests = Blueprint('quests', __name__)

@quests.route('/quests/map/')
@login_required
def map():
	return redirect(url_for('main.home'))

@quests.route('/quests/')
@login_required
def quest_all_list():
	page = request.args.get('page', 1, type=int)
	quests = Quest.query.paginate(page=page, per_page=20)
	return render_template('quests-all.html', quests=quests)

@quests.route('/quest/<int:quest_id>/')
@login_required
def quest(quest_id):
	#if the quest exists as a submission for a student 
	quest = Quest.query.get_or_404(quest_id)
	return render_template('quest.html', title=quest.title, quest=quest, legend='Quest')

@quests.route('/quest/submission/start/<int:quest_id>')
@login_required
def new_quest_work(quest_id):
	# check if the student has already started working on this 
	submission = QuestSubmission.query.filter_by().first()
	if submission == None:

		submission = QuestSubmission(studentid=current_user.id, course_id=current_user.get_role_obj().get_current_enrolled_course(), quest_id=quest_id)
		db.session.add(submission)
		db.commit()
	
	# if it does not exist create a new one
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
		db.session.commit()
		flash('Your announcement has been updated!', 'success')
		return redirect(url_for('quests.quest_submission', submission_id=submission.id))
	elif request.method == 'GET':
		form.submission_text.data = submission.submission_text
	return render_template('quest_submission.html', submission=submission, form=form, legend='Quest Submission')


@quests.route('/quest/create', methods=['GET','POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def create_new_quest():
	form = QuestForm()
	if form.validate_on_submit():
		# title, description, xp, campaign, repeatable, expiry, details, submission_instructions, quest_author
		quest = Quest(title=form.title.data, \
			description=form.description.data, \
			xp=form.xp.data, \
			#campaign=form.campaign.data, \
			repeatable=form.repeatable.data, \
			expiry=form.expiry.data, \
			details=form.details.data, \
			submission_instructions=form.submission_instructions.data, \
			quest_author=current_user, \
		)
		db.session.add(quest)
		db.session.commit()
		flash('You Quest has been created and shared', 'success')
		return redirect(url_for('quests.quest', quest_id=quest.id))
	return render_template('create_quest.html', form=form, title='New Quest', legend='New Quest')
	


@quests.route('/quest/<int:quest_id>/update/', methods=['GET','POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def update_quest(quest_id):
	quest = Quest.query.get_or_404(quest_id)
	form = QuestForm()
	if form.validate_on_submit():
		quest.title = form.title.data
		quest.description = form.description.data
		quest.xp = form.xp.data
		#quest.campaign = form.campaign.data
		quest.repeatable = form.repeatable.data
		quest.expirt = form.expiry.data
		quest.details = form.details.data
		quest.submission_instructions = form.submission_instructions.data 
		db.session.commit()
		flash('Your quest has been updated!', 'success')
		print("Quest Update:", quest)
		return redirect(url_for('quests.quest', quest_id=quest.id))
	elif request.method == 'GET':
		form.title.data = quest.title
		form.description.data = quest.description
		form.xp.data = quest.xp
		#form.campaign.data = quest.campaign
		form.repeatable.data = quest.repeatable
		form.expiry.data = quest.expiry
		form.details.data = quest.details
		form.submission_instructions.data = quest.submission_instructions
	else:
		print("The Quest form is not valid")
	return render_template('create_quest.html', title='Update Quest', quest=quest, form=form, legend='Update Quest')

@quests.route('/quest/<int:quest_id>/delete/', methods=['POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def delete_quest(quest_id):
	quest = Quest.query.get_or_404(quest_id)
	db.session.delete(quest)
	db.session.commit()
	flash("Your quest has been deleted.")
	return redirect(url_for('main.home'))