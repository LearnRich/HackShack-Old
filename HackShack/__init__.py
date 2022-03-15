from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_assets import Environment
from flask_marshmallow import Marshmallow
from flask_mail import Mail

from flask_migrate import Migrate

from os import environ

from .filters import datetimeformat, datetimepassed, get_class


db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()
assets = Environment()
migrate = Migrate()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
login_manager.login_message_category = 'info'

__ADMIN_ROLE = environ.get('ADMIN_ROLE_NAME')
__TEACHER_ROLE = environ.get('ADMIN_ROLE_NAME')
__STUDENT_ROLE = environ.get('ADMIN_ROLE_NAME')

def create_app():
	app = Flask(__name__)
	app.config.from_object('config.'+environ.get('FLASK_ENV').capitalize())

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	ma.init_app(app)
	migrate.init_app(app, db)

	from .errors.handlers import errors

	from .Auth.auth import auth_bp
	from .Registration.registration import reg_bp
	from .Main.main import main_bp
	from .Profile.profile import profile_bp

	#from .Students.students import students
	#from .Teachers.routes import teachers
	from .Announcements.announcements import announcements_bp
	
	#from .Activity.activity import activities
	#from .Quests.quests import quests
	#from .Campaign.campaign import campaigns
	#from .QuestMaps.questmaps import questmaps
	#from .Course.course import courses

	app.register_blueprint(errors)

	app.register_blueprint(main_bp)
	app.register_blueprint(auth_bp)
	app.register_blueprint(reg_bp)
	app.register_blueprint(profile_bp)
	#app.register_blueprint(students)
	#app.register_blueprint(teachers)

	app.register_blueprint(announcements_bp)

	#app.register_blueprint(activities)
	#app.register_blueprint(quests)
	#app.register_blueprint(campaigns)
	#app.register_blueprint(questmaps)
	#app.register_blueprint(courses)


	app.jinja_env.filters['datetimeformat'] = datetimeformat
	app.jinja_env.filters['datetimepassed'] = datetimepassed
	app.jinja_env.filters['get_class'] = get_class

	return app

