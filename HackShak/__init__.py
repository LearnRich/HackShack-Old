from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from HackShak.config import HackShakConfig
from HackShak.Main.utils import datetimeformat, datetimepassed


db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

__ADMIN_ROLE = 'admin'
__TEACHER_ROLE = 'teacher'
__STUDENT_ROLE = 'student'

def create_app(config_class=HackShakConfig):
	app = Flask(__name__)
	app.config.from_object(HackShakConfig)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	from HackShak.Users.routes import users
	from HackShak.Announcements.routes import announcements
	from HackShak.Main.routes import main
	from HackShak.Quests.routes import quests
	from HackShak.errors.handlers import errors

	app.register_blueprint(users)
	app.register_blueprint(announcements)
	app.register_blueprint(main)
	app.register_blueprint(quests)
	app.register_blueprint(errors)

	app.jinja_env.filters['datetimeformat'] = datetimeformat
	app.jinja_env.filters['datetimepassed'] = datetimepassed

	return app

