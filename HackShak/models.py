from sqlalchemy.orm import backref
from HackShak import db, ma, __STUDENT_ROLE, __ADMIN_ROLE, __TEACHER_ROLE
from flask_login import UserMixin
from datetime import datetime
import enum

course_enrollment = db.Table('course_enrollment',
	db.Column('course_id', db.ForeignKey('course.id'), primary_key=True),
	db.Column('student_id', db.ForeignKey('student.id'), primary_key=True)
)

taught_by = db.Table('taught_by',
	db.Column('course_id', db.ForeignKey('course.id'), primary_key=True),
	db.Column('teacher_id', db.ForeignKey('teacher.id'), primary_key=True)
)

quest_requirements = db.Table("quest_requirements",
	db.Column('base_quest_id', db.Integer, db.ForeignKey('quest.id')),
	db.Column('required_quest_id', db.Integer, db.ForeignKey('quest.id'))
)

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
	email = db.Column(db.String(128), unique=True)
	password = db.Column(db.String(60), nullable=False)
	account_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	active = db.Column(db.Boolean)

	firstname = db.Column(db.String(50))
	preferred_firstname = db.Column(db.String(50))
	f_internal_use_only_preferred_name = db.Column(db.Boolean, default=False)
	alias = db.Column(db.String(50))
	lastname = db.Column(db.String(50))

	avatar_file = db.Column(db.String(20), nullable=False, default='default.png')

	def get_roles(self):
		return self.role_assignments

	def has_role(self, role):
		return any(role == role_assignment.role.name and role_assignment.role.active
			for role_assignment in self.role_assignments)

	def get_role_obj(self):
		role = self.role_assignments[0].role.name
		if role == 'student': #__STUDENT_ROLE:
			return Student.query.filter_by(id=self.id).first()
		if role == 'teacher': #__TEACHER_ROLE:
			return Teacher.query.filter_by(id=self.id).first()
		if role == 'admin': # __ADMIN_ROLE:
			return Admin.query.filter_by(id=self.id).first()
		return self

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.avatar_file}')"	

class Admin(User):
	__tablename__ = 'admin'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

	def __repr__(self):
		return f"Teacher('{self.username}', '{self.email}', '{self.avatar_file}')"	

class Teacher(User):
	__tablename__ = 'teacher'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	representative_name = db.Column(db.String(45))

	announcements = db.relationship("Announcement", backref="announcement_author", lazy=True)
	courses =  db.relationship("Course", secondary=taught_by, back_populates='teachers')
	quests = db.relationship("Quest", backref='quest_author', lazy=True)

	def __repr__(self):
		return f"Teacher('{self.username}', '{self.email}', '{self.avatar_file}')"	

class SubmissionStatus(enum.Enum):
	IN_PROGRESS = 'In Progress'
	SUBMITTED = 'Submitted'
	RETURNED = 'Returned'
	DROPPED = 'Dropped'

# Students should really only be able to be enrolled in one active lass
# per semester, currently system will only handle this situation

class Student(User):
	__tablename__ = 'student'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	student_id = db.Column(db.String(15))
	grad_year = db.Column(db.Integer(), nullable=False)

	# relationships
	courses =  db.relationship("Course", secondary=course_enrollment)
	submissions = db.relationship("QuestSubmission", back_populates="student")

	def get_xp(self):
		total_xp = 0
		enrolled_course = self.get_current_enrolled_course()
		if enrolled_course != None:
			returned_work = QuestSubmission.query.filter_by(course_id=enrolled_course.id,status=SubmissionStatus.RETURNED).all()
			for work in returned_work:
				total_xp += work.xp_awarded
		return total_xp
	
	def get_current_rank(self):
		rank = Rank.query.filter(Rank.xp<=self.get_xp()).order_by(Rank.xp.desc()).first()
		return rank

	def get_next_rank(self):
		rank = Rank.query.filter(Rank.xp>self.get_xp()).order_by(Rank.xp.asc()).first()
		return rank

	def get_current_enrolled_course(self):
		for course in self.courses:
			if course.archived == False:
				return course
		return None
	
	def get_course_history(self):
		return self.courses
		course_history = []
		for course in self.courses:
			if course.archived:
				course_history.append(course)
		return course_history

	def get_work_in_progress(self):
		in_progress = QuestSubmission.query.filter_by(status=SubmissionStatus.IN_PROGRESS, student_id=self.id).all()
		return in_progress

	def get_submitted_work_list(self):
		submitted = QuestSubmission.query.filter_by(status=SubmissionStatus.SUBMITTED, student_id=self.id).all()
		return submitted
	
	def get_completed_work_list(self):
		completed =  QuestSubmission.query.filter_by(status=SubmissionStatus.RETURNED, student_id=self.id).all()
		return completed

	def __repr__(self):
		return f"Student('{self.username}', '{self.email}', '{self.avatar_file}')"	



class Campaign(db.Model):
	__tablename__ = 'campaign'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text)

	quests = db.relationship("Quest", back_populates='campaign')



