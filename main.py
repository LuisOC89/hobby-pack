from flask import request, redirect, render_template, session, flash, url_for
from sqlalchemy import desc
from app import db, app
from models import Hobbyist, Hobby, Place, Blog, Bloganswer, Encounter, Chat, Chat_comment
from hashingtools import checking_password_hash
from utils import filling, now1, checking_existing_address_in_db
import cgi

app.secret_key = 'super-secret-close-your-eyes'

def logged_in_hobbyist():
    current_hobbyist = Hobbyist.query.filter_by(nickname=session['hobbyist']).first()
    return current_hobbyist

endpoints_without_login = ['login', 'signup', 'index']

@app.before_request
def require_login():
    if not ('hobbyist' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

@app.route('/', methods=['POST','GET'])
def index():    
    hobbyists = Hobbyist.query.order_by(Hobbyist.state).order_by(Hobbyist.nickname).all()
    hobbies = Hobby.query.order_by(Hobby.name).all()
    places = Place.query.order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()
    encounters = Encounter.query.all()
    posts = Blog.query.all()

    #For the process of signing up. To pass "None" to the view as text
    welcome_message = str(request.args.get("welcome_message"))
    if (welcome_message == "None") :
        welcome_message = "None"

    #Create dictionary to post amount of hobbyists per hobby. Structure: dictionary = {"hobby1": "4" hobbyists, "hobby2": "3" hobbyists}
    dict_hobby_hobbyists = {}
    total_hobbies = Hobby.query.all()
    for hobby in total_hobbies:
        dict_hobby_hobbyists[hobby.name]=Hobbyist.query.filter(Hobbyist.hobbies.any(id=hobby.id)).count()

    #This will have all the posts with their answers: {Post1: [answer1, answer2, answer3], Post2: [answer1]}
    dict_posts_and_its_answers = {}
    for post in posts:
        #Initializing the list of lists
        dict_posts_and_its_answers[post.id] = []                
                        
        this_post_answers = Bloganswer.query.filter_by(blog_id=post.id).all()                 
                        
        for b_answer in this_post_answers:
            print (b_answer)
            dict_posts_and_its_answers[post.id].append(b_answer)
                
    return render_template('zindex.html',title="Hobby Pack - Sharing our hobbies", hobbyists=hobbyists, hobbies=hobbies, places=places, encounters=encounters, postshtml=posts, users_per_hobby=dict_hobby_hobbyists, welcomessage=welcome_message, posts_and_answers=dict_posts_and_its_answers)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('zlogin.html', title="Logging in")
    elif request.method == 'POST':
        hobbyist_python = request.form['hobbyist_html']
        password_python = request.form['password_html']
        hobbyists = Hobbyist.query.filter_by(nickname=hobbyist_python)
        if hobbyists.count() == 1:
            hobbyist = hobbyists.first()
            if checking_password_hash(password_python, hobbyist.password) == True:
                session['hobbyist'] = hobbyist_python
                flash('Welcome back, ' + str(hobbyist_python) + '.', 'allgood')
                return redirect("/")
            elif checking_password_hash(password_python, hobbyist.password) == False:
                flash("Sorry " + str(hobbyist_python) + ", that was not your password. :( ", "error10")
                #return redirect("/login")
                return render_template('zlogin.html', hobbyistname=hobbyist_python)
        flash('This username does not exist. :/', "error10")
        return redirect("/login")

@app.route('/logout')
def saliendo():
    del session['hobbyist']
    return redirect('/')

@app.route('/blog', methods=['POST', 'GET'])
def listing_blogs():
    #conditional assuming the access is through a get request from homeblogposts clicking {{post.title}}
    conditional_get_request_id = str(request.args.get("id"))
    #conditional assuming the access is through a get request from homeblogposts clicking {{post.title}}
    conditional_get_request_hobbyist = str(request.args.get("hobbyist"))
    #My error here (AttributeError: 'NoneType' object has no attribute 'id') is that I was looking for this value in html in homeblogposts.html instead of index.html
    #print(conditional_get_request_id)
    #print(conditional_get_request_hobbyist)

    #This will help to identify if this is an answer to a post created or a new post created
    conditional_get_request_id_answer = str(request.args.get("answer_id"))

    #if both are none, it means that this is a get request without passing an attribute from the view to the controller
    if ((conditional_get_request_id == "None") and (conditional_get_request_hobbyist =="None")):
        
        #This one shows all the posts of everyone in the blog order by year, by month, by day, by hour, by minute
        posts_python = Blog.query.all()  

        #This will have all the posts with their answers: {Post1: [answer1, answer2, answer3], Post2: [answer1]}
        dict_posts_python_and_its_answers = {}
        for post in posts_python:
                #Initializing the list of lists
                dict_posts_python_and_its_answers[post.id] = []                
                                
                this_post_answers = Bloganswer.query.filter_by(blog_id=post.id).all()                 
                                
                for b_answer in this_post_answers:
                    print (b_answer)
                    dict_posts_python_and_its_answers[post.id].append(b_answer)

        return render_template('allhomeblogposts.html', title="Blogging Hobbies", postshtml=posts_python, posts_and_answers=dict_posts_python_and_its_answers)
    #if conditional_get_request_id is not "None", then we are bringing the attribute "id" from the view to the controller
    elif ((conditional_get_request_id != "None") and (conditional_get_request_hobbyist=="None")): 
        if conditional_get_request_id_answer=="None":
            database_id = int(conditional_get_request_id)
            #print(database_id)
            current_post = Blog.query.get(database_id)
            title_python = current_post.title
            #print(title_python)
            body_python = current_post.body
            #print(body_python)
            hobbyist_owner_python = current_post.blog.nickname
            #print(hobbyist_owner_python)
            return render_template('eachblog.html', title="Reading my blog", titlehtml = title_python, bodyhtml=body_python, ownerhtml = hobbyist_owner_python) 
        else:
            database_id = int(conditional_get_request_id_answer)
            #print(database_id)
            current_post_answer = Bloganswer.query.get(database_id)
            title_python = current_post_answer.title
            #print(title_python)
            body_python = current_post_answer.body
            #print(body_python)
            hobbyist_owner_python = current_post_answer.blogsanswer.nickname
            #print(hobbyist_owner_python)
            return render_template('eachblog.html', title="Reading my blog", titlehtml = title_python, bodyhtml=body_python, ownerhtml = hobbyist_owner_python) 

    #if conditional_get_request_hobbyist is not "None", then we are bringing the attribute "hobbyist" from the view to the controller
    elif ((conditional_get_request_id == "None") and (conditional_get_request_hobbyist != "None")):
        hobbyist_name = conditional_get_request_hobbyist
        #print(hobbyist_name)
        current_hobbyist = Hobbyist.query.filter_by(nickname=hobbyist_name).first()
        #print(current_hobbyist)
        #This one shows all the blogs of just this particular hobbyist
        current_hobbyist_id = current_hobbyist.id
        posts_python = Blog.query.filter_by(hobbyist_id=current_hobbyist_id).all()
        return render_template('allhomeblogposts.html', title="Just blogging",postshtml=posts_python, posts_and_answers="N/A")

@app.route('/hobbies', methods=['POST', 'GET'])
def listing_hobbies():  
    if request.method == "GET":  
        conditional = str(request.args.get("condition"))
        conditional_get_request_id = str(request.args.get("id"))    
        conditional_get_request_hobby = str(request.args.get("hobby"))    
        if ((conditional_get_request_id == "None") and (conditional_get_request_hobby =="None") and conditional=="None"):        
            all_hobbies = Hobby.query.all()  
            my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all() 
            not_my_hobbies = [x for x in all_hobbies if x not in my_hobbies]
            
            #Dictionary to help: {"swimming": [3 hobbyists, 1 place], "skating": [1 hobbyist, 7, places]}
            hobbies_amount_hobbyists_amount_places = {}
            for hobby in all_hobbies:
                hobbies_amount_hobbyists_amount_places[hobby.name]=[]
                hobbies_amount_hobbyists_amount_places[hobby.name].append(Hobbyist.query.filter(Hobbyist.hobbies.any(name=hobby.name)).count())
                hobbies_amount_hobbyists_amount_places[hobby.name].append(Place.query.filter(Place.hobbies.any(name=hobby.name)).count())
   
            return render_template('allhobbies.html', title="Hobbies", hobbieshtml=all_hobbies, myhobbies=my_hobbies, notmyhobbies=not_my_hobbies, dict_helper=hobbies_amount_hobbyists_amount_places)
                
        elif ((conditional_get_request_id != "None") and (conditional_get_request_hobby == "None")): 
            database_id = int(conditional_get_request_id)
            current_hobby = Hobby.query.get(database_id)
            hobby_python = current_hobby        
            my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all() 
            """elif ((conditional_get_request_id == "None") and (conditional_get_request_hobby != "None")):
                hobby_name = conditional_get_request_hobby        
                current_hobby = Hobby.query.filter_by(nickname=hobby_name).first()
                current_hobby_id = current_hobby.id
                posts_python = Hobby.query.filter_by(hobby_id=current_hobby_id).all()
                return render_template('hobbies.html', title="Hobbie Pack!", postshtml=posts_python)"""
           
            this_hobby_hobbyists = Hobbyist.query.filter(Hobbyist.hobbies.any(name=hobby_python.name)).order_by(Hobbyist.nickname).all()
            this_hobby_places = Place.query.filter(Place.hobbies.any(name=hobby_python.name)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()   

            #Dictionary to store hobbyists and places in the form of: {'place1.unique_key_address': [amount_of_hobbyists_for_place1,[hobbyist1, hobbyist2, hobbyist3]]}
            dict_where_place_what_hobbyists = {}
            for place in this_hobby_places:
                #Initializing the list of lists
                dict_where_place_what_hobbyists[place.unique_key_address] = []                
                this_place_no_hobbyists = Hobbyist.query.filter(Hobbyist.hobbies.any(name=hobby_python.name)).filter(Hobbyist.places.any(unique_key_address=place.unique_key_address)).order_by(Hobbyist.nickname).count() 
                dict_where_place_what_hobbyists[place.unique_key_address].append(this_place_no_hobbyists) #For zipcode of place
                #Initializing the second list (for hobbyists on this place)
                dict_where_place_what_hobbyists[place.unique_key_address].append([])
                this_place_hobbyists = Hobbyist.query.filter(Hobbyist.hobbies.any(name=hobby_python.name)).filter(Hobbyist.places.any(unique_key_address=place.unique_key_address)).order_by(Hobbyist.nickname).all()                 
                for hobbyist in this_place_hobbyists:
                    dict_where_place_what_hobbyists[place.unique_key_address][1].append(hobbyist) 
            
            return render_template('eachhobby.html', title="About this hobby", hobbyhtml = hobby_python, dict_place_hobbyists=dict_where_place_what_hobbyists, places=this_hobby_places, my_hobbies=my_hobbies, hobby_hobbyists=this_hobby_hobbyists) 

        if (conditional == "user_title"):        
            hobbies_python = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()                           
            return render_template('eachhobbyist.html', title="About this hobbyist", hobbieshtml=hobbies_python)

@app.route('/people', methods=['POST','GET'])
def showing_all_people():
    hobbyists = Hobbyist.query.order_by(Hobbyist.state).order_by(Hobbyist.zipcode).order_by(Hobbyist.nickname).all()

    #Dictionary to keep number of hobbies and places per hobbyist: {Luis: [2 hobbies, 3 places], Rafa: [3 hobbies, 1 place]}
    hobbyist_amount_hobbies_amount_places = {}
    for hobbyist in hobbyists:
        hobbyist_amount_hobbies_amount_places[hobbyist.nickname] = []
        #First value of the list for amount hobbies
        hobbyist_amount_hobbies_amount_places[hobbyist.nickname].append(Hobby.query.filter(Hobby.hobbyists.any(nickname=hobbyist.nickname)).count())
        #Second value of the list for amount of places
        hobbyist_amount_hobbies_amount_places[hobbyist.nickname].append(Place.query.filter(Place.hobbyists.any(nickname=hobbyist.nickname)).count())        
    return render_template('allhobbyists.html',title="Hobbyists", hobbyists=hobbyists, hobbyists_properties=hobbyist_amount_hobbies_amount_places)

@app.route('/places', methods=['POST', 'GET'])
def listing_public_places():  
    if request.method == "GET":  
        conditional = str(request.args.get("condition"))
        conditional_get_request_id = str(request.args.get("id"))    
        conditional_get_request_hobby = str(request.args.get("hobby"))    
        if ((conditional_get_request_id == "None") and (conditional_get_request_hobby =="None") and conditional=="None"):        
            all_places = Place.query.order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()      
            
            #---------------------------my_places_already = (Session.query(Place, Hobby, Hobbyist).filter(P))   
            #---------------------------my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()
            #---------------------------my_places = Place.query.filter(Place.)

            my_places = Place.query.filter(Place.hobbyists.any(nickname=logged_in_hobbyist().nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()
            
            #Subtracting places of the current user from all the places of the website 
            not_my_places = [x for x in all_places if x not in my_places]
                        
            #Place.query.filter(Place.hobbyists.nickname!=logged_in_hobbyist().nickname).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()

            # Helper: {"Place1": [#people, #hobbies], "Place2": [#people, #hobbies]}
            place_amount_people_amount_hobbies = {}
            for place in all_places:
                place_amount_people_amount_hobbies[place.unique_key_address]=[]
                place_amount_people_amount_hobbies[place.unique_key_address].append(Hobbyist.query.filter(Hobbyist.places.any(unique_key_address=place.unique_key_address)).count())
                place_amount_people_amount_hobbies[place.unique_key_address].append(Hobby.query.filter(Hobby.places.any(unique_key_address=place.unique_key_address)).count())
                
            return render_template('allplaces.html', title="Hobbie Pack!", placeshtml=all_places, myplaces=my_places, notmyplaces=not_my_places, dict_helper=place_amount_people_amount_hobbies)

        elif ((conditional_get_request_id != "None") and (conditional_get_request_hobby == "None")): 
            database_id = int(conditional_get_request_id)
            current_place = Place.query.get(database_id)
            my_places = Place.query.filter(Place.hobbyists.any(nickname=logged_in_hobbyist().nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()
            #my_hobbies_in_this_place1 = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).filter(Hobby.places.any(name=placehtml)).filter(Hobby.places.any(streetaddress=streethtml)).filter(Hobby.places.any(city=cityhtml)).filter(Hobby.places.any(state=statehtml)).filter(Hobby.places.any(zipcode=zipcodehtml)).all() 

            hobbies_in_this_place = Hobby.query.filter(Hobby.places.any(id=database_id)).all() 
            amount_hobbies_in_this_place = Hobby.query.filter(Hobby.places.any(id=database_id)).count() 
            hobbyists_in_this_place = Hobbyist.query.filter(Hobbyist.places.any(id=database_id)).all()
            amount_hobbyists_in_this_place = Hobbyist.query.filter(Hobbyist.places.any(id=database_id)).count()
            #hobbyists_in_this_place
            
            #Create dictionary to post amount of hobbyists and amount of places in a hobby. Structure: dictionary = {"hobby1": ["4" hobbyists, "3" places], "hobby2": ["3" hobbyists, "0" places]}
            dict_hobby_hobbyists_places = {}
            total_hobbies = Hobby.query.all()
            for hobby in total_hobbies:
                dict_hobby_hobbyists_places[hobby.name]=[]
                dict_hobby_hobbyists_places[hobby.name].append(Hobbyist.query.filter(Hobbyist.hobbies.any(id=hobby.id)).count())
                dict_hobby_hobbyists_places[hobby.name].append(Place.query.filter(Place.hobbies.any(id=hobby.id)).count())
                
            #Checking dictionary just created
            for hobby1 in dict_hobby_hobbyists_places:
                print(hobby1, dict_hobby_hobbyists_places[hobby1][0], dict_hobby_hobbyists_places[hobby1][1])    

            #Create dictionary to post amount of hobbies and amount of places per hobbyist. Structure: dictionary = {"hobbyist1": ["4" hobbies, "3" places], "hobbyist2": ["3" hobbies, "0" places]}
            dict_hobbyist_hobbies_places = {}
            total_hobbyists = Hobbyist.query.all()
            for hobbyist in total_hobbyists:
                dict_hobbyist_hobbies_places[hobbyist.nickname]=[]
                dict_hobbyist_hobbies_places[hobbyist.nickname].append(Hobby.query.filter(Hobby.hobbyists.any(id=hobbyist.id)).count())
                dict_hobbyist_hobbies_places[hobbyist.nickname].append(Place.query.filter(Place.hobbyists.any(id=hobbyist.id)).count())

            '''test = Hobbyist.query.join(hobbieshobbyists).join(Hobby).filter(Hobbyist.places.any(id=database_id))
            print(Hobbyist.query.join(hobbieshobbyists).join(Hobby).filter(Hobbyist.places.any(id=database_id)).count())
            print(test.count())'''

            return render_template('eachplace.html', placehtml = current_place, hobbies=hobbies_in_this_place, no_hobbies=amount_hobbies_in_this_place, hobbyists=hobbyists_in_this_place, no_hobbyists=amount_hobbyists_in_this_place, hobby_no_hobbyists_no_places=dict_hobby_hobbyists_places, hobbyist_no_hobbies_no_places=dict_hobbyist_hobbies_places, my_places=my_places)#, test=test)
        """elif ((conditional_get_request_id == "None") and (conditional_get_request_hobby != "None")):
            hobby_name = conditional_get_request_hobby        
            current_hobby = Hobby.query.filter_by(nickname=hobby_name).first()
            current_hobby_id = current_hobby.id
            posts_python = Hobby.query.filter_by(hobby_id=current_hobby_id).all()
            return render_template('hobbies.html', title="Hobbie Pack!", postshtml=posts_python)"""
        '''if (conditional == "user_title"):        
            hobbies_python = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()                           
            return render_template('eachhobbyist.html', title="Hobbie Pack!", hobbieshtml=hobbies_python)'''

''' for encounters: Just for an idea:
#How to organize based on date and time:
        #I subtract the substrings, convert them and compared them: (( date: MM/DD/YYYY time: HH/MM )) 
        #year=Blog.date[6:4] #starting at space 6 and taking 4 spaces
        #month=Blog.date[0:2]
        #day=Blog.date[3:2]
        #hour=Blog.time[0:2]
        #minutes=Blog.time[3:2]


#This dict will take all the info from the query and organize the posts by year, month, day, hour and minute, plus containing some important info used in the
        dict_organized_posts = {}
        for post in posts_python:
            dict_organized_posts[post.id]=[]
            dict_organized_posts[post.id].append(post.title)
            dict_organized_posts[post.id].append(post.blog.nickname)
            dict_organized_posts[post.id].append(post.time) #for the whole time
            dict_organized_posts[post.id].append(post.time[0:2]) #for the hours
            dict_organized_posts[post.id].append(post.time[3:2]) #for the minutes
            dict_organized_posts[post.id].append(post.date) #for the whole date
            dict_organized_posts[post.id].append(post.date[6:4]) #for the year
            dict_organized_posts[post.id].append(post.date[0:2]) #for the month
            dict_organized_posts[post.id].append(post.date[3:2]) #for the day
            
#It would have the structure: {(id1: 1, [title, nickname, wholetime, hours, minutes, date, year, month, day] }
             '''

@app.route("/myinfo", methods=['GET', 'POST'])
def my_info():     
    if request.method == 'GET':
        condition=request.args.get('condition') 
        #To show the info of the user is logged in       
        if condition == "show_all_info_user":
            hobbyist = logged_in_hobbyist()
            conditional = "my_profile"
            #To show the info of other user in the website
        elif condition == "show_other_info_user": 
            hobbyist = Hobbyist.query.filter_by(nickname=request.args.get('hobbyist')).first()
            conditional = "other_user_profile"
        my_hobbies = Hobby.query.order_by(Hobby.name).filter(Hobby.hobbyists.any(nickname=hobbyist.nickname)).all()  
        my_places = Place.query.filter(Place.hobbyists.any(nickname=hobbyist.nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()       
        my_posts = Blog.query.filter_by(hobbyist_id=hobbyist.id).all()
        my_encounters = Encounter.query.all()  
        #Dictionary to store hobbies and places in the form of {'hobby1':[place1, place2, place3], 'hobby2':[place1, place1]}. This is to see where the person practices what hobbies
        dict_what_hobbie_where_places = {}
        for hobby in my_hobbies:
            dict_what_hobbie_where_places[hobby.name] = []
            my_places_this_hobbie = Place.query.filter(Place.hobbies.any(name=hobby.name)).filter(Place.hobbyists.any(nickname=hobbyist.nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all() 
            for place in my_places_this_hobbie:
                dict_what_hobbie_where_places[hobby.name].append(place)

        return render_template('eachhobbyist.html', title="Hobby Pack - Sharing our hobbies", hobbyist=hobbyist, my_hobbies=my_hobbies, my_places=my_places, my_encounters=my_encounters, my_posts=my_posts, conditional=conditional, dict_hobby_places=dict_what_hobbie_where_places)
        
@app.route("/newhobbyist", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        hobbyistname = request.form['hobbyistnamesignup']
        password = request.form['passwordsignup']
        verify_password = request.form['verifysignup']
        email = request.form['emailaddresssignup']
        city = request.form['citysignup']
        state = request.form['statesignup']
        zipcode = request.form['zipsignup']
        #Validation for all fields not to be empty
        if ((password =="") or (verify_password=="") or (hobbyistname=="") or (email=="") or (city=="") or (zipcode=="") or (state=="")):
            error_empty = "One or more fields are invalid. Please do not leave any field empty." 
        else:
            error_empty = ""
        #Validation for username (length at least 3 and maximum 20)
        if ((len(hobbyistname) < 3) or (len(hobbyistname) > 20)):
            error_name = 'The nickname entered is invalid. It has to be at least 3 characters long and maximum 20 characters long.'
        elif (" " in hobbyistname):
            error_name = 'The nickname entered is invalid. It can not have a space.'
        else: 
            error_name = ""
        #Validation for Password (length at least 3 and maximum 20)
        if ((len(password) < 3) and (len(password) > 0)):
            error_password = 'The password entered is invalid. It has to be at least 3 characters long.'
        elif password != verify_password:
            error_password = 'Passwords do not match.'
        else:
            error_password = ""
        #Validation for city (length at least 4 in US)
        if ((len(city) < 4) and (len(city) > 0)):
            error_city = 'The city entered is invalid. It has to be at least 4 characters long.'    
        else:
            error_city = ""     
        #Validation for zipcode (length 5 in US)
        if ((len(zipcode) != 5) and (len(zipcode) > 0)):
            error_zip = 'The zip code entered is invalid. It has to be 5 characters long.'
        #validation just numbers in zipcode    
        elif (len(zipcode) == 5):
            indicator_letter = 0
            for character in zipcode:
                if character.isalpha():
                    indicator_letter = indicator_letter + 1   
                else:
                    indicator_letter = indicator_letter
            if indicator_letter != 0:
                error_zip = 'The zip code entered is invalid. It has to have just numbers.'
            else:
                error_zip = ""
        else:
            error_zip = ""
        #validation for email
        if (email != ""):
            if ((len(email) < 3) and (len(email) > 0)):
                error_email = 'The email address entered is invalid. It has to be at least 3 characters long.'            
            elif ((len(email) > 40)):
                error_email = 'The email address entered is invalid. It has to be 20 characters long maximum.'            
            elif ((" " in email) or ("@" not in email) or ("." not in email)):
                error_email = 'The email address entered is invalid.'
            else:
                error_email = ""
        else:
            error_email = ""
        #Final validation - Validation pre-database (checking all the data fields are valid)
        if ((error_empty != "") or (error_name != "") or (error_password != "") or (error_city != "") or (error_zip != "") or (error_email != "")):
            return render_template('newhobbyist.html', title="Signing up", nickname=hobbyistname, email=email, city=city, zipcode=zipcode, errorname=error_name, errorpassword=error_password, erroremail=error_email, errorcity=error_city, errorzip=error_zip, errorempty=error_empty)
        else:
            hobbyists = Hobbyist.query.filter_by(nickname=hobbyistname)
            #Check if there is an user with this name already in the database
            if hobbyists.count() == 0:
                #Check if there is an user with the same email address
                emails = Hobbyist.query.filter_by(email=email)
                if emails.count() == 0:
                    hobbyist = Hobbyist(hobbyistname, email, city, state, zipcode, password)
                    db.session.add(hobbyist)
                    db.session.commit()
                    session['hobbyist'] = hobbyist.nickname
                    #cookie to say hi or dont to new user
                    if 'visits' in session:
                        session['visits'] = session.get('visits') + 1
                    else:
                        session['visits'] = 1  
                    if (session['visits'] != 1):
                        welcome_message = 'Logged in. Welcome, ' + str(hobbyist.nickname)    
                    else:
                        welcome_message = ''
                    #flash('Logged in. Welcome, ' + str(hobbyist.nickname), 'allgood')
                    #Redirect and url_for are get requests. adding_post is the function controller in main. 
                    return redirect(url_for("index", title="Posting my ideas", welcome_message=welcome_message))
                else:
                    error_empty = '''The email address "''' + str(email) + '''" already exists. Are you sure you are not signed up already?'''                
                    return render_template('newhobbyist.html', title="Signing up" , nickname=hobbyistname, email=email, city=city, zipcode=zipcode, errorempty=error_empty)
            else:
                    error_empty = '''The hobbyist name "''' + str(hobbyistname) + '''" already exists. Please signup with another hobbyist name.'''                
                    return render_template('newhobbyist.html', title="Signing up", nickname=hobbyistname, email=email, city=city, zipcode=zipcode, errorempty=error_empty)        
    else:
        return render_template('newhobbyist.html', title="Signing up")

@app.route('/newpost', methods=['POST', 'GET'])
def adding_post():
    if request.method == "GET":
        # Because the url_for points to the function "adding_post"(controller), not the template "newpost.html" (view), we have to extract the value of the argument "welcomessage" first as a get request.
        # When welcomemessage is empty, it passes the value "None". 
        welcomessage=request.args.get('welcomessage')
        return render_template('newpost.html', title="Posting my ideas", welcomemessage=welcomessage)

    if request.method == 'POST':
        condition = request.form['condition']
        if condition == "from_new_post":

            post_title = request.form['posttitle']
            post_body = request.form['postbody']
            post_already_exists = Blog.query.filter_by(title=post_title).count()              

            #Validation to make sure that the new post has title. 
            if ((post_title =="") and (post_body!="")):
                error = "notitle"                       
            #Validation to make sure that the new post has body. 
            elif ((post_title !="") and (post_body=="")):
                error = "nobody"                   
            #Validation to make sure that the new post has both title and body. 
            elif ((post_title =="") and (post_body=="")):
                error = "bothempty"
            #Validation to make sure there are no other posts with the same title
            elif (post_already_exists == 1):
                error = "titleexists"
            else:
                error = ""

            if (error!=""):    
                return render_template('newpost.html',title="Posting an idea", newtitle=post_title, newbody=post_body, errorhtml = error)
            else:
                new_post = Blog(post_title, post_body, filling(now1().month)+"/"+filling(now1().day)+"/"+filling(now1().year), filling(now1().hour)+":"+filling(now1().minute), logged_in_hobbyist())
                db.session.add(new_post)
                db.session.commit()
                #print(new_post.id)
                return redirect('''/blog?id='''+str(new_post.id))
        elif condition == "from_answer_to_post":
            post_that_you_will_answer_id = request.form['post_id']
            post_that_you_will_answer = Blog.query.filter_by(id=post_that_you_will_answer_id).first()

            post_that_you_will_answer_existing_answers = Bloganswer.query.filter_by(blog_id=post_that_you_will_answer.id).all()    
                       
            return render_template("newpostanswer.html", post_to_answer=post_that_you_will_answer, answers=post_that_you_will_answer_existing_answers)

        elif condition=="from_new_answer_to_post":
            post_that_you_will_answer_id = request.form['post2answer_id']
            post_that_you_will_answer = Blog.query.filter_by(id=post_that_you_will_answer_id).first()

            post_title = request.form['posttitle']
            post_body = request.form['postbody']
            post_already_exists = Blog.query.filter_by(title=post_title).count()              

            #Validation to make sure that the new post has title. 
            if ((post_title =="") and (post_body!="")):
                error = "notitle"                       
            #Validation to make sure that the new post has body. 
            elif ((post_title !="") and (post_body=="")):
                error = "nobody"                   
            #Validation to make sure that the new post has both title and body. 
            elif ((post_title =="") and (post_body=="")):
                error = "bothempty"
            #Validation to make sure there are no other posts with the same title
            elif (post_already_exists == 1):
                error = "titleexists"
            else:
                error = ""

            if (error!=""):    
                return render_template('newpostanswer.html',title="Posting an idea", newtitle=post_title, newbody=post_body, errorhtml = error, post_to_answer=post_that_you_will_answer)
            else:
                post_body = request.form['postbody']                
                new_post_answer = Bloganswer(post_title, post_body, filling(now1().month)+"/"+filling(now1().day)+"/"+filling(now1().year), filling(now1().hour)+":"+filling(now1().minute), post_that_you_will_answer ,logged_in_hobbyist())
                db.session.add(new_post_answer)
                db.session.commit()
                #print(new_post_answer.id)
                return redirect('''/blog?id='''+str(new_post_answer.id)+'''&answer_id='''+str(new_post_answer.id))

@app.route('/newhobbie', methods=['POST', 'GET'])
def adding_hobbie():
    if request.method == "GET":
        return render_template('newhobby.html', title="New hobby")

    if request.method == 'POST':
        conditional = str(request.form['conditional'])              
        if (conditional == "to_add_new_hobby_to_current_user"):
            hobby_name = str(request.form['hobbyname'])    
            hobby_already_exists = Hobby.query.filter_by(name=hobby_name).count()  
            list_hobbies = []  
            #Validation to make sure that the new hobbie has a name. Client-side validation
            if (hobby_name =="") :
                error = "no_name"     
                return render_template('newhobby.html',title="New hobby", newhobbyname=hobby_name, errorhtml = error)
            #Validation to make sure that this hobby is not already in the database under other user
            elif (hobby_already_exists == 1):
                #Validation to make sure that this hobby is not already a hobby of this user
                my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()
                #print(type(my_hobbies))
                for hobby in my_hobbies:
                    list_hobbies.append(hobby.name)
                    #print(hobby)
                    #print(hobby.name)
                if (hobby_name in list_hobbies):
                    error = "hobby_already_exists_mine"                          
                else:            
                    error = "hobby_already_exists"     
                return render_template('newhobby.html',title="New hobby", newhobbyname=hobby_name, errorhtml = error)              
            else:
                new_hobbie = Hobby(hobby_name)
                db.session.add(new_hobbie)
                db.session.commit()           
                new_hobbie.hobbyists.append(logged_in_hobbyist()) 
                db.session.commit()    
                return redirect('''/hobbies?id='''+str(new_hobbie.id))
        elif (conditional == "to_add_existing_hobby_to_current_user"):
            conditional_to_redirect = str(request.form['conditional_to_redirect'])  
            hobby_name = request.form['hobbyname']     
            #current_hobby = Hobby.query
            print (hobby_name)
            #Validation to make sure that the new hobbie has a name. Client-side validation
            if (hobby_name =="") :
                error = "no_name"     
                return render_template('newhobby.html',title="New hobby", newhobbyname=hobby_name, errorhtml = error)
            else:                
                #new_hobbie = Hobby(hobby_name)  
                existing_hobbie = Hobby.query.filter_by(name=hobby_name).first()                        
                existing_hobbie.hobbyists.append(logged_in_hobbyist()) 
                db.session.commit()    
                if conditional_to_redirect == ("Display_specific_hobby") :
                    return redirect('''/hobbies?id='''+str(existing_hobbie.id))
                elif conditional_to_redirect == ("Display_all_hobbies") :
                    return redirect("/hobbies")

@app.route('/newplace', methods=['POST', 'GET'])
def adding_place():    
    hobbies_python = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()
    if request.method == "GET":         
        return render_template('newplace.html', title='New place', hobbieshtml=hobbies_python, errorvrepeated="")  
        
    if request.method == "POST":
        conditional = str(request.form['conditional'])        
        if (conditional == "to_add_new_place_to_current_hobby"):

            hobbies_practiced = request.form.getlist('hobbieschecked')
            placehtml = str(request.form['placename'])        
            streethtml = str(request.form['streetaddress'])
            cityhtml = str(request.form['city'])
            statehtml = str(request.form['states'])
            zipcodehtml = str(request.form['zips'])   
            
            #Validation for all fields not to be empty
            if ((placehtml =="") or (streethtml=="") or (cityhtml=="") or (zipcodehtml=="")):
                error_empty = "One or more fields are invalid. Please do not leave any field empty." 
            else:
                error_empty = ""
            #Validation for name of new place (length at least 10 and maximum 40)
            if ((len(placehtml) < 1) or (len(placehtml) > 40)):
                error_name = 'The name entered is invalid. It has to be at least 1 character long and maximum 40 characters long.'       
            else: 
                error_name = ""
            #Validation for street address of new place (length at least 10 and maximum 40)
            if ((len(streethtml) < 10) or (len(streethtml) > 40)):
                error_street = 'The street address entered is invalid. It has to be at least 10 characters long and maximum 40 characters long.'       
            else: 
                error_street = ""
            #Validation for city (length at least 4 in US)
            if ((len(cityhtml) < 4) and (len(cityhtml) > 0)):
                error_city = 'The city entered is invalid. It has to be at least 4 characters long.'    
            else:
                error_city = ""            
            #Validation for zipcode (length 5 in US)
            if ((len(zipcodehtml) != 5) and (len(zipcodehtml) > 0)):
                error_zip = 'The zip code entered is invalid. It has to be 5 characters long.'
            #validation just numbers in zipcode    
            elif (len(zipcodehtml) == 5):
                indicator_letter = 0
                for character in zipcodehtml:
                    if character.isalpha():
                        indicator_letter = indicator_letter + 1   
                    else:
                        indicator_letter = indicator_letter
                if indicator_letter != 0:
                    error_zip = 'The zip code entered is invalid. It has to have just numbers.'
                else:
                    error_zip = ""
            else:
                error_zip = ""
            #Final validation - Validation pre-database (checking all the data fields are valid)
            if ((error_empty != "") or (error_name != "") or (error_street != "") or (error_city != "") or (error_zip != "")):
                return render_template('newplace.html', title="New place", hobbieshtml=hobbies_python, newplacename=placehtml, staddress=streethtml, city=cityhtml, zipcode=zipcodehtml, errorname=error_name, errorst=error_street, errorcity=error_city, errorzip=error_zip, errorempty=error_empty, errorvrepeated="")
        
            #validation para same street same city same state same zipcode
            else:
                existing_places_same_street = Place.query.filter_by(streetaddress=streethtml)
                if checking_existing_address_in_db(streethtml, cityhtml, statehtml, zipcodehtml, existing_places_same_street) == True:
                    error_value_repeated = "This place is already registered on this web. If you want to add it to your places click "
                    return render_template('newplace.html', title="New place", hobbieshtml=hobbies_python, newplacename=placehtml, staddress=streethtml, city=cityhtml, zipcode=zipcodehtml, errorvrepeated=error_value_repeated)
                else:
                    error_value_repeated = ""  
                    #Validation to checked that the user selected at least one of his hobbies.
                    if (len(hobbies_practiced) == 0):
                        return render_template('newplace.html', title="New place", hobbieshtml=hobbies_python, newplacename=placehtml, staddress=streethtml, city=cityhtml, zipcode=zipcodehtml, errorvrepeated="", errornohobbies="You have to choose at least one of the hobbies you practice here.")
                    #This is for knowing how many values there are inside these lists
                    #my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).count()   
                    #print(my_hobbies)
                    #my_hobbies_in_this_place = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).filter(Hobby.places.any(name=placehtml)).filter(Hobby.places.any(streetaddress=streethtml)).filter(Hobby.places.any(city=cityhtml)).filter(Hobby.places.any(state=statehtml)).filter(Hobby.places.any(zipcode=zipcodehtml)).count() 
                    #print(my_hobbies_in_this_place)
                
                    #This is for knowing the values there are inside these lists
                    #my_hobbies1 = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()   
                    #print(my_hobbies1)
                    #my_hobbies_in_this_place1 = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).filter(Hobby.places.any(name=placehtml)).filter(Hobby.places.any(streetaddress=streethtml)).filter(Hobby.places.any(city=cityhtml)).filter(Hobby.places.any(state=statehtml)).filter(Hobby.places.any(zipcode=zipcodehtml)).all() 
                    #print(my_hobbies_in_this_place1)
                    
                    #my_hobbies1 will be a list with elements looking like: <Hobby_1>. If you want any value, you will have to do it with a for and a dot, like:
                    # for hobby in my_hobbies1:
                    #   print(hobby.name) 
                    else:                    
                        '''my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()  
                        my_hobbies_in_this_place = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).filter(Hobby.places.any(name=placehtml)).filter(Hobby.places.any(streetaddress=streethtml)).filter(Hobby.places.any(city=cityhtml)).filter(Hobby.places.any(state=statehtml)).filter(Hobby.places.any(zipcode=zipcodehtml)).all() 

                        for myhobbie in my_hobbies:
                            if myhobbie not in my_hobbies_in_this_place:
                                blablabla'''         

                        new_place = Place(placehtml, streethtml, cityhtml, statehtml, zipcodehtml)
                        db.session.add(new_place)
                        db.session.commit()           

                        #To find Place by key_address_validation and avoid duplicating values in database or assigning wrong values to data        
                        place = Place.query.filter_by(unique_key_address=placehtml+streethtml+cityhtml+statehtml+zipcodehtml).first()
                        
                        #To add place to user                          
                        new_place.hobbyists.append(logged_in_hobbyist()) 
                        db.session.commit() 

                        #To add place to hobbies
                        #print(type(request.form.getlist('hobbieschecked')))
                        #print(type(hobbies_practiced))
                        #print(hobbies_practiced)
                        #for hobby in hobbies_practiced:
                            #print(hobby)
                        for hobby in hobbies_practiced:               
                            existing_hobbie = Hobby.query.filter_by(name=hobby).first()                        
                            existing_hobbie.places.append(place) 
                            db.session.commit()    

                        """return redirect('''/blog?id='''+str(new_post_answer.id)+'''&answer_id='''+str(new_post_answer.id))"""
                        return redirect("/myinfo?condition=show_all_info_user&answer_id=Hobby Pack - Sharing our hobbies")
                        '''<a href="/myinfo?condition=show_all_info_user">                           
                        return redirect(url_for("index", title="Hobby Pack - Sharing our hobbies"))'''

        elif (conditional=="to_add_existing_place_to_my_places"):
            place_key_address = request.form['placename']            
            my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()
            qty_my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).count()
            print(qty_my_hobbies)

            if qty_my_hobbies != 0 :
                return render_template('newcurrentplace.html', title="Hobby Pack - Sharing our hobbies", hobbieshtml=my_hobbies, placekey=place_key_address, errorhobbies="")
            else:
                return render_template('newcurrentplace.html', title="Hobby Pack - Sharing our hobbies", hobbieshtml=my_hobbies, placekey=place_key_address, errorhobbies="NoHobbiesYet")

        elif (conditional=="current_place_to_my_hobbies"):
            place_key_address = request.form['placekey']  
            place = Place.query.filter_by(unique_key_address=place_key_address).first()
            hobbies_practiced = request.form.getlist('hobbieschecked')

            place.hobbyists.append(logged_in_hobbyist())    
            db.session.commit()

            for hobby in hobbies_practiced:               
                existing_hobbie = Hobby.query.filter_by(name=hobby).first()                        
                existing_hobbie.places.append(place) 
                db.session.commit()   
                       
            all_places = Place.query.order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()      
            my_places = Place.query.filter(Place.hobbyists.any(nickname=logged_in_hobbyist().nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all() 
            not_my_places = [x for x in all_places if x not in my_places]

            place_amount_people_amount_hobbies = {}
            for place in all_places:
                place_amount_people_amount_hobbies[place.unique_key_address]=[]
                place_amount_people_amount_hobbies[place.unique_key_address].append(Hobbyist.query.filter(Hobbyist.places.any(unique_key_address=place.unique_key_address)).count())
                place_amount_people_amount_hobbies[place.unique_key_address].append(Hobby.query.filter(Hobby.places.any(unique_key_address=place.unique_key_address)).count())
            
            return render_template('allplaces.html', title="Hobby Pack - Sharing our hobbies", placeshtml=all_places, myplaces=my_places, notmyplaces=not_my_places, dict_helper=place_amount_people_amount_hobbies)

        elif (conditional=="to_add_existing_hobby_to_existing_place"):
            this_hobby = request.form['hobbyname']
            my_places_this_hobbie = Place.query.filter(Place.hobbies.any(name=this_hobby)).filter(Place.hobbyists.any(nickname=logged_in_hobbyist().nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all() 
            all_places = Place.query.order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()
            my_places_not_this_hobby_yet = [x for x in all_places if x not in my_places_this_hobbie] 
            return render_template('existingplaceexistinghobby.html', title="Hobby Pack - Linking your hobbies to your places", missing_placeshtml_for_me_for_this_hobby=my_places_not_this_hobby_yet, hobby=this_hobby, errorempty="")

        elif (conditional=="picking_missing_place"):
            #To check that is directing here correctly
            #print("\n\nIM here\n\n")
            this_hobby = str(request.form['hobby'])
            #print(this_hobby)
            picked_place_id = str(request.form.get('radioplace')) 
            #If none of the places as options in radio buttons get selected           
            if picked_place_id == "None":       
                #print(this_hobby)   

                my_places_this_hobbie = Place.query.filter(Place.hobbies.any(name=this_hobby)).filter(Place.hobbyists.any(nickname=logged_in_hobbyist().nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all() 
                all_places = Place.query.order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()
                my_places_not_this_hobby_yet = [x for x in all_places if x not in my_places_this_hobbie] 
                return render_template('existingplaceexistinghobby.html', title="Hobby Pack - Linking your hobbies to your places", missing_placeshtml_for_me_for_this_hobby=my_places_not_this_hobby_yet, hobby=this_hobby, errorempty="You didn't select any option.")
            
            else:                
                place_id = int(picked_place_id)
                current_place = Place.query.filter_by(id=place_id).first()
                my_places = Place.query.filter(Place.hobbyists.any(nickname=logged_in_hobbyist().nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all() 
                
                if current_place not in my_places:
                    current_place.hobbyists.append(logged_in_hobbyist())    
                    db.session.commit()
                                         
                existing_hobbie = Hobby.query.filter_by(name=this_hobby).first()                        
                existing_hobbie.places.append(current_place) 
                db.session.commit()   

                print("fine")                
                return redirect('/myinfo?condition=show_all_info_user')

            #place = Place.query.filter_by(id=picked_place_id).first()
            #this_hobby = request.form['hobbyname']
            #my_places_this_hobbie = Place.query.filter(Place.hobbies.any(name=this_hobby)).filter(Place.hobbyists.any(nickname=logged_in_hobbyist().nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all() 
            #all_places = Place.query.order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all()
            #my_places_not_this_hobby_yet = [x for x in all_places if x not in my_places_this_hobbie] 
            #return render_template('existingplaceexistinghobby.html', title="Hobby Pack - Linking your hobbies to your places", missing_placeshtml_for_me_for_this_hobby=my_places_not_this_hobby_yet, hobby=this_hobby)













@app.route('/chat', methods=['POST', 'GET'])
def listing_chats():
    #This will identify if this is a post request
    if request.method == "GET":                
        
        #This will help to identify if this is a get request from a specific view
        conditional = str(request.args.get("condition"))

        #if conditional is none, it means that this is a get request without passing any attribute from the view to the controller, so its just a click on zBase.html
        if (conditional == "None"):
            
            #This one shows all the posts of everyone in the blog order by year, by month, by day, by hour, by minute
            # Example: posts_python = Blog.query.all()               
            #my_chats = Chat.query.filter(Chat.participants.any(nickname=logged_in_hobbyist().nickname)).all()

            #Finally. Join of two tables and ordering depending on a value of a table. It doesnt work at the moment to order
            my_chats = Chat.query.filter(Chat.participants.any(nickname=logged_in_hobbyist().nickname)).join(Chat_comment).order_by(desc(Chat_comment.id)).all()

            #This will have all the posts with their answers: {Post1: [answer1, answer2, answer3], Post2: [answer1]}
            '''dict_posts_python_and_its_answers = {}
            for post in posts_python:
                    #Initializing the list of lists
                    dict_posts_python_and_its_answers[post.id] = []                
                                    
                    this_post_answers = Bloganswer.query.filter_by(blog_id=post.id).all()                 
                                    
                    for b_answer in this_post_answers:
                        print (b_answer)
                        dict_posts_python_and_its_answers[post.id].append(b_answer)'''

             #This will have all the chats with their comments: 
             # {Chat1: [[chat_name_for_this_user, last_comment_this_chat, date_or_time, other_users_names],[comment1, comment2, comment3]], 
             # Chat2: [[chat_name_for_this_user, last_comment_this_chat, date_or_time, other_users_names],[comment1]]}            
            dict_chats_and_their_comments = {}
            for chat in my_chats:
                this_chat_comments = Chat_comment.query.filter_by(chat_id=chat.id).all() 
                name_to_process = chat.name.split(",") 
                for name in name_to_process:
                    if name != logged_in_hobbyist().nickname:
                        chat_name = name 
                #Initializing the list of lists                                
                dict_chats_and_their_comments[chat.id] = [] 
                #{chat1:[]}
                dict_chats_and_their_comments[chat.id].append([])
                #chat1:[[]]
                dict_chats_and_their_comments[chat.id][0].append(chat_name)                
                dict_chats_and_their_comments[chat.id][0].append(this_chat_comments[-1])
                print("\n"+this_chat_comments[-1].comment+"\n")

                #To decide wheather to show date or time
                date_this_chat_last_comment = this_chat_comments[-1].date
                time_this_chat_last_comment = this_chat_comments[-1].time

                #if year today is greater than year of comment 
                print("\n"+date_this_chat_last_comment+"\n")
                print("\n"+str(type(date_this_chat_last_comment))+"\n")
                
                year_last_comment=date_this_chat_last_comment[6:10]
                print("\n"+year_last_comment+"\n")

                if (int(now1().year) > int(date_this_chat_last_comment[6:10])):                     
                    date_or_time = date_this_chat_last_comment
                else:
                    if (now1().month > int(date_this_chat_last_comment[0:2])):
                        date_or_time = date_this_chat_last_comment                        
                    else:
                        if (now1().day > int(date_this_chat_last_comment[3:5])):
                            date_or_time = date_this_chat_last_comment
                        else:
                            date_or_time = time_this_chat_last_comment
                dict_chats_and_their_comments[chat.id][0].append(date_or_time)

                current_chat_hobbyists = Hobbyist.query.filter(Hobbyist.chats.any(id=chat.id)).all()   
                                 
                #To help me store names of people in this chat group: [person1, person2, person3]}
                this_chat_other_participants = []
                for hobbyist in current_chat_hobbyists:
                    if (hobbyist.nickname!=logged_in_hobbyist().nickname):
                        this_chat_other_participants.append(hobbyist.nickname)

                #To help me store the other people's names
                other_participants_to_text = ",".join(this_chat_other_participants)

                dict_chats_and_their_comments[chat.id][0].append(other_participants_to_text)

                #How to organize based on date and time:
                #I subtract the substrings, convert them and compared them: (( date: MM/DD/YYYY time: HH/MM )) 
                #year=Blog.date[6:10] #starting at space 6 and until space 10
                #month=Blog.date[0:2]
                #day=Blog.date[3:5]
                #hour=Blog.time[0:2]
                #minutes=Blog.time[3:5]

                dict_chats_and_their_comments[chat.id].append([])                                                
                for comment in this_chat_comments:
                    print (comment.comment)
                    dict_chats_and_their_comments[chat.id][1].append(comment)                

            #Example: return render_template('allhomeblogposts.html', title="Blogging Hobbies", postshtml=posts_python, posts_and_answers=dict_posts_python_and_its_answers)
            return render_template('allchats.html', title="Messages", chats=my_chats, chat_comments=dict_chats_and_their_comments)
        
        elif (conditional == "see_this_chat"):
            database_id = int(request.args.get("chat_id"))            
            current_chat = Chat.query.filter_by(id=database_id).first()                        
              
            name_to_process = current_chat.name.split(",") 
            for name in name_to_process:
                if name != logged_in_hobbyist().nickname:
                    chat_name = name 

            current_chat_hobbyists = Hobbyist.query.filter(Hobbyist.chats.any(id=database_id)).all()   
                                 
            #To help me store names of people in this chat group: [person1, person2, person3]
            other_participants = []
            for hobbyist in current_chat_hobbyists:
                if (hobbyist.nickname!=logged_in_hobbyist().nickname):
                    other_participants.append(hobbyist.nickname)
            
            other_participants_to_text = ",".join(other_participants)
                
            all_comments = Chat_comment.query.filter_by(chat_id=current_chat.id).all()
            my_comments = Chat_comment.query.filter_by(chat_id=current_chat.id).filter_by(hobbyist_id=logged_in_hobbyist().id).all()
    
            # dictionary_of_chats_and_their_seen_for_this_user_names
            # dict: {chat1: name_I_should_see, chat2: name_I_should_see}       
            return render_template('eachchat.html', title="Messages", chat=current_chat, chat_name=chat_name,comments=all_comments, my_comments=my_comments, other_participants=other_participants_to_text) 


        elif (conditional == "just_created_chat"):              
            database_id = int(request.args.get("chat_id"))            
            current_chat = Chat.query.filter_by(id=database_id).first()     

            name_to_process = current_chat.name.split(",") 
            for name in name_to_process:
                if name != logged_in_hobbyist().nickname:
                    chat_name = name 

            current_chat_hobbyists = Hobbyist.query.filter(Hobbyist.chats.any(id=database_id)).all()   
                                 
            #To help me store names of people in this chat group: [person1, person2, person3]
            other_participants = []
            for hobbyist in current_chat_hobbyists:
                if (hobbyist.nickname!=logged_in_hobbyist().nickname):
                    other_participants.append(hobbyist.nickname)
            
            other_participants_to_text = ",".join(other_participants)

            all_comments = Chat_comment.query.filter_by(chat_id=current_chat.id).all()
            my_comments = Chat_comment.query.filter_by(chat_id=current_chat.id).filter_by(hobbyist_id=logged_in_hobbyist().id).all()
    
            # dictionary_of_chats_and_their_seen_for_this_user_names
            # dict: {chat1: name_I_should_see, chat2: name_I_should_see}              
            return render_template('eachchat.html', title="Messages", chat=current_chat, chat_name=chat_name, comments=all_comments, my_comments=my_comments, other_participants=other_participants_to_text) 
        
        '''#if conditional_get_request_hobbyist is not "None", then we are bringing the attribute "hobbyist" from the view to the controller
        elif ((conditional_get_request_id == "None") and (conditional_get_request_hobbyist != "None")):
            hobbyist_name = conditional_get_request_hobbyist
            #print(hobbyist_name)
            current_hobbyist = Hobbyist.query.filter_by(nickname=hobbyist_name).first()
            #print(current_hobbyist)
            #This one shows all the blogs of just this particular hobbyist
            current_hobbyist_id = current_hobbyist.id
            posts_python = Blog.query.filter_by(hobbyist_id=current_hobbyist_id).all()
            return render_template('allhomeblogposts.html', title="Just blogging",postshtml=posts_python)
        '''

#TODO#3 Adding a chat (similar to adding a blog)

@app.route('/newchat', methods=['POST', 'GET'])
def creating_chat():
    #Same function than below post request, just watching behavior 
    if request.method == "GET":
        condition = request.args.get('condition')
        other_hobbyists = Hobbyist.query.filter(Hobbyist.id!=logged_in_hobbyist().id).order_by(Hobbyist.nickname).all() 

        #dict in the form: {user1: [hobby1, hobby2, hobby3], user2: [hobby3]}
        dict_user_hobbies = {}
        for user in other_hobbyists:
            dict_user_hobbies[user.nickname] = []
            hobbies_this_user = Hobby.query.filter(Hobby.hobbyists.any(nickname=user.nickname)).all() 
            for hobby in hobbies_this_user:                    
                dict_user_hobbies[user.nickname].append(hobby)
        
        if condition == "from_allchats_view":      
            return render_template('newchat.html',title="Creating a chat", other_people=other_hobbyists, errormessage="", errorpeople="", dict_user_hobbies=dict_user_hobbies)
        

    if request.method == 'POST':
        condition = request.form['condition']
        other_hobbyists = Hobbyist.query.filter(Hobbyist.id!=logged_in_hobbyist().id).order_by(Hobbyist.nickname).all() 

        #dict in the form: {user1: [hobby1, hobby2, hobby3], user2: [hobby3]}
        dict_user_hobbies = {}
        for user in other_hobbyists:
            dict_user_hobbies[user.nickname] = []
            hobbies_this_user = Hobby.query.filter(Hobby.hobbyists.any(nickname=user.nickname)).all() 
            for hobby in hobbies_this_user:                    
                dict_user_hobbies[user.nickname].append(hobby)
        '''for hobby in my_hobbies:
            dict_what_hobbie_where_places[hobby.name] = []
            my_places_this_hobbie = Place.query.filter(Place.hobbies.any(name=hobby.name)).filter(Place.hobbyists.any(nickname=hobbyist.nickname)).order_by(Place.state).order_by(Place.city).order_by(Place.zipcode).all() 
            for place in my_places_this_hobbie:
                dict_what_hobbie_where_places[hobby.name].append(place)'''

        if condition == "from_allchats_view":      
            '''my_chats = Chat.query.filter(Chat.participants.any(nickname=logged_in_hobbyist().nickname)).all()'''            
            return render_template('newchat.html',title="Creating a chat", other_people=other_hobbyists, errormessage="", errorpeople="", dict_user_hobbies=dict_user_hobbies)
        
        elif condition == "from_newchat_view_validation":
            initial_message = request.form['initial_message']
            people_invited = request.form.getlist('peoplechecked')
            
            #Validation to make sure that there is a message. 
            if (initial_message ==""):
                error_message = "nomessage"  
            else: 
                error_message = "" 

            #Validation to checked that the user selected at least one of his hobbies.
            if (len(people_invited) == 0):
                error_people = "nopeople"
            else:
                error_people = ""
                
            if (error_people != "") or (error_message != ""):                
                return render_template('newchat.html',title="Creating a chat", other_people=other_hobbyists, errormessage=error_message, errorpeople=error_people, dict_user_hobbies=dict_user_hobbies)
            else:
                if (len(people_invited) == 1):                    

                    #What happens if Luis invites Rafa. Is it the same if Rafa invites Luis?
                    #It would be Rafa,Luis vs. Luis,Rafa
                    #I'm going to sort the names alphabetically so it will always be the same name Luis,Rafa
                    if logged_in_hobbyist().nickname < people_invited[0]:
                        name_chat = logged_in_hobbyist().nickname+","+people_invited[0]
                    else:
                        name_chat = people_invited[0]+","+logged_in_hobbyist().nickname
                    
                    #To check if this chat already exists
                    chat_exists = Chat.query.filter_by(name=name_chat).count()  

                    #There is a chat already with this name
                    if (chat_exists == 1):                        
                        return render_template('newchat.html',title="Creating a chat", other_people=other_hobbyists, errormessage="", errorpeople="chat_exists", dict_user_hobbies=dict_user_hobbies, other_person=people_invited[0])
                    elif (chat_exists == 0):
                        is_a_group = False
                        
                        new_chat = Chat(is_a_group, name_chat)
                        db.session.add(new_chat)
                        db.session.commit()

                        #To add chat to users in chat   
                        # Self creator                       
                        new_chat.participants.append(logged_in_hobbyist()) 
                        # Other person
                        other_person = Hobbyist.query.filter_by(nickname=people_invited[0]).first()                         
                        new_chat.participants.append(other_person)
                        db.session.commit() 

                        #To add comment to database and relate to chat
                        this_chat = Chat.query.filter_by(name=name_chat).first()   
                        new_comment = Chat_comment(initial_message, filling(now1().month)+"/"+filling(now1().day)+"/"+filling(now1().year), filling(now1().hour)+":"+filling(now1().minute), logged_in_hobbyist(), this_chat)
                        db.session.add(new_comment)
                        db.session.commit()

                        #print(new_post.id)
                        return redirect("/chat?condition=just_created_chat&chat_id="+str(new_chat.id))
                
                elif (len(people_invited) > 1):   
                    people_invited_to_text = ",".join(people_invited)                     
                    return render_template('newgroup.html',title="Creating a chat", initial_message=initial_message, people_invited=people_invited_to_text)
                                       
        elif condition == "from_newgroup_view_validation":
            initial_message = request.form['initial_message']
            people_invited_as_text = request.form['people_invited']
            people_invited_back_to_list = people_invited_as_text.split(",")

            chat_name = request.form['group_name'] 
            
            '''for person in people_invited_back_to_list:
                print("\n"+person+"\n")'''

            #Validation to make sure that the user wrote a name.
            if (chat_name == ""):
                error_name = "empty"
            else:
                #To check if this chat already exists
                chat_exists = Chat.query.filter_by(name=chat_name).count()
                if (chat_exists == 1):   
                    error_name = "chat_exists"  
                else:
                    error_name = ""    

            if (error_name != ""):                
                return render_template('newgroup.html',title="Creating a chat", initial_message=initial_message, people_invited=people_invited_as_text, errorname=error_name, name_of_group=chat_name)
            else:                
                is_a_group = True
                            
                new_chat = Chat(is_a_group, chat_name)
                db.session.add(new_chat)
                db.session.commit()

                #To add chat to users in chat   
                # Self creator                       
                new_chat.participants.append(logged_in_hobbyist()) 
                
                # Other people
                for other_person in people_invited_back_to_list:
                    other_person_to_add = Hobbyist.query.filter_by(nickname=other_person).first()                         
                    new_chat.participants.append(other_person_to_add)
                    db.session.commit() 

                #To add comment to database and relate to chat
                this_chat = Chat.query.filter_by(name=chat_name).first()   
                new_comment = Chat_comment(initial_message, filling(now1().month)+"/"+filling(now1().day)+"/"+filling(now1().year), filling(now1().hour)+":"+filling(now1().minute), logged_in_hobbyist(), this_chat)
                db.session.add(new_comment)
                db.session.commit()

                #print(new_post.id)
                return redirect('''/chat?condition=just_created_chat&chat_id='''+str(new_chat.id))

        elif condition == "new_comment_existent_chat":
            message = request.form['comment']
            
            #Validation to make sure that there is a message. 
            if (message ==""):
                database_id = int(request.form["chat_id"])            
                current_chat = Chat.query.filter_by(id=database_id).first()   
                
                name_to_process = current_chat.name.split(",") 
                for name in name_to_process:
                    if name != logged_in_hobbyist().nickname:
                        chat_name = name 
                    
                current_chat_hobbyists = Hobbyist.query.filter(Hobbyist.chats.any(id=database_id)).all()   
                                 
                #To help me store names of people in this chat group: [person1, person2, person3]
                other_participants = []
                for hobbyist in current_chat_hobbyists:
                    if (hobbyist.nickname!=logged_in_hobbyist().nickname):
                        other_participants.append(hobbyist.nickname)
                
                other_participants_to_text = ",".join(other_participants)

                all_comments = Chat_comment.query.filter_by(chat_id=current_chat.id).all()
                my_comments = Chat_comment.query.filter_by(chat_id=current_chat.id).filter_by(hobbyist_id=logged_in_hobbyist().id).all()
        
                # dictionary_of_chats_and_their_seen_for_this_user_names
                # dict: {chat1: name_I_should_see, chat2: name_I_should_see}       
                return render_template('eachchat.html', title="Messages", chat=current_chat, chat_name=chat_name,comments=all_comments, my_comments=my_comments, other_participants=other_participants_to_text) 
            
            else:
                database_id = int(request.form["chat_id"])            
                current_chat = Chat.query.filter_by(id=database_id).first()   
                
                name_to_process = current_chat.name.split(",") 
                for name in name_to_process:
                    if name != logged_in_hobbyist().nickname:
                        chat_name = name 
                
                new_comment = Chat_comment(message, filling(now1().month)+"/"+filling(now1().day)+"/"+filling(now1().year), filling(now1().hour)+":"+filling(now1().minute), logged_in_hobbyist(), current_chat)
                db.session.add(new_comment)
                db.session.commit()
                
                current_chat_hobbyists = Hobbyist.query.filter(Hobbyist.chats.any(id=database_id)).all()   
                                 
                #To help me store names of people in this chat group: [person1, person2, person3]
                other_participants = []
                for hobbyist in current_chat_hobbyists:
                    if (hobbyist.nickname!=logged_in_hobbyist().nickname):
                        other_participants.append(hobbyist.nickname)
                
                other_participants_to_text = ",".join(other_participants)

                all_comments = Chat_comment.query.filter_by(chat_id=current_chat.id).all()
                my_comments = Chat_comment.query.filter_by(chat_id=current_chat.id).filter_by(hobbyist_id=logged_in_hobbyist().id).all()
        
                # dictionary_of_chats_and_their_seen_for_this_user_names
                # dict: {chat1: name_I_should_see, chat2: name_I_should_see}       
                return render_template('eachchat.html', title="Messages", chat=current_chat, chat_name=chat_name,comments=all_comments, my_comments=my_comments, other_participants=other_participants_to_text) 

@app.route('/event', methods=['POST', 'GET'])
def acting_on_events():
    #Same function than below post request, just watching behavior 
    if request.method == "GET":
        condition = request.args.get('condition')

        if condition == "None":
            return render_template('allchats.html')                
    
        if condition == "from_allchats_view":      
            return render_template('newchat.html',title="Creating a chat", other_people=other_hobbyists, errormessage="", errorpeople="", dict_user_hobbies=dict_user_hobbies)
        
    if request.method == 'POST':
        condition = request.form['condition']
        
        if condition == "from_allchats_view":      
            return render_template('newchat.html',title="Creating a chat", other_people=other_hobbyists, errormessage="", errorpeople="", dict_user_hobbies=dict_user_hobbies)
        

#TODO encounters (show all, show each)
#TODO adding encounters (add encounter, add attendance later, add recap, add comment)

# Views allevents.html, eachevent.html, newevent.html

if __name__ == '__main__':
    app.run()