#!/usr/bin/python3
""" Handles all default RESTFul API """
from flask import request, abort, jsonify
from api.v1.app import *
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


def validate_state(id):
    """ validate if query has id to reference """
    try:
        valid = storage.get(State, id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def validate_city(id):
    """ validate if city obj exists """
    try:
        valid = storage.get(City, id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def get_all_cities(state_id):
    """ get all cities """
    if (state_id is not None):
        state = validate_state(state_id)
    cities = storage.all(City)
    cities_all = []
    for city in cities.values():
        cities_all.append(city.to_dict())
    return jsonify(cities_all)


def delete_city(city_id):
    """ delete city request """
    city = validate_city(city_id)
    storage.delete(city)
    storage.save()
    response = {}
    return jsonify(response)


def create_city(request):
    """ create city """
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    try:
        name_city = request_json['name']
    except Exception:
        abort(400, "Missing name")
    city = City(name=name_city, state_id=state.id)
    storage.new()
    storage.save()
    return jsonify(city.to_dict())


def update_city(city_id, request):
    """ update city """
    city = validate_city(city_id)
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if (key not in ('id', 'created_at', 'updated_at', 'state_id')):
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 defaults={'state_id': None}, strict_slashes=False)
@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def cities(state_or_city_id):
    """ Switch to select function """
    if (request.method == "GET"):
        return get_all_cities(state_or_city_id)
    elif request.method == "DELETE":
        return delete_city(state_or_city_id)
    elif request.method == "POST":
        return create_city(request), 201
    elif request.method == 'PUT':
        return update_city(state_or_city_id, request), 200
