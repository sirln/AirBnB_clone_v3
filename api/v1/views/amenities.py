#!/usr/bin/python3
'''
Module to create Amenity class view
To handle all default RESTFul API actions
'''
from models import storage, Amenity
from flask import Flask, jsonify, abort, request


@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    amenities_list = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities_list]
    return jsonify(amenities)


@app.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
