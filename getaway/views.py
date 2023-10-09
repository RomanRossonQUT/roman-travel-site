from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination 
from . import db

mainbp = Blueprint('main', __name__)

# Define a route for the root URL '/'
@mainbp.route('/')
def index():
    # Retrieve all destinations from the database using SQLAlchemy
    destinations = db.session.query(Destination).all()
    
    # Render the 'index.html' template with the list of destinations
    return render_template('index.html', destinations=destinations)

# Define a route for searching
@mainbp.route('/search')
def search():
    # Check if the 'search' parameter is present in the request and not empty
    if request.args['search'] and request.args['search'] != "":
        query = "%" + request.args['search'] + "%"
        # Perform a search in the database for destinations matching the query
        destinations = db.session.query(Destination).filter(Destination.description.like(f"%{query}%")).all()
        # Render the 'index.html' template with the search results
        return render_template('index.html', destinations=destinations)
    else:
        # Redirect to the main index if the search parameter is missing or empty
        return redirect(url_for('main.index'))
