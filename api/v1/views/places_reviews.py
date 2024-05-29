#!/usr/bin/python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity
from flask import abort, request
from flask.json import jsonify


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_place_reviews(place_id):
    """
    Get all the reviews of a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = list()
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    """
    Get a review
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(place_id, amenity_id):
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
def add_review(place_id, amenity_id):
    """
    Add a new amenity
    """
    json = request.get_json(silent=True)
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict()), 200

    new_amenity = Amenity(**json)
    new_amenity.place_id = place_id
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates the value of the place object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    update_json = request.get_json(silent=True)
    if update_json is None:
        abort(400, "Not a JSON")
    for key, val in update_json.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
