#!/usr/bin/python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, request
from flask.json import jsonify


@app_views.route("/amenities", strict_slashes=False)
def get_amenities(state_id):
    """
    Get all ammenities
    """
    amenities = storage.all(Amenity)
    all_amenities = list()
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    return all_amenities


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    """
    Get an amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return amenity.to_dict()


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", methods=['POST'],
                 strict_slashes=False)
def add_amenity(amenity_id):
    """New Amenity
    Add a new amenity
    """
    json = request.get_json(silent=True)

    if json is None:
        abort(404, "Not a JSON")

    if 'name' not in json:
        abort(404, "Missing name")

    new_amenity = Amenity(**json)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates the value of the object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    update_json = request.get_json(silent=True)
    if update_json is None:
        abort(404, "Not a JSON")
    for key, val in update_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
