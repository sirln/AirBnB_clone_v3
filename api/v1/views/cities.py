#!/usr/bin/python3
"""API view module for City objects"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Method that retrieves all city objects
    of a state"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_obj(city_id):
    """Method that retrieves a particular city
    object using its id"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        return jsonify(city_obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>/cities', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_obj(city_id):
    """Method that deletes a particular city object
    using its id"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city_obj(state_id):
    """Method that creates a city object in a
    particular state"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    response = request.get_json()
    if "name" not in response:
        abort(400, 'Missing name')
    response['state_id'] = state_id
    city_obj = City(**response)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city_obj(city_id):
    """Method that updates a city object to a
    specific city_id"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        if not request.get_json():
            abort(400, 'Not a JSON')
        response = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in response.items():
            if key not in ignore_keys:
                setattr(city_obj, key, value)
        city_obj.save()
        return jsonify(city_obj.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """Method that handles 404: Not Found"""
    return jsonify({'error': 'Not found'}), 404


def bad_request(error):
    """Method that returns bad requests message
    for illegal requests to API"""
    return jsonify({'error': 'Bad Request'}), 400
