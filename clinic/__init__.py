from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY']='anythingsecretasasecretkey'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://victor:7mudaki@localhost/dr_bot_db"
db = SQLAlchemy(app)