from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,login_user,LoginManager,logout_user,login_required,current_user

app = Flask(__name__)
app.config['SECRET_KEY']='anythingsecretasasecretkey'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://victor:7mudaki@localhost/dr_bot_db"
db = SQLAlchemy(app)