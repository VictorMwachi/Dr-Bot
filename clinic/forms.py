from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField

class RegisterForm(FlaskForm):
	"""docstring for RegisterForm"""
	email = StringField(label='Email')
	first_name = StringField(label='First Name')
	last_name = StringField(label='Last Name')
	password = PasswordField(label='Password')
	conf_password = PasswordField(label='Confirm Password')
	submit = SubmitField(label='Submit')

class LoginForm(FlaskForm):
	email = StringField(label='Email')
	password = PasswordField(label='Password')
	submit = SubmitField(label='Submit')

		