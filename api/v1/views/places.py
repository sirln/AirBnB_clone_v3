#!/usr/bin/python3
'''
Module to create Place class view
To handle all default RESTFul API actions
'''
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    places_list = storage.all('Place').values()
    places = [place.to_dict() for place in places_list
              if place.city_id == city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    user = storage.get('User', data.get('user_id'))
    if not user:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
