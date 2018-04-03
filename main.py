from flask import request, redirect, render_template, session, flash
from app import db, app
from models import Hobbyist, Hobby, Place, Encounter, Blog
from hashingtools import checking_password_hash
import cgi

app.secret_key = 'super-secret-close-your-eyes'

@app.route('/', methods=['POST','GET'])
def index():
    hobbyists = Hobbyist.query.all()
    return render_template('index.html',title="Blogz", hobbyists=hobbyists)

endpoints_without_login = ['login', 'signup', 'index', 'listing_blogs']

@app.before_request
def require_login():
    if not ('hobbyist' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

if __name__ == '__main__':
    app.run()