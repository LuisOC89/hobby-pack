from flask import request, render_template, redirect

from app import db

from models import Blog, Bloganswer
from utils import filling, now1, logged_in_hobbyist

class zPosts(object):
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
