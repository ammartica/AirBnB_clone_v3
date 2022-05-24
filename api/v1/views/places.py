#!/usr/bin/python3
""" Handles all default RESTFul API """
from flask import request, abort, jsonify
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from api.v1.app import *


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """method retieves all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def one_place(place_id):
    """method that retrieves a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """method that deletes a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """method to create a new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request = request.get_json()
    if not request:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get(User, request.get('user_id'))
    if not user:
        abort(404)
    place = Place(city_id=city.id, user_id=user.id, name=data.get('name'))
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """method to update a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request = request.get_json()
    if not request:
        abort(400, 'Not a JSON')
    request['id'] = place.id
    request['user_id'] = place.user_id
    request['city_id'] = place.city_id
    request['created_at'] = place.created_at
    place.__init__(**request)
    place.save()
    return jsonify(place.to_dict()), 200
