#!/usr/bin/python3
"""API view module for state objects"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def all_states():
    """Method that retrieves all state objects"""
    states = storage.all(State)
    state_list = []
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_stateid(state_id):
    """Method that retrieves a state object
    using its state id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_obj(state_id):
    """Method that deletes a state object
    using its state id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state_obj():
    """Method that creates a state object
    using POST"""
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    state_obj = State(**response)
    storage.new(state_obj)
    storage.save()
    return jsonify(state_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
