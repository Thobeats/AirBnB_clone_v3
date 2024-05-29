#!/usr/bin/python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, request
from flask.json import jsonify


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_state_cities(state_id):
    """
    Get all the cities in state
    """
    state = storage.get(State, state_id)
    cities = list()
    if state is None:
        abort(404)
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    """
    Get a single city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a city record
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def add_state_city(state_id):
    """New City
    Add a new city
    """
    json = request.get_json(silent=True)
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if json is None:
        abort(400, "Not a JSON")

    if 'name' not in json:
        abort(400, "Missing name")

    new_city = City(**json)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Updates the value of the object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    update_json = request.get_json(silent=True)
    if update_json is None:
        abort(400, "Not a JSON")
    for key, val in update_json.items():
        if key not in ['id', 'created_at', 'state_id', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
