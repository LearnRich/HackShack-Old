from flask import current_app, abort
from PIL import Image
import os
import secrets
from functools import wraps
from flask_login import current_user
from HackShak import login_manager
from HackShak.models import User


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


