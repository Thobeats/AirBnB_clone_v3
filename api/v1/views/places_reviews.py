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


@app_views.route("/reviews/<review_id>", methods=['POST'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete a review
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def add_place_review(place_id):
    """
    Add a new reviews of a place
    """
    json = request.get_json(silent=True)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if json is None:
        abort(400, "Not a JSON")
    if 'user_id' not in json:
        abort(400, 'Missing user_id')
    user = storage.get(User, json['user_id'])
    if user is None:
        abort(404)
    if 'text' not in json:
        abort(400, 'Missing text')
    review = Review(**json)
    review.place_id = place_id
    review.save()
    return jsonify(review), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates the value of the review object
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
