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
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenities(place_id, amenity_id):
    """
    Deletes an amenity
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'],
                 strict_slashes=False)
def add_amenity_to_place(place_id, amenity_id):
    """
    Add a new amenity
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    return jsonify(amenity.to_dict()), 201
