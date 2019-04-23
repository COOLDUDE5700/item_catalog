#!/usr/bin/env python

# importing modules
from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os
import random
import requests
import httplib2
import json
import string

app = Flask(__name__)

CLIENT_ID = json.loads(
            open('client_secrets.json', 'r').read())['web']['client_id']

# connecting to a database
engine = create_engine('sqlite:///item_catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
# creating a session
DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create anti-forgery state token
@app.route('/login/')
def login():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state, client_id=CLIENT_ID)


# Connect to Google Sign-in using oAuth method.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


# validaing the access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

# Verifying access token
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

# check of user is already connected
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

# acquiring use info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

# See if the user exists. If it doesn't, make a new one.
    user_id = getuserid(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h2>welcome '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; '
    output += 'border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    return output


def getuserid(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# disconnecting the logged in user
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    if 'username' in login_session:
        gdisconnect()
        del login_session['google_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash("You have been successfully logged out!")
        return redirect(url_for('homepage'))
    else:
        flash("You were not logged in!")
        return redirect(url_for('homepage'))


# creating new user
def create_user(login_session):
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
    )
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# getting user by user info
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).all()
    return user


# homepage
@app.route('/')
@app.route('/catalog/')
def homepage():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(
            Item.id.desc()).limit(5)
    return render_template(
        'HOME.html', categories=categories, items=items)


# adding a category
@app.route('/catalog/addcategory', methods=['GET', 'POST'])
def addCategory():
    if 'user_id' not in login_session:
        flash('kindly login to add new category.')
        return redirect(url_for('login'))
    elif request.method == 'POST':
        newCategory = Category(
            name=request.form['newcategoryname'],
            user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('new category was succesfully added')
        return redirect(url_for('homepage'))
    else:
        return render_template('newcategory.html')


# Editing a category
@app.route('/catalog/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).first()

    if 'user_id' not in login_session:
        flash('You need to be logged in to edit items .')
        return redirect(url_for('login'))
    if category.user_id != login_session['user_id']:
        flash('You are not authorized to edit this Category.')
        return redirect(url_for('homepage'))
    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
        session.add(category)
        session.commit()
        flash('Category is successfully edited!')
        return redirect(url_for('homepage'))
    else:
        return render_template('editcategory.html', category=category)


# deleting a category
@app.route('/catalog/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'user_id' not in login_session:
        flash('you need to login to delete a category!')
        return redirect(url_for('login'))
    if category.user_id != login_session['user_id']:
        flash('You are not authorized delete this Category.')
        return redirect(url_for('homepage'))
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash('Category has been deleted!')
        return redirect(url_for('homepage'))
    else:
        return render_template('deletecategory.html', category=category)


# creating a new item
@app.route("/catalog/item/new/", methods=['GET', 'POST'])
def add_item():
    categories = session.query(Category).all()
    if 'user_id' not in login_session:
        flash("you need to log in to create an item")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        new_item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category'],
            user_id=login_session['user_id']
        )
        session.add(new_item)
        session.commit()
        flash('Item has been succesfully added!')
        return redirect(url_for('homepage'))
    else:
        return render_template('new_item.html', categories=categories)


# vieing a specific item
@app.route('/catalog/item/<int:item_id>/')
def view_item(item_id):
    category = session.query(Category).filter_by(id=Item.category_id).all()
    item = session.query(Item).filter_by(id=item_id).one()
    userinfo = session.query(User).filter_by(id=item.user_id).first()
    return render_template(
        'viewitem.html',
        category=category, item=item, userinfo=userinfo)


# show items in a specific category
@app.route('/catalog/category/<int:category_id>/items/')
def Itemsincategory(category_id):
    categories = session.query(Category).filter_by(id=category_id).first()
    items = session.query(Item).filter_by(category_id=categories.id).all()
    totalitems = session.query(Item).\
        filter_by(category_id=categories.id).count()
    return render_template('item.html', categories=categories, items=items,
                           totalitems=totalitems)


# Edit existing item.
@app.route("/catalog/item/<int:item_id>/edit/", methods=['GET', 'POST'])
def edit_item(item_id):
    if 'user_id' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))

    item = session.query(Item).filter_by(id=item_id).first()
    if item.user_id != login_session['user_id']:
        flash('You were not authorised to edit this item.')
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category_id = request.form['category']
        session.add(item)
        session.commit()
        flash('Item successfully updated!')
        return redirect(url_for('view_item', item_id=item_id))
    else:
        categories = session.query(Category).\
            filter_by(user_id=login_session['user_id']).all()
        return render_template(
            'update_item.html',
            item=item,
            categories=categories
        )


# Delete existing item.
@app.route("/catalog/item/<int:item_id>/delete/", methods=['GET', 'POST'])
def delete_item(item_id):
    if 'user_id' not in login_session:
        flash('you need to login to delete an item.')
        return redirect(url_for('login'))

    item = session.query(Item).filter_by(id=item_id).first()
    if login_session['user_id'] != item.user_id:
        flash("You are not authorised to delete that item.")
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item has been successfully deleted!")
        return redirect(url_for('homepage'))
    else:
        return render_template('deletecategory.html', item=item)


# Returns the JSON of all the items in the catalog.
@app.route('/catalog/json')
def show_catalog_json():

    items = session.query(Item).order_by(Item.id.desc())
    return jsonify(catalog=[i.serialize for i in items])


# Returns the JSON of a particular item in the catalog.
@app.route(
    '/catalog/<int:category_id>/item/<int:item_id>/JSON')
def catalog_item_json(category_id, item_id):
    item = session.query(Item)\
               .filter_by(id=item_id, category_id=category_id).first()
    return jsonify(item=item.serialize)


# Returns the JSON of all the categories in the catalog.
@app.route('/catalog/categories/JSON')
def categories_json():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host="0.0.0.0", port=8079)
