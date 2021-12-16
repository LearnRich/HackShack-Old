from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from HackShak.config import HackShakConfig
from HackShak.Main.utils import datetimeformat, datetimepassed, get_class
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

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
	ma.init_app(app)

	from HackShak.Users.routes import users
	from HackShak.Students.routes import students
	from HackShak.Teachers.routes import teachers
	from HackShak.Announcements.routes import announcements
	from HackShak.Main.routes import main
	from HackShak.Activity.routes import activities
	from HackShak.Quests.routes import quests
	from HackShak.Campaign.routes import campaigns
	from HackShak.QuestMaps.routes import questmaps
	from HackShak.Course.routes import courses
	from HackShak.errors.handlers import errors

	app.register_blueprint(main)
	app.register_blueprint(errors)

	app.register_blueprint(users)
	app.register_blueprint(students)
	app.register_blueprint(teachers)

	app.register_blueprint(announcements)

	app.register_blueprint(activities)
	app.register_blueprint(quests)
	app.register_blueprint(campaigns)
	app.register_blueprint(questmaps)
	app.register_blueprint(courses)



	app.jinja_env.filters['datetimeformat'] = datetimeformat
	app.jinja_env.filters['datetimepassed'] = datetimepassed
	app.jinja_env.filters['get_class'] = get_class

	return app

