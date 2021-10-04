from HackShak import db
from flask_login import UserMixin

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
	lastname = db.Column(db.String(50))
	email = db.Column(db.String(128), unique=True)
	image_file = db.Column(db.String(20), nullable=False, default='default.png')
	password = db.Column(db.String(60), nullable=False)
	active = db.Column(db.Boolean)
	confirmed_at = db.Column(db.DateTime())
	
	def get_roles(self):
		return self.role_assignments

	def has_role(self, role):
		return any(role == role_assignment.role.name and role_assignment.role.active
			for role_assignment in self.role_assignments)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"	
