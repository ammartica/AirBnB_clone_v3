#!/usr/bin/python3
''' Module that handles all default RESTFul API '''

from flask import request, abort, jsonify
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """method that retrieves a list of all cities"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_one_city(city_id):
    """method that retrieves a city by id"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """method that deletes a city by id"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    else:
        city.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """method to create a new city"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    city = request.get_json()
    if city is None:
        abort(400, 'Not a JSON')
    if 'name' not in city:
        abort(400, 'Missing name')
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """method to update a city by id"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    req = request.get_json()
    req['id'] = city.id
    req['created_at'] = city.created_at
    req['state_id'] = city.state_id
    city.__init__(**req)
    city.save()
    return (jsonify(city.to_dict()), 200)
