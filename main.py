from flask import request, redirect, render_template, session, flash
from app import db, app
from models import Hobbyist, Hobby, Place, Encounter, Blog
from hashingtools import checking_password_hash
import cgi

app.secret_key = 'super-secret-close-your-eyes'