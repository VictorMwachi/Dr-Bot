from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField
from wtforms.validators import Length, EqualTo, DataRequired,Email

class RegisterForm(FlaskForm):
	"""docstring for RegisterForm"""
	email = StringField(label='Email',validators=[DataRequired(),Email()])
	first_name = StringField(label='First Name',validators=[Length(min=3),DataRequired()])
	last_name = StringField(label='Last Name',validators=[Length(min=3),DataRequired()])
	password = PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
	password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password'),DataRequired()])
	submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
	email = StringField(label='Email',validators=[DataRequired()])
	password = PasswordField(label='Password',validators=[DataRequired()])
	submit = SubmitField(label='Login')

class BioForm(FlaskForm):
	birthday = DateField(label='Date of Birth:')
	town = StringField(label='Town:')
	country = StringField(label='Country:')
	phone = StringField(label='Phone Number:')
	physical_address = StringField(label='Physical Adress:')
	submit = SubmitField(label='Update')


		