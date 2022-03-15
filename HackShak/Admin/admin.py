from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import current_user, login_required

from .. import db, __ADMIN_ROLE
from ..models import User
from ..Auth.utils import roles_required

admin_bp = Blueprint('admin_bp', __name__,
	url_prefix='/admin/',
	template_folder='templates'
)

# Features for Admin 

# remove students
# create terms 
# backup DB
# 

@admin_bp.route('/user/<string:username>/remove/')
@login_required
@roles_required([__ADMIN_ROLE])
def remove_user(username):
	user = User.query.get_or_404(username=username)
	if user.author != current_user:
		abort(403)
	db.session.delete(user)
	db.session.commit()
	flash(f"The User {user.username} has been deleted.")
	return redirect(url_for('main.home'))


