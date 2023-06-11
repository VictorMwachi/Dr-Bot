from clinic import app,db,login_manager
from clinic.forms import RegisterForm,LoginForm,BioForm,DiagnoseForm
from clinic.models import Users,Bio,Symptom,Diagnosis
from flask import render_template,redirect,flash,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
#from sklearn.ensemble import GradientBoostingClassifier
import pickle
import numpy as np

symp_dict = {'itching': 1, 'skin rash': 3, 'nodal skin eruptions': 4, 'continuous sneezing': 4,
'shivering': 5, 'chills': 3, 'joint pain': 3, 'stomach pain': 5, 'acidity': 3,
'ulcers on tongue': 4, 'muscle wasting': 3, 'vomiting': 5, 'burning micturition': 6,
'spotting urination': 6, 'fatigue': 4, 'weight gain': 3, 'anxiety': 4, 'cold hands and feets': 5,
'mood swings': 3, 'weight loss': 3, 'restlessness': 5, 'lethargy': 2, 'patches in throat': 6,
'irregular sugar level': 5, 'cough': 4, 'high fever': 7, 'sunken eyes': 3, 'breathlessness': 4,
'sweating': 3, 'dehydration': 4, 'indigestion': 5, 'headache': 3, 'yellowish skin': 3,
'dark urine': 4, 'nausea': 5, 'loss of appetite': 4, 'pain behind the eyes': 4, 'back pain': 3,
'constipation': 4, 'abdominal pain': 4, 'diarrhoea': 6, 'mild fever': 5, 'yellow urine': 4,
'yellowing of eyes': 4, 'acute liver failure': 6, 'fluid overload': 4, 'swelling of stomach': 7,
'swelled lymph nodes': 6, 'malaise': 6, 'blurred and distorted vision': 5, 'phlegm': 5,
'throat irritation': 4, 'redness of eyes': 5, 'sinus pressure': 4, 'runny nose': 5,
'congestion': 5, 'chest pain': 7, 'weakness in limbs': 7, 'fast heart rate': 5,
'pain during bowel movements': 5, 'pain in anal region': 6, 'bloody stool': 5,
'irritation in anus': 6, 'neck pain': 5, 'dizziness': 4, 'cramps': 4, 'bruising': 4,
'obesity': 4, 'swollen legs': 5, 'swollen blood vessels': 5, 'puffy face and eyes': 5,
'enlarged thyroid': 6, 'brittle nails': 5, 'swollen extremeties': 5, 'excessive hunger': 4,
'extra marital contacts': 5, 'drying and tingling lips': 4, 'slurred speech': 4, 'knee pain': 3,
'hip joint pain': 2, 'muscle weakness': 2, 'stiff neck': 4, 'swelling joints': 5,
'movement stiffness': 5, 'spinning movements': 6, 'loss of balance': 4, 'unsteadiness': 4,
'weakness of one body side': 4, 'loss of smell': 3, 'bladder discomfort': 4,
'foul smell ofurine': 5, 'continuous feel of urine': 6, 'passage of gases': 5,
'internal itching': 4, 'toxic look (typhos)': 5, 'depression': 3, 'irritability': 2,
'muscle pain': 2, 'altered sensorium': 2, 'red spots over body': 3, 'belly pain': 4,
'abnormal menstruation': 6, 'dischromic patches': 6, 'watering from eyes': 4,
'increased appetite': 5, 'polyuria': 4, 'family history': 5, 'mucoid sputum': 4,
'rusty sputum': 4, 'lack of concentration': 3, 'visual disturbances': 3,
'receiving blood transfusion': 5, 'receiving unsterile injections': 2, 'coma': 7,
'stomach bleeding': 6, 'distention of abdomen': 4, 'history of alcohol consumption': 5,
'blood in sputum': 5, 'prominent veins on calf': 6, 'palpitations': 4, 'painful walking': 2,
'pus filled pimples': 2, 'blackheads': 2, 'scurring': 2, 'skin peeling': 3,
'silver like dusting': 2, 'small dents in nails': 2, 'inflammatory nails': 2, 'blister': 4,
'red sore around nose': 2, 'yellow crust ooze': 3, 'prognosis': 5}


#GBC_model = GradientBoostingClassifier()
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
	form=DiagnoseForm()
	if form.validate_on_submit():
		new_symptoms = Symptom(symptom_1 = form.symptom_1.data,
				       symptom_2 = form.symptom_2.data,
				       symptom_3 = form.symptom_3.data,
				       symptom_4 = form.symptom_4.data,
				       user_id=current_user.id)
		db.session.add(new_symptoms)
		db.session.commit()
		db.session.refresh(new_symptoms)

		symp_list=[symp_dict.get(symp,0) for symp in str(new_symptoms).split(",")]
		for i in range(13):
			symp_list.append(0)

		result=model.predict(np.array(symp_list).reshape(1,-1))[0]

		new_diagnosis=Diagnosis(disease=result,user_id=current_user.id,symptoms_id=new_symptoms.id)
		db.session.add(new_diagnosis)
		db.session.commit()
		db.session.refresh(new_diagnosis)

		return redirect(url_for('diagnosis_result',id=new_diagnosis.id))
		
	else:
		if form.errors != {}:
			#print(form.errors)
			for error in form.errors.values():
				#print(error)
				flash(f'{error}',category='danger')

	
	return render_template('dashboard.html',form=form)

@app.route('/diagnosis/<int:id>',strict_slashes=False)
@login_required
def diagnosis_result(id=id):
	dis_rec = Diagnosis.query.filter_by(id=id).first()
	symptoms = Symptom.query.filter_by(id=dis_rec.id).first()
	user_bio=Bio.query.filter_by(user_id=current_user.id).first()

	return render_template('result.html',dis_rec=dis_rec,symptoms=symptoms,bio=user_bio)

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
