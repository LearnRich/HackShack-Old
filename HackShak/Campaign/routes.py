from flask import Blueprint, render_template, request, url_for, redirect, flash, abort, jsonify
from HackShak import __ADMIN_ROLE, __TEACHER_ROLE, __STUDENT_ROLE
from flask_login import current_user, login_required
from HackShak import db
from HackShak.Users.utils import roles_required
from HackShak.models import Campaign, Quest
from HackShak.schemas import CampaignSchema
from HackShak.Campaign.forms import CampaignForm

campaigns = Blueprint('campaigns', __name__)

@campaigns.route('/campaigns/all/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def campaigns_all():
    campaigns_list = Campaign.query.all()
    return render_template('campaigns_all.html',campaigns=campaigns_list, title='New Campaign', legend='New Campaign')


@campaigns.route('/campaign/create/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def campaign_create():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            name = form.name.data,
            description = form.description.data
        )
        db.session.add(campaign)
        db.session.commit()
        flash(f"Your campaign: {campaign.name}, has been created.", 'success')
        return redirect(url_for('campaigns.campaigns_all'))
    return render_template('campaign_create.html',form=form, title='New Campaign', legend='New Campaign')

@campaigns.route('/campaign/<int:campaign_id>/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('campaign_manager.html', campaign=campaign, title='Review Campaign', legend='Review Campaign')

@campaigns.route('/campaign/<int:campaign_id>/update/', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def campaign_update(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = CampaignForm()
    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        db.session.commit()
        flash(f"Your campaign {campaign.name} has been update.", 'success')
        return redirect(url_for('campaigns.campaign', campaign_id=campaign.id))
    elif request.method == 'GET':
        form.name.data = campaign.name
        form.description.data = campaign.description
    return render_template('campaign_create.html',form=form, title='Update Campaign', legend='Update Campaign')


@campaigns.route('/campaign/<int:campaign_id>/quests', methods=['GET', 'POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def campaign_quests(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('campaign_quest_manager.html', campaign=campaign, legend='Manage Campaign Quests')

@campaigns.route('/campaign/<int:campaign_id>/quest/add', methods=['POST'])
@login_required
@roles_required([__TEACHER_ROLE])
def campaign_quest_add(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    add_count = 0
    if request.method == 'POST':
        selected_quests = request.form
        print(selected_quests)
        for quest_id in selected_quests:
            quest = Quest.query.get(quest_id)
            if quest:
                if quest not in campaign.quests:
                    campaign.quests.append(quest)
                    add_count += 1
                    flash(f"Quest: {quest.title} has been added to campaign: {campaign.name}", 'success')
                else:
                    flash(f"Quest: {quest.title} was already assigned to campaign: {campaign.name}", 'warning')
    db.session.commit()
    return redirect(url_for('campaigns.campaign_quests', campaign_id=campaign.id))


@campaigns.route('/campaign/<int:campaign_id>/quest/<int:quest_id>/remove')
@login_required
@roles_required([__TEACHER_ROLE])
def campaign_quest_remove(campaign_id, quest_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    quest = Quest.query.get_or_404(quest_id)
    campaign.quests.remove(quest)
    db.session.commit()
    flash(f"Quest(s) have been added to campaign: {campaign.name}", 'success')
    return redirect(url_for('campaigns.campaign_quests', campaign_id=campaign.id))


# |---------------------------------------|
# | Routes related to campaign AJAX Calls |
# |---------------------------------------|

@campaigns.route('/campaigns/search/', defaults={'limit':None}, methods=['POST'])
@campaigns.route('/campaigns/search/<int:limit>', methods=['POST'])
@login_required
def campaigns_search(limit):
    json_campaign_list = []
    if request.method == 'POST':
        print(request.form)
        campaign_name_qry = request.form['query']

        if limit:
            campaigns = Campaign.query.filter(Campaign.name.contains(campaign_name_qry)).limit(limit).all()
        else:
            campaigns = Campaign.query.filter(Campaign.name.contains(campaign_name_qry)).all()

        campaign_schema = CampaignSchema()
        for campaign in campaigns:
            output = campaign_schema.dump(campaign)
            json_campaign_list.append(output)
            
    return jsonify(json_campaign_list)
