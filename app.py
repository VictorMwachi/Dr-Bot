from flask import Flask,render_template,redirect,url_for

app = Flask(__name__)

@app.route('/',strict_slashes=False)
@app.route('/home',strict_slashes=False)
def home():
	return render_template('home.html')


@app.route('/register',methods=('GET','POST'),strict_slashes=False)
def register():
	return render_template('register.html')


@app.route('/login',methods=('GET','POST'),strict_slashes=False)
def login():
	return render_template('login.html')

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

if __name__ == '__main__':
	app.run(debug=True)