class Quest(db.Model):
	__tablename__ = "quest"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	description = db.Column(db.Text, nullable=True)
	xp = db.Column(db.Integer, nullable=False)
	expiry = db.Column(db.String(100), nullable=True)
	repeatable = db.Column(db.String(100), nullable=True)
	details = db.Column(db.Text, nullable=True)
	submission_instructions = db.Column(db.Text, nullable=True)

	campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	campaign = db.relationship('Campaign', back_populates='quests')
	required_quests = db.relationship(
		'Quest',
		secondary=quest_requirements,
		primaryjoin=(quest_requirements.c.base_quest_id == id),
		secondaryjoin=(quest_requirements.c.required_quest_id == id),
		backref = db.backref('required_quest', lazy='dynamic'), lazy='dynamic'
		)


class SubmissionFeedback(db.Model):
	__tablename__ = 'submission_feedback'
	id = db.Column(db.Integer, primary_key=True)
	submission_id = db.Column(db.Integer, db.ForeignKey('quest_submission.id'), nullable=False)
	teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
	feedback_text = db.Column(db.Text)
	feedback_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	teacher = db.relationship('Teacher')

class QuestSubmission(db.Model):
	__tablename__ = 'quest_submission'
	id = db.Column(db.Integer, primary_key=True)
	quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

	status = db.Column(db.Enum(SubmissionStatus, values_callable=lambda x: [str(member.value) for member in SubmissionStatus]), default=SubmissionStatus.IN_PROGRESS)
	started_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	submission_text = db.Column(db.Text)
	files = db.Column(db.Text)
	#subbmitted_on = db.Column(db.DateTime)

	xp_awarded = db.Column(db.Integer, default=0)

	# future add the ability to add Proficincy Standards to Student Work
	quest = db.relationship("Quest")
	student = db.relationship("Student", back_populates='submissions')
	course = db.relationship("Course")
	feedback = db.relationship("SubmissionFeedback")

	def get_quest_name(self):
		quest = Quest.query.filter_by(id=self.quest_id).first()
		# if there is a quest return the Name otherwise return None
		if quest:
			return quest.title
		return "None"

	def __repr__(self):
		return f"QuestSubmission('{self.quest.title}', '{self.status}')"

class Course(db.Model):
	__tablename__ = "course"
	id = db.Column(db.Integer, primary_key=True)
	course_code = db.Column(db.String(100))
	course_name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text)

	base_quest_map = db.Column(db.String(50)) # change this to foriegn key with quest maps is created
	grade = db.Column(db.String(2), nullable=False)
	block = db.Column(db.String(1), nullable=False)
	term = db.Column(db.String(10), nullable=False)
	archived = db.Column(db.Boolean, default=False, nullable=False)
	bc_curriculum = db.Column(db.String(100))

	teachers = db.relationship('Teacher', secondary=taught_by, back_populates='courses')

	students = db.relationship("Student", secondary=course_enrollment, back_populates="courses")
	
	def __repr__(self):
		return f"Course('{self.course_name}', '{self.description}')"

class Rank(db.Model):
	__tablename__ = "rank"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	xp = db.Column(db.Integer(), nullable=False)
	symbol_html = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"Rank('{self.name}', '{self.xp}')"

badge_requirements = db.Table("badge_requirements",
	db.Column('badge_id', db.Integer, db.ForeignKey('badge.id')),
	db.Column('required_quest_id', db.Integer, db.ForeignKey('quest.id'))
)

class Badge(db.Model):
	__tablename__ = "badge"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text)
	type = db.Column(db.String(100), nullable=False)  # Talents || Achievements || Awards

	required_quests = db.relationship("Quest", secondary=badge_requirements, backref = db.backref('badge_required_quest', lazy='dynamic'), lazy='dynamic')

	xp = db.Column(db.Integer(), nullable=False)
	badge_image = db.Column(db.String(100), nullable=False)

class MessageCategory(enum.Enum):
	MESSAGE = 'Message'
	IMPORTANT = 'Important'
	WARNING = 'Warning'
	PROBLEM = 'Problem'

class Announcement(db.Model):
	__tablename__ = 'announcement'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	message_category = db.Column(db.Enum(MessageCategory, values_callable=lambda x: [str(member.value) for member in MessageCategory]), default=MessageCategory.MESSAGE)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Announcement('{self.title}', '{self.content}')"

class CurricularCompetencies(db.Model):
	__tablename__ = 'competencies'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text, nullable=False)

'''
class Term(db.Model):
	__tablename__ = 'term'
	id = db.Column(db.Integer, primary_key=True)
	start_date = db.Column(db.DateTime, nullable=False)
	end_date = db.Column(db.DateTime, nullable=False)

Create a notification to be assigned to all users on creation of an announcement
When 
class Notification(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



course_taught_by = db.Table('course_taught_by', 
	db.Column('course_id', db.ForeignKey('course.id'), primary_key=True),
	db.Column('teacher_id', db.ForeignKey('teacher.id'), primary_key=True),
)
'''
