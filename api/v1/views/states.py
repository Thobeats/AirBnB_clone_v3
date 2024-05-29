#!/usr/bin/python3
"""
creates state blueprint object app_views
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request
from flask.json import jsonify


@app_views.route("/states", strict_slashes=False)
def get_all_states():
    """
    Gets all the state objects
    """
    try:

        all_states = storage.all("State")
        states = list()
        for key, obj in all_states.items():
            states.append(obj.to_dict())
        return states
    except Exception:
        return jsonify([])


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_states(state_id):
    """
    Get a states by its Id
    """
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return state.to_dict()
    except Exception:
        return jsonify([])


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a state record
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def add_state():
    """New State
    Add a new State
    """
    json = request.get_json(silent=True)

    if json is None:
        abort(400, "Not a JSON")

    if 'name' not in json:
        abort(400, "Missing name")

    new_state = State(**json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates the value of the object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    update_json = request.get_json(silent=True)
    if update_json is None:
        abort(400, "Not a JSON")
    for key, val in update_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
