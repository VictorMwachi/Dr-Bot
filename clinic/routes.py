from clinic import app,db,login_manager
from clinic.forms import RegisterForm,LoginForm,BioForm,DiagnoseForm
from clinic.models import Users,Bio,Symptom
from flask import render_template,redirect,flash,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
from sklearn.ensemble import GradientBoostingClassifier
import pickle


GBC_model = GradientBoostingClassifier()
model = pickle.load(open('dr_bot.sav', 'rb'))

login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/',strict_slashes=False)
@app.route('/home',strict_slashes=False)
def home():
	return render_template('home.html')


@app.route('/register',methods=('GET','POST'),strict_slashes=False)
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		new_user = Users(first_name = form.first_name.data,
			last_name=form.last_name.data,
			email=form.email.data,
			password_hash = generate_password_hash(form.password.data))
		db.session.add(new_user)
		db.session.commit()
		flash(f'{form.email.data} {form.first_name.data} {form.last_name.data} has been registered successfully',category='success')
		return redirect(url_for('login'))
	else:
		if form.errors != {}:
			#print(form.errors)
			for error in form.errors.values():
				#print(error)
				flash(f'{error}',category='danger')

	return render_template('register.html', form=form)


@app.route('/login',methods=('GET','POST'),strict_slashes=False)
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user=Users.query.filter_by(email=form.email.data).first()
		if user is None:
			flash('User not found,check email and try again or register to create an account',category='info')
		else:
			if check_password_hash(user.password_hash,form.password.data):
				login_user(user)
				flash(f'welcome {user.first_name} {user.last_name}, you logged in successfully',category='success')
				return redirect(url_for('dashboard'))
			else:
				flash('Incorrect password!!!, Enter password and try again',category='danger')
	else:
		if form.errors != {}:
			#print(form.errors)
			for error in form.errors.values():
				#print(error)
				flash(f'{error}',category='danger')
	return render_template('login.html',form=form)


@app.route('/logout',strict_slashes=False)
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/dashboard',methods=('GET','POST'),strict_slashes=False)
@login_required
def dashboard():
	symptoms = []
	form=DiagnoseForm()
	if form.validate_on_submit():
		new_symptoms = Symptom(symptom_1 = form.symptom_1.data,
				       symptom_2 = form.symptom_2.data,
				       symptom_3 = form.symptom_3.data,
				       symptom_4 = form.symptom_4.data,
				       user_id=current_user.id)
		db.session.add(new_symptoms)
		db.session.commit()
		symptoms=[form.symptom_1.data, form.symptom_2.data, form.symptom_3.data,  form.symptom_4.data]
		diagnosis = model.predict(symptoms)
	else:
		if form.errors != {}:
			#print(form.errors)
			for error in form.errors.values():
				#print(error)
				flash(f'{error}',category='danger')

	
	return render_template('dashboard.html',form=form,diagnosis=diagnosis)

@app.route('/about',strict_slashes=False)
def about_page():
	return render_template('about.html')

@app.route('/contact',methods=('GET','POST'),strict_slashes=False)
def contact_page():
	return render_template('contact.html')

@app.route('/bio',methods=('GET','POST'),strict_slashes=False)
@login_required
def bio_data():
	form = BioForm()
	bio = Bio.query.filter_by(user_id=current_user.id).first()

	if form.validate_on_submit():
		new_bio = Bio(town = form.town.data,
			country=form.country.data,
			physical_address=form.physical_address.data,
			birthday = form.birthday.data,
			phone = form.phone.data,
			user_id=current_user.id)

		if bio is None:
			db.session.add(new_bio)
		else:
			bio.town = form.town.data
			bio.country=form.country.data,
			bio.physical_address=form.physical_address.data,
			bio.birthday = form.birthday.data,
			bio.phone = form.phone.data,
			db.session.merge(bio)
		
		db.session.commit()
		flash(f'You have updated bio data sucessfully',category='success')
		return redirect(url_for('bio_data'))
	else:
		if form.errors != {}:
			#print(form.errors)
			for error in form.errors.values():
				#print(error)
				flash(f'{error}',category='danger')


	return render_template('bio.html',form=form,bio=bio)
