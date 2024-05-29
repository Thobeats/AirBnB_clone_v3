#!/usr/bin/python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from flask import abort, request
from flask.json import jsonify


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def get_place_amenities(place_id):
    """
    Get all the amenities of a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = list()
    for amenities in place.amenities:
        amenities.append(amenities.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenities_id>", strict_slashes=False)
def get_new_amenity(amenities_id):
    """
    Get a amenities
    """
    amenities = storage.get(amenities, amenities_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route("/amenities/<amenities_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenities(amenities_id):
    """
    Deletes a amenities
    """
    amenities = storage.get(amenities, amenities_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities", methods=['POST'],
                 strict_slashes=False)
def add_amenities(place_id):
    """New amenities
    Add a new amenities
    """
    json = request.get_json(silent=True)
    place = storage.get(City, place_id)

    if place is None:
        abort(404)

    if json is None:
        abort(404, "Not a JSON")

    if 'user_id' not in json:
        abort(404, "Missing user_id")

    user = storage.get(User, json['user_id'])

    if user is None:
        abort(404)

    if 'text' not in json:
        abort(404, "Missing text")

    new_amenities = Amenity(**json)
    new_amenities.save()
    return jsonify(new_amenities.to_dict()), 201


@app_views.route("/amenities/<amenities_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenities_id):
    """
    Updates the value of the place object
    """
    amenities = storage.get(amenities, amenities_id)
    if amenities is None:
        abort(404)
    update_json = request.get_json(silent=True)
    if update_json is None:
        abort(404, "Not a JSON")
    for key, val in update_json.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(amenities, key, val)
    amenities.save()
    return jsonify(amenities.to_dict()), 200
