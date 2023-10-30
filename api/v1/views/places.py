#!/usr/bin/python3
'''
Module to create Place class view
To handle all default RESTFul API actions
'''
from flask import Flask, jsonify, abort, request
from models import storage, City, User, Place


@app.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    places_list = storage.all('Place').values()
    places = [place.to_dict() for place in places_list
              if place.city_id == city_id]
    return jsonify(places)


@app.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/cities/<city_id>/places', methods=['POST'])
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
    user = storage.get('User', data['user_id'])
    if not user:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app.route('/api/v1/places/<place_id>', methods=['PUT'])
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
    place.save()
    return jsonify(place.to_dict()), 200
