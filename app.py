from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
# Connection String To connect to database: app.config['SQLAlchemy_DATABASE_URI'] = 'type_of_database+driver://username:password@server:port-number/name-of-database'

# MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hobby-pack:'+str((os.environ.get("PASS_DB")))+'@localhost:8889/hobby-pack'

#PostgreSQL
# app.config OPTION running directly
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://hobby_pack:'+str((os.environ.get("PASS_DB")))+'@localhost:5432/hobby_pack'

#PostgreSQL
# app.config OPTION running with Docker
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://hobby_pack:'+str((os.environ.get("PASS_DB")))+'@host.docker.internal:5432/hobby_pack'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)