from flask import Blueprint, render_template, request, url_for, redirect, flash, abort, jsonify
from HackShak import __ADMIN_ROLE, __TEACHER_ROLE, __STUDENT_ROLE
from flask_login import current_user, login_required
from HackShak import db
from HackShak.Users.utils import roles_required
from HackShak.models import Campaign, Quest, QuestMap
from HackShak.schemas import QuestMapSchema
from HackShak.QuestMaps.forms import QuestMapForm

questmaps = Blueprint('questmaps', __name__)

@questmaps.route('/questmaps/all/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def questmaps_all():
    questmaps = QuestMap.query.all()
    print(questmaps)
    return render_template('questmaps_all.html',questmaps=questmaps, title='View All Quest Maps', legend='View All Quest Maps')


@questmaps.route('/questmap/create/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def questmap_create():
    form = QuestMapForm()
    if form.validate_on_submit():
        questmap = QuestMap(
            title = form.title.data,
            description = form.description.data
        )
        db.session.add(questmap)
        db.session.commit()
        flash(f"Your quest map: {questmap.title}, has been created.", 'success')
        return redirect(url_for('questmaps.questmaps_all'))
    return render_template('questmap_create.html',form=form, title='New Quest Map', legend='New Quest Map')

@questmaps.route('/questmap/<int:questmap_id>/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def questmap(questmap_id):
    questmap = QuestMap.query.get_or_404(questmap_id)
    return render_template('questmap_manager.html', questmap=questmap, title='Manage Quest Map', legend='Manage Quest Map')

@questmaps.route('/questmap/<int:questmap_id>/update/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def questmap_update(questmap_id):
    questmap = QuestMap.query.get_or_404(questmap_id)
    form = QuestMapForm()
    if form.validate_on_submit():
        questmap.title = form.title.data
        questmap.description = form.description.data
        db.session.commit()
        flash(f"Your quest map {questmap.title} has been update.", 'success')
        return redirect(url_for('questmaps.questmap', questmap_id=questmap.id))
    elif request.method == 'GET':
        form.title.data = questmap.title
        form.description.data = questmap.description
    return render_template('questmap_create.html',form=form, title='Update Quest Map', legend='Update Quest Map')


@questmaps.route('/questmap/<int:questmap_id>/quests', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def questmap_quests(questmap_id):
    questmap = QuestMap.query.get_or_404(questmap_id)
    return render_template('questmap_quest_manager.html', questmap=questmap, legend='Manage Assigned Quests to Map')

@questmaps.route('/questmap/<int:questmap_id>/quest/add', methods=['POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def questmap_quest_add(questmap_id):
    questmap = QuestMap.query.get_or_404(questmap_id)
    add_count = 0
    if request.method == 'POST':
        selected_quests = request.form
        print(selected_quests)
        for quest_id in selected_quests:
            quest = Quest.query.get(quest_id)
            if quest:
                if quest not in questmap.quests:
                    questmap.quests.append(quest)
                    add_count += 1
                    flash(f"Quest: {quest.title} has been added to quest map: {questmap.title}", 'success')
                else:
                    flash(f"Quest: {quest.title} was already assigned to campaign: {questmap.title}", 'warning')
    db.session.commit()
    return redirect(url_for('questmaps.questmap_quests', questmap_id=questmap.id))


@questmaps.route('/questmap/<int:questmap_id>/quest/<int:quest_id>/remove', methods=['POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def questmap_quest_remove(questmap_id, quest_id):
    questmap = QuestMap.query.get_or_404(questmap_id)
    quest = Quest.query.get_or_404(quest_id)
    if quest in questmap.quests:
        questmap.quests.remove(quest)
        db.session.commit()
        flash(f"Quest(s) have been added to questmap: {questmap.title}", 'success')
    else:
        flash(f"Quest '{quest.title}' wasn't part of questmap and couldn't be removed", 'warning')
    return redirect(url_for('questmaps.questmap_quests', questmap_id=questmap.id))

@questmaps.route('/questmap/<int:questmap_id>/quest/setprimary', methods=['POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def questmap_set_primary_quest(questmap_id):
    questmap = QuestMap.query.get_or_404(questmap_id)
    quest_id = request.form['set_primary']
    print(quest_id)
    quest = Quest.query.get_or_404(quest_id)
    questmap.primary_quest = quest
    db.session.commit()
    flash(f"Quest '{quest.title}' has been set at the primary quest for map", 'success')
    return redirect(url_for('questmaps.questmap_quests', questmap_id=questmap.id))

# |---------------------------------------|
# | Routes related to campaign AJAX Calls |
# |---------------------------------------|

@questmaps.route('/questmaps/search/', defaults={'limit':None}, methods=['POST'])
@questmaps.route('/questmaps/search/<int:limit>', methods=['POST'])
@login_required
def questmaps_search(limit):
    json_questmap_list = []
    if request.method == 'POST':
        print(request.form)
        questmap_title_qry = request.form['query']

        if limit:
            questmaps = QuestMap.query.filter(QuestMap.title.contains(questmap_title_qry)).limit(limit).all()
        else:
            questmaps = QuestMap.query.filter(QuestMap.title.contains(questmap_title_qry)).all()

        questmap_schema = QuestMapSchema()
        for campaign in questmaps:
            output = questmap_schema.dump(campaign)
            json_questmap_list.append(output)
            
    return jsonify(json_questmap_list)
