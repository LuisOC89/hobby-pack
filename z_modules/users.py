from flask import request, render_template, flash, session, redirect, url_for

from app import db
from models import Hobbyist, Hobby, Place, Blog, Encounter
from hashingtools import checking_password_hash
from utils import logged_in_hobbyist

class zUser(object):
    def login(self):
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
    
    def saliendo(self):
        del session['hobbyist']
        return redirect('/')

    def signup(self):
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

    def showing_all_people(self):
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

    def my_info(self):     
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
            