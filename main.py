from flask import request, redirect, render_template, session, flash, url_for
from app import db, app
from models import Hobbyist, Hobby, Place, Encounter, Blog
from hashingtools import checking_password_hash
import cgi

app.secret_key = 'super-secret-close-your-eyes'

@app.route('/', methods=['POST','GET'])
def index():
    hobbyists = Hobbyist.query.all()
    hobbies = Hobby.query.all()
    places = Place.query.all()
    encounters = Encounter.query.all()
    posts = Blog.query.all()
    return render_template('zindex.html',title="Hobby Pack", hobbyists=hobbyists, hobbies=hobbies, places=places, encounters=encounters, postshtml=posts)

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
        #Validation for email (length 5 in US)
        if ((len(zipcode) != 5) and (len(zipcode) > 0)):
            error_zip = 'The zip code entered is invalid. It has to be 5 characters long.'
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
            return render_template('newhobbyist.html', nickname=hobbyistname, email=email, city=city, zipcode=zipcode, errorname=error_name, errorpassword=error_password, erroremail=error_email, errorcity=error_city, errorzip=error_zip, errorempty=error_empty)
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
                    if (session['visits'] == 1):
                        welcome_message = 'Logged in. Welcome, ' + str(hobbyist.nickname)    
                    else:
                        welcome_message = ''
                    #flash('Logged in. Welcome, ' + str(hobbyist.nickname), 'allgood')
                    #Redirect and url_for are get requests. adding_post is the function controller in main. 
                    return redirect(url_for("adding_post", welcomessage=welcome_message))
                else:
                    error_empty = '''The email address "''' + str(email) + '''" already exists. Are you sure you are not signed up already?'''                
                    return render_template('newhobbyist.html', nickname=hobbyistname, email=email, city=city, zipcode=zipcode, errorempty=error_empty)
            else:
                    error_empty = '''The hobbyist name "''' + str(hobbyistname) + '''" already exists. Please signup with another hobbyist name.'''                
                    return render_template('newhobbyist.html', nickname=hobbyistname, email=email, city=city, zipcode=zipcode, errorempty=error_empty)        
    else:
        return render_template('newhobbyist.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('zlogin.html')
    elif request.method == 'POST':
        hobbyist_python = request.form['hobbyist_html']
        password_python = request.form['password_html']
        hobbyists = Hobbyist.query.filter_by(nickname=hobbyist_python)
        if hobbyists.count() == 1:
            hobbyist = hobbyists.first()
            if checking_password_hash(password_python, hobbyist.password) == True:
                session['hobbyist'] = hobbyist_python
                flash('Welcome back, ' + str(hobbyist_python) + '.', 'allgood')
                return redirect("/newpost")
            elif checking_password_hash(password_python, hobbyist.password) == False:
                flash("Sorry " + str(hobbyist_python) + ", that was not your password. :( ", "error10")
                #return redirect("/login")
                return render_template('zlogin.html', hobbyistname=hobbyist_python)
        flash('This username does not exist. :/', "error10")
        return redirect("/login")

@app.route('/blog', methods=['POST', 'GET'])
def listing_blogs():
    #conditional assuming the access is through a get request from homeblogposts clicking {{post.title}}
    conditional_get_request_id = str(request.args.get("id"))
    #conditional assuming the access is through a get request from homeblogposts clicking {{post.title}}
    conditional_get_request_hobbyist = str(request.args.get("hobbyist"))
    #My error here (AttributeError: 'NoneType' object has no attribute 'id') is that I was looking for this value in html in homeblogposts.html instead of index.html
    #print(conditional_get_request_id)
    #print(conditional_get_request_hobbyist)
    #if both are none, it means that this is a get request without passing an attribute from the view to the controller
    if ((conditional_get_request_id == "None") and (conditional_get_request_hobbyist =="None")):
        #This one shows all the posts of everyone in the blog 
        posts_python = Blog.query.all()  
        return render_template('allhomeblogposts.html',title="Hobbie Pack!", postshtml=posts_python)
    #if conditional_get_request_id is not "None", then we are bringing the attribute "id" from the view to the controller
    elif ((conditional_get_request_id != "None") and (conditional_get_request_hobbyist=="None")): 
        database_id = int(conditional_get_request_id)
        #print(database_id)
        current_post = Blog.query.get(database_id)
        title_python = current_post.title
        #print(title_python)
        body_python = current_post.body
        #print(body_python)
        hobbyist_owner_python = current_post.blog.nickname
        #print(hobbyist_owner_python)
        return render_template('eachblog.html', titlehtml = title_python, bodyhtml=body_python, ownerhtml = hobbyist_owner_python) 
    #if conditional_get_request_hobbyist is not "None", then we are bringing the attribute "hobbyist" from the view to the controller
    elif ((conditional_get_request_id == "None") and (conditional_get_request_hobbyist != "None")):
        hobbyist_name = conditional_get_request_hobbyist
        #print(hobbyist_name)
        current_hobbyist = Hobbyist.query.filter_by(nickname=hobbyist_name).first()
        #print(current_hobbyist)
        #This one shows all the blogs of just this particular hobbyist
        current_hobbyist_id = current_hobbyist.id
        posts_python = Blog.query.filter_by(hobbyist_id=current_hobbyist_id).all()
        return render_template('allhomeblogposts.html',title="Hobbie Pack!",postshtml=posts_python)

@app.route('/newpost', methods=['POST', 'GET'])
def adding_post():
    if request.method == "GET":
        # Because the url_for points to the function "adding_post"(controller), not the template "newpost.html" (view), we have to extract the value of the argument "welcomessage" first as a get request.
        # When welcomemessage is empty, it passes the value "None". 
        welcomessage=request.args.get('welcomessage')
        return render_template('newpost.html', welcomemessage=welcomessage)

    if request.method == 'POST':
        post_title = request.form['posttitle']
        post_body = request.form['postbody']
        #Validation to make sure that the new post has a title and a body. Client-side validation
        if ((post_title =="") and (post_body!="")):
            error = "notitle"     
            return render_template('newpost.html',title="Hobbies Pack!", newtitle=post_title, newbody=post_body, errorhtml = error)       
        elif ((post_title !="") and (post_body=="")):
            error = "nobody"    
            return render_template('newpost.html',title="Hobbies Pack!", newtitle=post_title, newbody=post_body, errorhtml = error)        
        elif ((post_title =="") and (post_body=="")):
            error = "bothempty"
            return render_template('newpost.html',title="Hobbies Pack!", newtitle=post_title, newbody=post_body, errorhtml = error)
        else:
            new_post = Blog(post_title, post_body, logged_in_hobbyist())
            db.session.add(new_post)
            db.session.commit()
            #print(new_post.id)
            return redirect('''/blog?id='''+str(new_post.id))

@app.route('/logout')
def saliendo():
    del session['hobbyist']
    return redirect('/')

@app.route('/people', methods=['POST','GET'])
def showing_all_people():
    hobbyists = Hobbyist.query.all()
    return render_template('allhobbyists.html',title="Hobby Pack", hobbyists=hobbyists)

endpoints_without_login = ['login', 'signup', 'index', 'listing_blogs']

@app.before_request
def require_login():
    if not ('hobbyist' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

@app.route('/hobbies', methods=['POST', 'GET'])
def listing_hobbies():  
    if request.method == "GET":  
        conditional = str(request.args.get("condition"))
        conditional_get_request_id = str(request.args.get("id"))    
        conditional_get_request_hobby = str(request.args.get("hobby"))    
        if ((conditional_get_request_id == "None") and (conditional_get_request_hobby =="None") and conditional=="None"):        
            hobbies_python = Hobby.query.all()  
            hobbyists_python = Hobbyist.query.all()
            places_python = Place.query.all()
            return render_template('allhobbies.html', title="Hobbie Pack!", hobbieshtml=hobbies_python, hobbyistshtml=hobbyists_python, placeshtml=places_python)
        elif ((conditional_get_request_id != "None") and (conditional_get_request_hobby == "None")): 
            database_id = int(conditional_get_request_id)
            current_hobby = Hobby.query.get(database_id)
            hobby_python = current_hobby.name        
            return render_template('eachhobby.html', hobbyhtml = hobby_python) 
        """elif ((conditional_get_request_id == "None") and (conditional_get_request_hobby != "None")):
            hobby_name = conditional_get_request_hobby        
            current_hobby = Hobby.query.filter_by(nickname=hobby_name).first()
            current_hobby_id = current_hobby.id
            posts_python = Hobby.query.filter_by(hobby_id=current_hobby_id).all()
            return render_template('hobbies.html', title="Hobbie Pack!", postshtml=posts_python)"""
        if (conditional == "user_title"):        
            hobbies_python = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()                           
            return render_template('eachhobbyist.html', title="Hobbie Pack!", hobbieshtml=hobbies_python)


@app.route('/newhobbie', methods=['POST', 'GET'])
def adding_hobbie():
    if request.method == "GET":
        return render_template('newhobby.html')

    if request.method == 'POST':
        conditional = str(request.form['conditional'])
        if (conditional == "to_add_new_hobby_to_current_user"):
            hobby_name = request.form['hobbyname']        
            #Validation to make sure that the new hobbie has a name. Client-side validation
            if (hobby_name =="") :
                error = "no_name"     
                return render_template('newhobby.html',title="Hobbies Pack!", newhobbyname=hobby_name, errorhtml = error)
            else:
                new_hobbie = Hobby(hobby_name)
                db.session.add(new_hobbie)
                db.session.commit()           
                new_hobbie.hobbyists.append(logged_in_hobbyist()) 
                db.session.commit()    
                return redirect('''/hobbies?id='''+str(new_hobbie.id))
        elif (conditional == "to_add_existing_hobby_to_current_user"):
            hobby_name = request.form['hobbyname']     
            #current_hobby = Hobby.query
            print (hobby_name)
            #Validation to make sure that the new hobbie has a name. Client-side validation
            if (hobby_name =="") :
                error = "no_name"     
                return render_template('newhobby.html',title="Hobbies Pack!", newhobbyname=hobby_name, errorhtml = error)
            else:
                #new_hobbie = Hobby(hobby_name)  
                existing_hobbie = Hobby.query.filter_by(name=hobby_name).first()                        
                existing_hobbie.hobbyists.append(logged_in_hobbyist()) 
                db.session.commit()    
                return redirect('''/hobbies?id='''+str(existing_hobbie.id))

def logged_in_hobbyist():
    current_hobbyist = Hobbyist.query.filter_by(nickname=session['hobbyist']).first()
    return current_hobbyist

@app.route('/places', methods=['POST', 'GET'])
def listing_public_places():  
    if request.method == "GET":  
        conditional = str(request.args.get("condition"))
        conditional_get_request_id = str(request.args.get("id"))    
        conditional_get_request_hobby = str(request.args.get("hobby"))    
        if ((conditional_get_request_id == "None") and (conditional_get_request_hobby =="None") and conditional=="None"):        
            places_python = Place.query.all()       

            #---------------------------my_places_already = (Session.query(Place, Hobby, Hobbyist).filter(P))   
            #---------------------------my_hobbies = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()
            #---------------------------my_places = Place.query.filter(Place.)

            my_places = Place.query.filter(Place.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()
            

            return render_template('allplaces.html', title="Hobbie Pack!", placeshtml=places_python, myplaces=my_places)
        '''elif ((conditional_get_request_id != "None") and (conditional_get_request_hobby == "None")): 
            database_id = int(conditional_get_request_id)
            current_hobby = Hobby.query.get(database_id)
            hobby_python = current_hobby.name        
            return render_template('eachhobby.html', hobbyhtml = hobby_python) '''
        """elif ((conditional_get_request_id == "None") and (conditional_get_request_hobby != "None")):
            hobby_name = conditional_get_request_hobby        
            current_hobby = Hobby.query.filter_by(nickname=hobby_name).first()
            current_hobby_id = current_hobby.id
            posts_python = Hobby.query.filter_by(hobby_id=current_hobby_id).all()
            return render_template('hobbies.html', title="Hobbie Pack!", postshtml=posts_python)"""
        '''if (conditional == "user_title"):        
            hobbies_python = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()                           
            return render_template('eachhobbyist.html', title="Hobbie Pack!", hobbieshtml=hobbies_python)'''

@app.route('/newplace', methods=['POST', 'GET'])
def adding_place():
    if request.method == "GET":
        hobbies_python = Hobby.query.filter(Hobby.hobbyists.any(nickname=logged_in_hobbyist().nickname)).all()
        return render_template('newplace.html', hobbieshtml=hobbies_python)  
    if request.method == "POST":
        hobbies_practiced = request.form.getlist('hobbieschecked')
        placehtml = str(request.form['placename'])        
        streethtml = str(request.form['streetaddress'])
        cityhtml = str(request.form['city'])
        statehtml = str(request.form['states'])
        zipcodehtml = str(request.form['zips'])
        
        new_place = Place(placehtml, streethtml, cityhtml, statehtml, zipcodehtml)
        db.session.add(new_place)
        db.session.commit()           
                  
        place = Place.query.filter_by(name=placehtml).first()
        
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
            
        return render_template('zindex.html')


'''
def qty_per_hobby():
    hobby_times = {}

    current_hobby = Hobbyist.query.filter_by(nickname=session['hobbyist']).first()'''


if __name__ == '__main__':
    app.run()