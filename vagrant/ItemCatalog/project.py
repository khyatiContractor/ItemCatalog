from flask import Flask, render_template, request, redirect, jsonify, url_for, flash


from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CatalogItem, User

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
APPLICATION_NAME = "catalog catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalogcatalogwithusers.db',connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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
        response = make_response(json.dumps('Current user is already connected.'),
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

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; height: 200px;border-radius: 100px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
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
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

 
# JSON APIs to view catalog Information
@app.route('/catalog/<int:catalog_id>/catalog/JSON')
def catalogcatalogJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(
        catalog_id=catalog_id).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/catalog/<int:catalog_id>/catalog/<int:catalog_menu_id>/JSON')
def catalogItemJSON(catalog_id, catalog_menu_id):
    catalog_Item = session.query(CatalogItem).filter_by(id=catalog_menu_id).one()
    return jsonify(Catalog_Item=catalog_Item.serialize)


@app.route('/catalog/JSON')
def catalogsJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(catalogs=[r.serialize for r in catalogs]) 


# Show all catalogs
@app.route('/')
@app.route('/catalog/')
def showcatalogs():
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    items = session.query(CatalogItem).order_by(CatalogItem.id.desc()).limit(5).all()
    some_list = []
    for item in items:
        #print item.catalog_id
        catalog_name = session.query(Catalog).filter_by(id=item.catalog_id).first()
        some_list.append((item, catalog_name))
        #print catalog_name.name
    return render_template('catalogs.html', catalogs=catalogs,some_list=some_list)

# Create a new catalog


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newcatalog():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newcatalog = Catalog(
            name=request.form['name'], user_id=1)
        session.add(newcatalog)
        flash('New catalog %s Successfully Created' % newcatalog.name)
        session.commit()
        return redirect(url_for('showcatalogs'))
    else:
        return render_template('newCatalog.html')

# Edit a catalog


@app.route('/catalog/<int:catalog_id>/edit/', methods=['GET', 'POST'])
def editcatalog(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedcatalog = session.query(
        Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedcatalog.name = request.form['name']
            #session.editedcatalog.update()
            session.commit()
            flash('catalog Successfully Edited %s' % editedcatalog.name)
            return redirect(url_for('showcatalogs'))
    else:
        return render_template('editcatalog.html', catalog=editedcatalog)


# Delete a catalog
@app.route('/catalog/<int:catalog_id>/delete/', methods=['GET', 'POST'])
def deletecatalog(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalogToDelete = session.query(
        Catalog).filter_by(id=catalog_id).one()
    itemsToDelete = session.query(CatalogItem).filter_by(catalog_id=catalog_id).all()
    
    if request.method == 'POST':
        session.delete(catalogToDelete)
        for item in itemsToDelete:
            session.delete(session.query(
            CatalogItem).filter_by(catalog_id=item.catalog_id).first())
            print item.name
        #itemsToDelete.remove(4)
        flash('%s Successfully Deleted' % catalogToDelete.name)
        session.commit()
        return redirect(url_for('showcatalogs', catalog_id=catalog_id))
    else:
        return render_template('deleteCatalog.html', catalog=catalogToDelete)

# Show a menu items


@app.route('/catalog/<int:catalog_id>/')
@app.route('/catalog/<int:catalog_id>/catalogMenu/')
def showCatalogMenu(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    count =  session.query(CatalogItem).filter_by(catalog_id=catalog_id).count()
    creator = getUserInfo(catalog.user_id)
    print count
    items = session.query(CatalogItem).filter_by(
        catalog_id=catalog_id).all()
    return render_template('menu.html', items=items, catalog=catalog, catalogs=catalogs,count=count)


# Create a new catalog item
@app.route('/catalog/<int:catalog_id>/catalogMenu/new/', methods=['GET', 'POST'])
def newcatalogMenuItem(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'], description=request.form['description'], price=request.form[
                           'price'], catalog_id=catalog_id, user_id=catalog.user_id)
        session.add(newItem)
        session.commit()
        flash('New catalog %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showcatalogs', catalog_id=catalog_id))
    else:
        return render_template('newcatalogmenuitem.html', catalog_id=catalog_id)

# Edit a catalog item

@app.route('/catalog/<int:catalog_id>/catalogMenu/<int:catalog_menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(catalog_id, catalog_menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CatalogItem).filter_by(id=catalog_menu_id).one()
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showCatalogMenu', catalog_id=catalog_id))
    else:
        return render_template('editmenuitem.html', catalog_id=catalog_id, menu_id=catalog_menu_id, item=editedItem)


# Delete a menu item
@app.route('/catalog/<int:catalog_id>/catalogMenu/<int:catalog_menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(catalog_id, catalog_menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    itemToDelete = session.query(CatalogItem).filter_by(id=catalog_menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showCatalogMenu', catalog_id=catalog_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)



# show details of menu item
@app.route('/catalog/catalogMenu/<int:item_id>')
def showDetails(item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()
    return render_template('showDetails.html', details=item.description,item=item)


# Delete a catalog item


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)