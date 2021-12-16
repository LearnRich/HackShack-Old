from flask import Blueprint, render_template, request, url_for, redirect, flash, abort, jsonify
from HackShak import __ADMIN_ROLE, __TEACHER_ROLE
from flask_login import current_user, login_required
from HackShak import db
from HackShak.Users.utils import roles_required
from HackShak.models import Activity, QuestMap
from HackShak.schemas import QuestMapSchema


activities = Blueprint('activities', __name__)

@activities.route('/activity/live/search/', defaults={'limit':None}, methods=['POST'])
@activities.route('/activity/live/search/<int:limit>/', methods=['POST'])
@login_required
def activity_live_search(limit):
	json_quest_list = []
	if request.method == 'POST':
		quest_name_qry = request.form['query']
		
		if limit:
			activities = QuestMap.query.filter(QuestMap.title.contains(quest_name_qry)).limit(limit).all()
		else:
			activities = QuestMap.query.filter(QuestMap.title.contains(quest_name_qry)).all()

		quest_schema = QuestMapSchema()
		for activity in activities:
			output = quest_schema.dump(activity)
			json_quest_list.append(output)
        
	return jsonify(json_quest_list)