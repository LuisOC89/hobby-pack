from flask import request, render_template

from models import Hobbyist, Hobby, Place, Encounter, Blog, Bloganswer

class zHome(object):
    def index(self):    
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
