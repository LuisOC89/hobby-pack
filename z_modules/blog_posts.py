from flask import request, render_template, redirect

from app import db

from models import Blog, Bloganswer, Hobbyist
from utils import filling, now1, logged_in_hobbyist

class zPosts(object):
    
    def listing_blogs(self):
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

    def adding_post(self):
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
                elif len(post_title) > 30:
                    error = "lentitle"
                elif len(post_body) > 120:
                    error = "lenbody"
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
                elif len(post_title) > 30:
                    error = "lentitle"
                elif len(post_body) > 120:
                    error = "lenbody"
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

    
