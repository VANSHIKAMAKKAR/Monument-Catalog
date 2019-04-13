from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Places, PopularLocations, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "INDIAN HERITAGE APPLICATION"

engine = create_engine('sqlite:///itemcatalogappwithlogin.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/places/')
def showPlaces():
    place = session.query(Places).order_by(asc(Places.name))
    return render_template('place.html', p=place)


@app.route('/newplaces/')
def shownewPlaces():
    place = session.query(Places).order_by(asc(Places.name))
    return render_template('newPlace.html', p=place)


@app.route('/monu/<int:place_id>/')
def showMonuments(place_id):
    place = session.query(Places).filter_by(id=place_id).one()
    monu = session.query(PopularLocations).filter_by(places_id=place_id).all()
    return render_template('monuments.html', p=place, Monu=monu)


@app.route('/publicmonu/<int:place_id>/')
def showPublicMonuments(place_id):
    place = session.query(Places).filter_by(id=place_id).one()
    monu = session.query(PopularLocations).filter_by(places_id=place_id).all()
    return render_template('publicmonuments.html', p=place, Monu=monu)


@app.route('/places/new/', methods=['GET', 'POST'])
def newPlace():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newPlace = Places(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newPlace)
        flash('New Place %s Successfully Created' % newPlace.name)
        session.commit()
        return redirect(url_for('shownewPlaces'))
    else:
        return render_template('addplace.html')


@app.route('/places/<int:place_id>/delete/',
           methods=['GET', 'POST'])
def deletePlace(place_id):
    placeToDelete = session.query(
        Places).filter_by(id=place_id).one()
    Placemon = session.query(PopularLocations).filter_by(
        places_id=place_id).all()
    if 'username' not in login_session:
        return redirect('/login')
    if placeToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to delete this Place. \
        Please create your own Place in order to delete.');\
        setTimeout(function() \
        {window.location.href = '/newplaces/';}, 1000);}\
        </script><body onload='myFunction()'>"
    if request.method == 'POST':
        for i in Placemon:
            session.delete(i)
            session.commit()
        session.delete(placeToDelete)
        session.commit()
        return redirect(url_for('shownewPlaces', places_id=place_id))
    else:
        return render_template('deleteplace.html', place=placeToDelete)


@app.route('/places/<int:place_id>/edit', methods=['GET', 'POST'])
def editPlace(place_id):
    editedPlace = session.query(Places).filter_by(id=place_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedPlace.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to edit this Place. \
        Please create your own Place in order to edit.');\
        setTimeout(function() \
        {window.location.href = '/newplaces/';}, 1000);}\
        </script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedPlace.name = request.form['name']
            return redirect(url_for('shownewPlaces'))
    else:
        return render_template('editplace.html', place=editedPlace)


@app.route('/monu/<int:place_id>/new', methods=['GET', 'POST'])
def addnewmonu(place_id):
    monu = session.query(PopularLocations).filter_by(
        places_id=place_id).all()
    place = session.query(Places).filter_by(
        id=place_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if place.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to add Monument.');\
        setTimeout(function()\
        {window.location.href = '/newplaces';}, 1000);}</script>\
        <body onload='myFunction()'>"
    if request.method == 'POST':
        newmonu = PopularLocations(name=request.form['name'],
                                   description=request.form['description'],
                                   year=request.form['year'],
                                   founder=request.form['founder'],
                                   places_id=place_id)
        session.add(newmonu)
        session.commit()
        return redirect(url_for('showPublicMonuments',
                                place_id=place_id))
    else:
        return render_template('addnewmonu.html',
                               place_id=place_id, monu=monu,
                               place=place)


@app.route('/monu/<int:place_id><int:places_id>/edit',
           methods=['GET', 'POST'])
def editMon(place_id, places_id):
    editmon = session.query(PopularLocations).filter_by(id=places_id).one()
    Place = session.query(Places).filter_by(id=place_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if Place.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to edit this Monument. \
        Please create your own Monument in order to edit.');\
        setTimeout(function()\
        {window.location.href = '/newPlace/';}, 1000);}</script>\
        <body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editmon.name = request.form['name']
        if request.form['description']:
            editmon.description = request.form['description']
        if request.form['year']:
            editmon.year = request.form['year']
        if request.form['founder']:
            editmon.starring = request.form['founder']
        session.add(editmon)
        session.commit()
        return redirect(url_for('showPublicMonuments',
                                place_id=place_id))
    else:
        return render_template('editmon.html',
                               place=Place, editmon=editmon)


@app.route('/monu/<int:place_id>/<int:places_id>/delete',
           methods=['GET', 'POST'])
def deleteMonu(place_id, places_id):
    Place = session.query(Places).filter_by(id=place_id).one()
    monuToDelete = session.query(PopularLocations).filter_by(
        id=places_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if Place.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorized to delete this Monument. Please create \
        your own Monument in order to delete.');\
        setTimeout(function() \
        {window.location.href = '/newmovies/';}, 1000);}</script><body \
        onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(monuToDelete)
        session.commit()
        return redirect(url_for('showPublicMonuments',
                                place_id=place_id))
    else:
        return render_template('deletemonu.html',
                               monu=monuToDelete, place=Place)


@app.route('/places/<int:place_id>/loc/JSON')
def placelocJSON(place_id):
    place = session.query(Places).filter_by(id=place_id).all()
    loc = session.query(PopularLocations).filter_by(
        places_id=place_id).all()
    return jsonify(loc=[i.serialize for i in loc])


@app.route('/places/<int:place_id>/<int:places_id>/JSON')
def locaJSON(place_id, places_id):
    loc = session.query(PopularLocations).filter_by(id=places_id).all()
    return jsonify(Loc=[i.serialize for i in loc])


@app.route('/places/JSON')
def placesJSON():
    place = session.query(Places).all()
    return jsonify(Place=[i.serialize for i in place])


# Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


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

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;\
     height: 300px;border-radius: 150px;-webkit-border-radius:\
      150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        place = session.query(Places).order_by(asc(Places.name))
        return render_template('place.html', p=place)
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        place = session.query(Places).order_by(asc(Places.name))
        return render_template('place.html', p=place)
    else:
        place = session.query(Places).order_by(asc(Places.name))
        return render_template('place.html', p=place)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
