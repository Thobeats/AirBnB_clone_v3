#!/usr/bin/python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, request
from flask.json import jsonify


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_city_places(city_id):
    """
    Get all the places of a city
    """
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        places = list()
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    except Exception:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id):
    """
    Get a place
    """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        return jsonify(place.to_dict())
    except Exception:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(user_id):
    """
    Deletes a place
    """
    try:
        place = storage.get(Place, user_id)
        if place is None:
            abort(404)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """New Place
    Add a new place
    """
    try:
        json = request.get_json(silent=True)
        city = storage.get(City, city_id)

        if city is None:
            abort(404)

        if json is None:
            abort(400, "Not a JSON")

        if 'user_id' not in json:
            abort(404, "Missing user_id")

        user = storage.get(User, json['user_id'])

        if user is None:
            abort(404)

        if 'name' not in json:
            abort(400, "Missing name")

        new_place = Place(**json)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates the value of the place object
    """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        update_json = request.get_json(silent=True)
        if update_json is None:
            abort(400, "Not a JSON")
        for key, val in update_json.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, val)
        place.save()
        return jsonify(place.to_dict()), 200
    except Exception:
        abort(404)
