#!/usr/bin/python3
''' Module that handles all default RESTFul API '''

from flask import jsonify, abort, request, Response
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """method that retrieves a list of all places"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_one_place(place_id):
    """method that retrieves a place by id"""
    place = storage.get('Place', place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """method that deletes a place by id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """method to create a new place"""
    place = request.get_json()
    if not place:
        abort(400, 'Not a JSON')
    if 'user_id' not in place:
        abort(400, 'Missing user_id')
    if 'name' not in place:
        abort(400, 'Missing name')
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    user = storage.get('User', request.json['user_id'])
    if user is None:
        abort(404)

    new_place = Place(name=request.json['name'],
                      city_id=city_id, user_id=request.json['user_id'])
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """method to update a place by id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    req = request.get_json()
    req['id'] = place.id
    req['user_id'] = place.user_id
    req['city_id'] = place.city_id
    req['created_at'] = place.created_at
    place.__init__(**data)
    place.save()
    return jsonify(place.to_dict()), 200
