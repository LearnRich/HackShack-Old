from HackShak import db
from flask_login import UserMixin

class Quest(db.Model):
	__tablename__ = 'quests'