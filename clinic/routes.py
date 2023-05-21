from clinic import app
from clinic.forms import RegisterForm,LoginForm
from clinic.models import User
from flask import render_template,redirect,flash,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,LoginManager,logout_user,login_required,current_user


@app.route('/',strict_slashes=False)
@app.route('/home',strict_slashes=False)
def home():
	return render_template('home.html')


@app.route('/register',methods=('GET','POST'),strict_slashes=False)
def register():
	form = RegisterForm()
	if form.validate_on_submit():

		new_user = User(first_name = form.first_name.data,
			last_name=form.last_name.data,
			email=form.email.data,
			password_hash = generate_password_hash(form.password.data))
		db.session.add(new_user)
		db.session.commit()
		flash(f'{email} {first_name} {last_name} has been registered successfully')

	return render_template('register.html',form=form)


@app.route('/login',methods=('GET','POST'),strict_slashes=False)
def login():
	form = LoginForm()
	return render_template('login.html',form=form)

@app.route('/logout',strict_slashes=False)
def logout():
	return redirect(url_for('home'))

@app.route('/dashboard',methods=('GET','POST'),strict_slashes=False)
def dashboard():
	return "this is th dashboard"

@app.route('/about',strict_slashes=False)
def about_page():
	return render_template('about.html')

@app.route('/contact',methods=('GET','POST'),strict_slashes=False)
def contact_page():
	return render_template('contact.html')

@app.route('/bio',methods=('GET','POST'),strict_slashes=False)
def bio_data():
	return render_template('bio.html')