from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,IntegerField
from wtforms.validators import Length, EqualTo, DataRequired,Email

class RegisterForm(FlaskForm):
	"""RegisterForm"""
	email = StringField(label='Email',validators=[DataRequired(),Email()])
	first_name = StringField(label='First Name',validators=[Length(min=3),DataRequired()])
	last_name = StringField(label='Last Name',validators=[Length(min=3),DataRequired()])
	password = PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
	password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password'),DataRequired()])
	submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
	"""Login Form"""
	email = StringField(label='Email',validators=[DataRequired(),Email()])
	password = PasswordField(label='Password',validators=[DataRequired()])
	submit = SubmitField(label='Login')

class BioForm(FlaskForm):
	"""Bio data Form"""
	user_id = IntegerField()
	birthday = DateField(label='Date of Birth:',validators=[DataRequired()])
	town = StringField(label='Town:',validators=[DataRequired()])
	country = StringField(label='Country:',validators=[DataRequired()])
	phone = StringField(label='Phone Number:',validators=[DataRequired()])
	physical_address = StringField(label='Physical Adress:',validators=[DataRequired()])
	submit = SubmitField(label='Update')

class DiagnoseForm(FlaskForm):
	"""dianos form"""
	user_id = IntegerField()
	symptom_1 = StringField(label='Symptom_1:',validators=[DataRequired()])
	symptom_2 = StringField(label='Symptom_2:',validators=[DataRequired()])
	symptom_3 = StringField(label='Symptom_3:',validators=[DataRequired()])
	symptom_4 = StringField(label='Symptom_4:',validators=[DataRequired()])
	submit = SubmitField(label='Consult')


		