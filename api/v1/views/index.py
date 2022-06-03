#!/usr/bin/python3
"""verifies status on json object"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/status', strict_slashes=False)
def objStatus():
    """status of obj app_views returned as JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def number_objects():
    """endpoint retrieves number of each objects by type"""
    cls_dict = {'amenities': storage.count(Amenity),
                'cities': storage.count(City),
                'places': storage.count(Place),
                'reviews': storage.count(Review),
                'states': storage.count(State),
                'users': storage.count(User)}
    return jsonify(cls_dict)
