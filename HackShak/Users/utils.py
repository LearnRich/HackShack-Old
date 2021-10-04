from flask import current_app, abort
from PIL import Image
import os
import secrets
from functools import wraps
from flask_login import current_user
from HackShak import login_manager
from HackShak.Users.models import User


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

def roles_required(roles: list, require_all=False):
    def _roles_required(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if len(roles) == 0:
                raise ValueError('Empty list used when requiring a role.')
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if require_all and not all(current_user.has_role(role) for role in roles):
                abort(403)
            elif not require_all and not any(current_user.has_role(role) for role in roles):
                abort(403)
            return f(*args, **kwargs)
        return decorated_view
    return _roles_required


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

def splitme(s, c):
    if (s[0] == c):
        return s[1:]
    else: 
        return(s)

