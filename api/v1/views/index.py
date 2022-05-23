#!/usr/bin/python3
"""verifies status on json object"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def objStatus():
    """status of obj app_views returned as JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """endpoint retrieves number of each objects by type"""
    cls_dict = {'amenities': storage.count('Amenity'),
                'cities': storage.count('City'),
                'places': storage.count('Place'),
                'reviews': storage.count('Review'),
                'states': storage.count('State'),
                'users': storage.count('User')}
    return jsonify(cls_dict)
