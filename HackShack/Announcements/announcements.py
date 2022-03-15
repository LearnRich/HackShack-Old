from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
from flask_login import current_user, login_required
from .. import db, __TEACHER_ROLE, __ADMIN_ROLE
from ..models import Announcement, Teacher
from ..Announcements.forms import AnnouncementForm
from ..Auth.utils import roles_required


announcements_bp = Blueprint(
	'announcements_bp', 
	__name__,
	url_prefix='/announcement/',
	template_folder='templates'
)

@announcements_bp.route('/all/')
def announcements_all():
	page = request.args.get('page', 1, type=int)
	announcement_posts = Announcement.query.paginate(page=page, per_page=10)
	return render_template('announcements.html', announcements=announcement_posts)

@announcements_bp.route('/create/', methods=['GET', 'POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def announcement_create():
	form = AnnouncementForm()
	if form.validate_on_submit():
		teacher = Teacher.query.get_or_404(current_user.id)
		announcement = Announcement(title=form.title.data, content=form.content.data, announcement_author=teacher)
		db.session.add(announcement)
		db.session.commit()
		flash('You Announcement has been created and shared', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_announcement.html', form=form, title='New Announcement', legend='New Announcement')

@announcements_bp.route('/<int:announcement_id>/')
def announcement(announcement_id):
	announcement = Announcement.query.get_or_404(announcement_id)
	return render_template('announcement.html', title=announcement.title, announcement=announcement)

@announcements_bp.route('/<int:announcement_id>/update/', methods=['GET','POST'])
@login_required
def announcement_update(announcement_id):
	announcement = Announcement.query.get_or_404(announcement_id)
	if announcement.announcement_author != current_user:
		abort(403)
	form = AnnouncementForm()
	if form.validate_on_submit():
		announcement.title = form.title.data
		announcement.content = form.content.data
		db.session.commit()
		flash('Your announcement has been updated!', 'success')
		return redirect(url_for('announcements.announcement', announcement_id=announcement.id))
	elif request.method == 'GET':
		form.title.data = announcement.title
		form.content.data = announcement.content

	return render_template('create_announcement.html', title='Update Announcement', post=announcement, form=form, legend='Update Announcement')

@announcements_bp.route('/<int:announcement_id>/delete/', methods=['POST'])
@login_required
def announcement_delete(announcement_id):
	announcement = Announcement.query.get_or_404(announcement_id)
	if announcement.announcement_author != current_user:
		abort(403)
	db.session.delete(announcement)
	db.session.commit()
	flash("Your announcement has been deleted.")
	return redirect(url_for('main.home'))

