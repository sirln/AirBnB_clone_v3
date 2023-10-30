#!/usr/bin/python3
'''
Module to create User class view
To handle all default RESTFul API actions
'''
from flask import Flask, jsonify, abort, request
from models import storage, User


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users_list = storage.all('User').values()
    users = [user.to_dict() for user in users_list]
    return jsonify(users)


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
