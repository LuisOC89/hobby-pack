from app import db
from hashingtools import make_password_hashing

#Table to help handling many-to-many-relationships between hobbies and hobbyists. Two columns, one for hobbyist id and other for hobbie id.
#hobbieshobbyists will be a table called "hobbieshobbyists" with two columns, one for the hobbies' ids and called "hobby_id" and the other
# called "hobbyist_id" for the hobbyists' ids.
hobbieshobbyists = db.Table('hobbieshobbyists',
    db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id')),
    db.Column('hobbyist_id', db.Integer, db.ForeignKey('hobbyist.id'))
)  

#Table to help handling many-to-many-relationships between places and hobbyists. Two columns, one for hobbyist id and other for place id.
placeshobbyists = db.Table('placeshobbyists',
    db.Column('place_id', db.Integer, db.ForeignKey('place.id')),
    db.Column('hobbyist_id', db.Integer, db.ForeignKey('hobbyist.id'))
)

#Table to help handling many-to-many-relationships between hobbyists and encounters. Two columns, one for hobbyist id and other for encounter id.
encountershobbyists = db.Table('encountershobbyists', 
    db.Column('encounter_id', db.Integer, db.ForeignKey('encounter.id')),
    db.Column('hobbyist_id', db.Integer, db.ForeignKey('hobbyist.id'))
)

#Table to help handling many-to-many-relationships between hobbies and places. Two columns, one for place id and other for hobbie id.
hobbiesplaces = db.Table('hobbiesplaces',
    db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id')),
    db.Column('place_id', db.Integer, db.ForeignKey("place.id"))
)

# Classes Hobbyist, Hobby, Place, Encounter, Blog
#A blog will belong to just one user (one-to-many-relationship)
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(120))
    date = db.Column(db.String(10))
    time = db.Column(db.String(5))     
    hobbyist_id = db.Column(db.Integer, db.ForeignKey('hobbyist.id'))
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.id'))
    blog_answers = db.relationship("Bloganswer", backref="bloganswer")

    def __init__(self, title, body, date, time, hobbyist_owner):
        self.title = title
        self.body = body
        self.date = date
        self.time = time        
        self.blog = hobbyist_owner

#A blog can have answers (one-to-many-relationship) from other users 
class Bloganswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(120))
    date = db.Column(db.String(10))
    time = db.Column(db.String(5))     
    hobbyist_id = db.Column(db.Integer, db.ForeignKey('hobbyist.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    def __init__(self, title, body, date, time, blog_related, user_owner):
        self.title = title
        self.body = body
        self.date = date
        self.time = time
        self.bloganswer = blog_related
        self.blogsanswer = user_owner

#A hobbyist can have blogs (one-to-many-relationship), hobbies, places, encounters (many-to-many-relationship) 
class Hobbyist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(40), unique=True)
    city = db.Column(db.String(60))
    state = db.Column(db.String(20))
    zipcode = db.Column(db.String(5))
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="blog")
    # "hobbies" will be an attribute in this class to relate class-table "Hobbyist" to class-table "Hobby" using helper table "hobbieshobbyists" and creating the attribute 
    # "hobbyists" indirectly in class-table "Hobby", thats why we dont declare field "hobbyists" in table "Hobby"
    hobbies = db.relationship('Hobby', secondary=hobbieshobbyists, backref=db.backref('hobbyists', lazy='dynamic'))
    places = db.relationship('Place', secondary=placeshobbyists, backref=db.backref('hobbyists', lazy='dynamic'))
    encounters = db.relationship('Encounter', secondary=encountershobbyists, backref=db.backref('hobbyists', lazy='dynamic'))
    blogsanswers = db.relationship("Bloganswer", backref="blogsanswer")

    def __init__(self, nickname, email, city, state, zipcode, password_to_be_hashed):
        self.nickname = nickname
        self.email = email
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.password = make_password_hashing(password_to_be_hashed)

#A hobby can have diferent hobbyists (many-to-many-relationship), places (many-to-many-relationship), encounters (one-to-many-relationship)
class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    places = db.relationship('Place', secondary=hobbiesplaces, backref=db.backref('hobbies', lazy='dynamic'))
    encounters = db.relationship("Encounter", backref="encounter")

    def __init__(self, name):
        self.name = name

#A place can have different hobbyists, hobbies, encounters (many-to-many-relationship)
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    streetaddress = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zipcode = db.Column(db.String(120))
    encounters = db.relationship("Encounter", backref="event")

    def __init__(self, name, staddress, city, state, zipcode):
        self.name = name
        self.streetaddress = staddress
        self.city = city
        self.state = state
        self.zipcode = zipcode
    
#An encounter can have a hobby, a place and different hobbyists (one-to-many-relationship)
class Encounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)    
    date = db.Column(db.String(10))
    start_time = db.Column(db.String(5))   
    duration_hours = db.Column(db.Integer)
    duration_minutes = db.Column(db.Integer)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    hobby_id = db.Column(db.Integer, db.ForeignKey('hobby.id'))

    def __init__(self, name, date, time, duration_hours, duration_minutes, holding_place, hobby_taking_place):
        self.name = name
        self.date = date
        self.time = time
        self.duration_hours = duration_hours
        self.duration_minutes = duration_minutes
        self.place = holding_place
        self.encounter = hobby_taking_place