from flask_login import UserMixin
from clinic import db,app
class Users(UserMixin,db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	first_name = db.Column(db.String(25),nullable=False)
	last_name = db.Column(db.String(25),nullable=False)
	email = db.Column(db.String(100),nullable=False,unique=True)
	password_hash = db.Column(db.String(200),nullable=False)
	bio = db.relationship('Bio',backref='user',uselist=False, lazy=True)


	def __init__(self,first_name,last_name,email,password_hash):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password_hash = password_hash


class Bio(db.Model):
	"""docstring for bio"""
	id = db.Column(db.Integer(), primary_key=True)
	birthday = db.Column(db.Date(),nullable=False)
	physical_address = db.Column(db.String(500),nullable=False)
	town = db.Column(db.String(15),nullable=False)
	country = db.Column(db.String(20),nullable=False)
	phone = db.Column(db.String(15),nullable=False)
	user_id = db.Column(db.Integer(),db.ForeignKey('users.id'),nullable=False,unique=True)

	def __init__(self,birthday,phone,physical_address,town,country,user_id):
		self.birthday = birthday
		self.physical_address = physical_address
		self.town = town
		self.country = country
		self.phone = phone
		self.user_id = user_id
with app.app_context():
	db.create_all()