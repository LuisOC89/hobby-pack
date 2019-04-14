import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from conf.config import DB_TYPE, DB_DRIVER, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = '{}+{}://{}:{}@{}:{}/{}'.format(DB_TYPE, DB_DRIVER, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
app.config['SQLALCHEMY_ECHO'] = True

# Info about this here: https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Connection String To connect to database: app.config['SQLAlchemy_DATABASE_URI'] = 'type_of_database+driver://username:password@server:port-number/name-of-database'

# MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hobby-pack:'+str((os.environ.get("PASS_DB")))+'@localhost:8889/hobby-pack'

#PostgreSQL
# app.config OPTION running directly
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://hobby_pack:'+str((os.environ.get("PASS_DB")))+'@localhost:5432/hobby_pack'

# app.config OPTION running with Docker
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://hobby_pack:'+str((os.environ.get("PASS_DB")))+'@host.docker.internal:5432/hobby_pack'