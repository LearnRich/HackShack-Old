

'''
class Notification(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
'''
