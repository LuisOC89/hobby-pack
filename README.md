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

## What I had to Learn
I had to learn many-to-many relationship in flask-SQLAlchemy. To improve the UI and UX I needed to learn more about CSS and Bootstrap, besides I wanted to include some APIs in my project (youtube, google, wikipedia). Related to APIs I was at 0, so I had to learn Javascript and APIs :) (still work in progress).  
