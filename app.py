from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hobby-pack:-1<E+3*z !>@localhost:8889/hobby-pack'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)