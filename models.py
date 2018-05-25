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

#Table to help handling many-to-many-relationships between hobbyists and encounters. Two columns, one for hobbyist id and other for encounter id.
encountershobbyistsattendance = db.Table('encountershobbyistsattendance', 
    db.Column('encounter_id', db.Integer, db.ForeignKey('encounter.id')),
    db.Column('hobbyist_id', db.Integer, db.ForeignKey('hobbyist.id'))
)

#Table to help handling many-to-many-relationships between hobbies and places. Two columns, one for place id and other for hobbie id.
hobbiesplaces = db.Table('hobbiesplaces',
    db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id')),
    db.Column('place_id', db.Integer, db.ForeignKey("place.id"))
)
chatshobbyists = db.Table('chatshobbyists',
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id')),
    db.Column('participant_id', db.Integer, db.ForeignKey("hobbyist.id"))
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
    comments = db.relationship("Chat_comment", backref="chat_comment")
    # "hobbies" will be an attribute in this class to relate class-table "Hobbyist" to class-table "Hobby" using helper table "hobbieshobbyists" and creating the attribute 
    # "hobbyists" indirectly in class-table "Hobby", thats why we dont declare field "hobbyists" in table "Hobby"
    hobbies = db.relationship('Hobby', secondary=hobbieshobbyists, backref=db.backref('hobbyists', lazy='dynamic'))
    places = db.relationship('Place', secondary=placeshobbyists, backref=db.backref('hobbyists', lazy='dynamic'))
    blogsanswers = db.relationship("Bloganswer", backref="blogsanswer")
    chats = db.relationship('Chat', secondary=chatshobbyists, backref=db.backref('participants', lazy='dynamic'))
    encounters = db.relationship('Encounter', secondary=encountershobbyists, backref=db.backref('hobbyists', lazy='dynamic'))
    encounters_attendance = db.relationship('Encounter', secondary=encountershobbyistsattendance, backref=db.backref('hobbyists_attendance', lazy='dynamic'))
    event_comments = db.relationship("Event_comment", backref="event_comment_user")    
    encounters_created = db.relationship('Encounter', backref="created_encounter")

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
    unique_key_address = db.Column(db.String(120))
    encounters = db.relationship("Encounter", backref="event")

    def __init__(self, name, staddress, city, state, zipcode):
        self.name = name
        self.streetaddress = staddress
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.unique_key_address = name+staddress+city+state+zipcode

#For chat feature
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_a_group = db.Column(db.Boolean)
    name = db.Column(db.String(1000))
    comments = db.relationship("Chat_comment", backref="chat_comments")

    def __init__(self, is_a_group, name_of_chat):
        self.is_a_group = is_a_group
        self.name = name_of_chat
        
class Chat_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    date = db.Column(db.String(10))
    time = db.Column(db.String(5)) 
    hobbyist_id = db.Column(db.Integer, db.ForeignKey('hobbyist.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id')) 

    def __init__(self, comment, date, time, comment_owner, chat_belonging):
        self.comment = comment
        self.date = date
        self.time = time
        self.chat_comment = comment_owner
        self.chat_comments = chat_belonging

class Encounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(60))       
    date = db.Column(db.String(10))
    start_time = db.Column(db.String(5)) 
    #201805131321 > 201705131321 > 201704131321 - YYYYMMDDHHMM 
    date_and_time_to_order = db.Column(db.String(12))  
    #HH:MM
    duration = db.Column(db.String(5))
    attendance_taken_status = db.Column(db.Boolean)
    attendance_taken_date_time = db.Column(db.String(16))
    event_key = db.Column(db.String(500))

    hobby_id = db.Column(db.Integer, db.ForeignKey('hobby.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    creator_hobbyist_id = db.Column(db.Integer, db.ForeignKey('hobbyist.id'))
    #Table encountershobbyists - People invited by creator and people that wanted to assist even if they were not invited 
    # - This is declared in the class Hobbyist and is many-to-many
    #Table encountershobbyistsattendance - People verified attendance by creator the day of the event
    # - This is declared in the class Hobbyist and is many-to-many    
    encounter_comments = db.relationship("Event_comment", backref="event_comment")

    def __init__(self, name, date, time, datetime_ordered, duration, attendance_taken_status, event_key, hobby, holding_place, hobbyist_creator):
        self.name = name
        self.date = date
        self.start_time = time
        self.date_and_time_to_order = datetime_ordered
        self.duration = duration
        self.attendance_taken_status = attendance_taken_status
        self.event_key = event_key 
        
        self.encounter = hobby        
        self.event = holding_place
        self.created_encounter = hobbyist_creator     

    def taking_attendance(self, attendance_taken_status, attendance_taken_date_time):
        self.attendance_taken_status = attendance_taken_status   
        self.attendance_taken_date_time = attendance_taken_date_time

class Event_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Kind of comment will have three possible values: "invitation", "recap", "before_event", "after_event"
    content = db.Column(db.String(1000))
    kind_of_comment = db.Column(db.String(12))
    event_id = db.Column(db.Integer, db.ForeignKey('encounter.id'))
    hobbyist_id = db.Column(db.Integer, db.ForeignKey('hobbyist.id'))

    def __init__(self, content, kind, event, user):
        self.content = content 
        self.kind_of_comment = kind
        self.event_comment = event
        self.event_comment_user = user
        
'''
    class Cat:
        def __init__(self):
        # every Cat comes into this world tired and hungry
            self.tired = True
            self.hungry = True
        def sleep(self):
            self.tired = False
            # a Cat always wakes up hungry
            self.hungry = True
        def eat(self):
            if self.hungry:
                self.hungry = False
            else:
                # eating when already full makes a Cat sleepy
                self.tired = True
        def noise(self):
            # sleepy cats say prrrr, energized cats say meow!
            if self.tired:
                return "prrrr"
            else:
                return "meow!"
    def main():
        tom = Cat()
        print("tom says:", tom.noise())
        tom.sleep()
        print("After sleeping, tom says:", tom.noise())

        OUTPUT
        tom says: prrrr
        After sleeping, tom says: meow!
        After eating, tom still says: meow!
        After eating again, tom says: prrrr
    '''