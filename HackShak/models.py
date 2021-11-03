from HackShak import db
from flask_login import UserMixin
from datetime import datetime

class Role(db.Model):
	__tablename__ = 'role'
	name = db.Column(db.String(20), primary_key=True)
	active = db.Column(db.Boolean, default=True, nullable=False)

	def __init__(self, name, active=True):
		self.name = name
		self.active = active

	@staticmethod
	def create(name, active=True):
		rv = Role(name, active)
		db.session.add(rv)
		db.session.commit()
		return rv

	@staticmethod
	def get(role_name):
		role = Role.query.filter(Role.name == role_name).first()
		return role

	def __repr__(self):
		return f"{self.name}"	


class RoleAssignment(db.Model):
	__tablename__ = 'role_assignment'
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable=False)
	role_name = db.Column('role_name', db.String(20), db.ForeignKey('role.name'), nullable=False)

	role = db.relationship('Role', backref=db.backref('role_assignments', lazy='joined'), lazy='joined')
	user = db.relationship('User', backref=db.backref('role_assignments', lazy='joined'), lazy='joined')

	def __init__(self, role_name, user_id):
		self.role_name = str(role_name)
		self.user_id = user_id

	@staticmethod
	def create(role_name, user_id):
		rv = RoleAssignment(role_name, user_id)
		db.session.add(rv)
		db.session.commit()
		return rv

	@staticmethod
	def get(id):
		rv = RoleAssignment.query.filter(RoleAssignment.id == id).first()
		return rv

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False, index=True)
	firstname = db.Column(db.String(50))
	#legal_firstname
	#prefered first name
	#internal_use_only_usual_name_flag
	# alias
	lastname = db.Column(db.String(50))
	email = db.Column(db.String(128), unique=True)
	# change variable to avatar_file
	image_file = db.Column(db.String(20), nullable=False, default='default.png')
	password = db.Column(db.String(60), nullable=False)
	active = db.Column(db.Boolean)
	confirmed_at = db.Column(db.DateTime())

	# grad year
	# announcements via email
	# visible to other students

	#custom style
	
	announcements = db.relationship("Announcement", backref="announcement_author", lazy=True)
	quests = db.relationship("Quest", backref='quest_author', lazy=True)

	def get_roles(self):
		return self.role_assignments

	def has_role(self, role):
		return any(role == role_assignment.role.name and role_assignment.role.active
			for role_assignment in self.role_assignments)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"	

class Announcement(db.Model):
	__tablename__ = 'announcement'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)

	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Announcement('{self.title}', '{self.content}')"


class Quest(db.Model):
	__tablename__ = "quest"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	description = db.Column(db.Text, nullable=True)
	xp = db.Column(db.Integer, nullable=False)
	# campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=True)
	expiry = db.Column(db.String(100), nullable=True)
	repeatable = db.Column(db.String(100), nullable=True)
	# requirements -> this should be multiple foriegn keys
	details = db.Column(db.Text, nullable=False)
	submission_instructions = db.Column(db.Text, nullable=False)

	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Quest('{self.title}', '{self.description}')"


'''
class Campaign(db.Model):
	__tablename__ = 'campaign'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)

	quests =  db.relationship("Quest", backref='quest', lazy=True)

	def __repr__(self):
		return f"Campaign('{self.title}', '{self.description}')"
'''


'''
class Notification(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
'''
