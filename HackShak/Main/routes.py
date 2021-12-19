from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from HackShak.models import Announcement, Rank
from flask_login import current_user, login_required
from HackShak.Users.utils import roles_required

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home/')
@login_required
def home():
	if current_user.has_role('student'):
		return redirect(url_for('students.student_quests_available'))
	page = request.args.get('page', 1, type=int)
	announcements = Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=page, per_page=2)
	for post in announcements.items:
		print(post)
	return render_template('home.html', posts=announcements)

@main.route('/about/')
@main.route('/help/')
@main.route('/faq/')
def about():
	return render_template('about.html', title='FAQ')


@main.route('/ranks/')
def ranks():
	rank_list = Rank.query.order_by(Rank.xp.asc())
	return render_template('faq/ranks.html', ranks=rank_list)
