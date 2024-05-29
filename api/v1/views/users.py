#!/usr/bin/python3
"""
creates users for blueprint object app_views
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request
from flask.json import jsonify
import hashlib


@app_views.route("/users", strict_slashes=False)
def get_users():
    """
    Get all Users
    """
    users = storage.all("User")
    all_users = list()
    for key, user in users.items():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    """
    Get a user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def add_user():
    """New User
    Add a new user
    """
    json = request.get_json(silent=True)

    if json is None:
        abort(400, "Not a JSON")

    if 'password' not in json:
        abort(400, "Missing password")

    if 'email' not in json:
        abort(400, "Missing email")

    hasher = hashlib.md5()
    hasher.update(json['password'])
    hashed_password = hasher.digest()

    new_user = User(**json)
    new_user.password = hashed_password
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates the value of the user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    update_json = request.get_json(silent=True)
    if update_json is None:
        abort(400, "Not a JSON")
    for key, val in update_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
