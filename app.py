from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hobby-pack:'+str((os.environ.get("PASS_DB")))+'@localhost:8889/hobby-pack'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://hobby-pack:'+str((os.environ.get("PASS_DB")))+'@localhost:5432/hobby-pack'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)