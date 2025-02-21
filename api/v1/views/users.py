#!/usr/bin/python3
'''
Module to create User class view
To handle all default RESTFul API actions
'''
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    users_list = storage.all(User).values()
    users = [user.to_dict() for user in users_list]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    if not data:
        return abort(400, {"error": "Not a JSON"})
    if 'email' not in data:
        return abort(400, {"error": "Missing email"})
    if 'password' not in data:
        return abort(400, {"error": "Missing password"})
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        return abort(400, {"error": "Not a JSON"})
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
