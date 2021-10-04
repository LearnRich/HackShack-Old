from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
from flask_login import current_user, login_required
from HackShak import db, __TEACHER_ROLE, __ADMIN_ROLE
from HackShak.Announcements.models import Announcement
from HackShak.Announcements.forms import AnnouncementForm
from HackShak.Users.utils import roles_required


announcements = Blueprint('announcements', __name__)

@announcements.route('/announcements')
def get_all_announcements():
	page = request.args.get('page', 1, type=int)
	announcement_posts = Announcement.query.paginate(page=page, per_page=10)
	return render_template('announcements.html', posts=announcement_posts)

@announcements.route('/announcement/new', methods=['GET', 'POST'])
@login_required
@roles_required([__ADMIN_ROLE, __TEACHER_ROLE])
def new_announcement():
	form = AnnouncementForm()
	if form.validate_on_submit():
		announcement = Announcement(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(announcement)
		db.session.commit()
		flash('You Announcement has been created and shared', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_announcement.html', form=form, title='New Announcement', legend='New Announcement')

@announcements.route('/announcement/<int:announcement_id>')
def announcement(announcement_id):
	announcement = Announcement.query.get_or_404(announcement_id)
	return render_template('announcement.html', title=announcement.title, post=announcement)

@announcements.route('/announcement/<int:announcement_id>/update', methods=['GET','POST'])
@login_required
def update_announcement(announcement_id):
	announcement = Announcement.query.get_or_404(announcement_id)
	if announcement.author != current_user:
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

@announcements.route('/announcement/<int:announcement_id>/delete', methods=['POST'])
@login_required
def delete_announcement(announcement_id):
	announcement = Announcement.query.get_or_404(announcement_id)
	if announcement.author != current_user:
		abort(403)
	db.session.delete(announcement)
	db.session.commit()
	flash("Your announcement has been deleted.")
	return redirect(url_for('main.home'))
