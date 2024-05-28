#!/usr/bin/python3
"""
place related api endpoints
"""

from api.v1.views import app_views
from flask import abort, request
from flask.json import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city(city_id=None):
    """
    returns a list of all places of a city
    """
    all_city = storage.all(City)
    res = []
    if all_city is not {} and city_id is not None:
        for city in all_city.values():
            if city.id == city_id:
                for place in city.places:
                    res.append(place.to_dict())
                return jsonify(res)

    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_places(place_id=None):
    """
    retrieves place object based on place_id
    """
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())

    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    """
    deletes a place object
    """
    place = storage.get(Place, place_id)
    if place is not None:
        place.delete()
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def make_place(city_id=None):
    """
    creates a place object
    """
    json = request.get_json(silent=True)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if json is None:
        abort(400, 'Not a JSON')

    if 'name' not in json:
        abort(400, 'Missing name')

    if 'user_id' not in json:
        abort(400, 'Missing user_id')

    if storage.get(User, json['user_id']) is None:
        abort(404)

    place = Place(**json)
    place.city_id = city_id
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """
    updates a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    json = request.get_json(silent=True)

    if json is None:
        abort(400, 'Not a JSON')

    for key, value in json.items():
        if key != 'updated_at' and key != 'created_at' and key != 'id' \
           and key != 'user_id' and key != 'city_id':
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200
