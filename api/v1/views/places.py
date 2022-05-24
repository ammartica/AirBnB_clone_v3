#!/usr/bin/python3
""" Handles all default RESTFul API """
from flask import request, abort, jsonify
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from api.v1.app import *


def validate_city(city_id):
    """ validate if query has id to reference """
    try:
        valid = storage.get(City, city_id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def validate_place(place_id):
    """ validate if place obj exists """
    try:
        valid = storage.get(Place, place_id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ get all places """
    if (city_id is not None):
        city = validate_city(city_id)
    places_all = []
    for place in city.places():
        places_all.append(place.to_dict())
    return jsonify(places_all)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_place(place_id):
    """gets one specified place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete place request """
    place = validate_place(place_id)
    storage.delete(place)
    storage.save()
    response = {}
    return jsonify(response), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create place """
    if (city_id is not None):
        city = validate_city(city_id)
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_json:
        abort(400, 'Missing user_id')
    if 'name' not in request_json:
        abort(400, 'Missing name')
    place = storage.get(City, city_id)
    if place is None:
        abort(404)

    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)

    new_place = Place(name=request.json['name'],
                      city_id=city_id, user_id=request.json['user_id'])
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place):
    """ update place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if (key not in ('id', 'created_at', 'updated_at', 'city_id')):
            setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
