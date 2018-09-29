# hobby-pack
An app that allows people with the same hobbies that live close by to create events in public places where they will meet.

## Overview
It allows a person to sign up, log in, have a profile, add a new hobby, add a new public place related to an existing hobby, add a hobby from other user to their hobbies, add an existing public place to their places, post comments to a blog, chat with other people registered in the app and finally create an event were the user invites other people, and after the event, the creator of the event takes attendance.

## The Reason
This project was motivated by the need of a person that moves to a new city and doesnt know other people in the same city with the same hobbies, so this person feels alone. With this app, this person will meet new people and hopefully make new friends.  

## Features
* User signup: A person is able to create an account in the system. There is limited access to not logged-in users.
* User login: Users are able to login. There is limited access to not logged-in users.
* User profile: A person has a profile with some of his/her data (city, state, zipcode), what hobbies this person likes where this person practices these hobbies (public places) and what posts this user has in the main blog.
* Chat: A logged-in user is able to create a chat with one person or with a group of people he chooses at the moment of creating the chat. The name of the chat is either the name of the other person (one-to-one user) or the name assigned to the group of people (one-to-many users) at the moment of creation.
* Hobbies visualization and addition: A logged-in user is able to add a hobby to her/his hobbies, either by creating a new hobby or by adding a hobby from other user if the hobby already exists. All users are able to see all the hobbies from other users and where they practice these hobbies.
* Places visualization and addition: A logged-in user is able to add a public place related to one or several of her/his to her/his places, either by creating a new place or by adding a place from other user if the place already exists. All users are able to see all the places from other users and what hobbies they practice on these places.
* Blog: A logged-in user is able to post a comment on the main Blog page. Other users and creator user is able to answer this initial or main post.

## Technologies
* Python 
* SQLAlchemy
* Bootstrap
* Flask, Jinja templates
* Javascript
* JSON & APIs (oh yeah! :))
* DOCKER
* POSTGRESQL

## To run the app

# To run directly:
Go to Project directory main folder
In the file app.py, uncomment app.config related to running directly
Then, do: python main.py
Go to localhost:5000

# To run with DOCKER:

# Two ways to run with local database in POSTGRES:

# 1. WITH DOCKER BUILD and DOCKER RUN:
1.1 CHANGE "HOST" in connection configuration in file app.py from "localhost" to "host.docker.internal" 
1.1 Do: docker build -t humbledore/hobby_pack . 
If you want to use Dockerfile.dev as your Dockerfile, then do:
docker build -f Dockerfile.dev -t humbledore/hobby_pack . 
--no-cache included in previous command if you want it to rebuild image from zero
1.2 Do: docker run -p 3001:5000 -v "$(pwd):/app" humbledore/hobby_pack
Go to localhost:3001

# 2. WITH DOCKER-COMPOSE BUILD AND UP:
2.0 FIX VOLUMES IN docker-compose.yml file (in case of running in other container with db)
2.1 Do: docker-compose build
--no-cache included in previous command if you want it to rebuild image from zero
2.2 Do: docker-compose up
Go to localhost:4001

# 3.0 Or just do: docker-compose up --build

# --reload declared here so it reloads everytime a change is made (it matters in docker too)

## What I had to Learn
I had to learn many-to-many relationship in flask-SQLAlchemy. To improve the UI and UX I needed to learn more about CSS and Bootstrap, besides I wanted to include some APIs in my project (youtube, google, wikipedia). Related to APIs I was at 0, so I had to learn Javascript and APIs :) (still work in progress).  

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
