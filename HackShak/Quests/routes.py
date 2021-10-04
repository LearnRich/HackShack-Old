from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from HackShak import __ADMIN_ROLE, __TEACHER_ROLE
from flask_login import current_user, login_required
from HackShak import db
from HackShak.Users.utils import roles_required
from HackShak.Quests.forms import QuestForm
from HackShak.Quests.models import Quest

quests = Blueprint('quests', __name__)

quests.route('/quests/create')
@login_required()
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def create_new_quest():
	form = QuestForm()
	if form.validate_on_submit():
		quest = Quest(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(quest)
		db.session.commit()
		flash('You Quest has been created and shared', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_quest.html', form=form, title='New Quest', legend='New Quest')

@quests.route('/quests/<int:quest_id>')
def announcement(quest_id):
	quest = Quest.query.get_or_404(quest_id)
	return render_template('announcement.html', title=quest.title, quest=quest)

@quests.route('/quests/<int:quest_id>/update', methods=['GET','POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def update_quest(quest_id):
	quest = Quest.query.get_or_404(quest_id)
	form = QuestForm()
	if form.validate_on_submit():
		quest.title = form.title.data
		quest.content = form.content.data
		db.session.commit()
		flash('Your quest has been updated!', 'success')
		return redirect(url_for('quests.quest', quest_id=quest.id))
	elif request.method == 'GET':
		form.title.data = quest.title
		form.content.data = quest.content

	return render_template('create_quest.html', title='Update Quest', quest=quest, form=form, legend='Update Quest')

@quests.route('/quests/<int:quest_id>/delete', methods=['POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def delete_quest(quest_id):
	quest = Quest.query.get_or_404(quest_id)
	db.session.delete(quest)
	db.session.commit()
	flash("Your quest has been deleted.")
	return redirect(url_for('main.home'))
