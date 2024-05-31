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
from models.state import State


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
def delete_place(place_id):
    """
    Deletes a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """New Place
    Add a new place
    """
    json = request.get_json(silent=True)
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if json is None:
        abort(400, "Not a JSON")

    if 'user_id' not in json:
        abort(400, "Missing user_id")

    user = storage.get(User, json['user_id'])

    if user is None:
        abort(404)

    if 'name' not in json:
        abort(400, "Missing name")

    new_place = Place(**json)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates the value of the place object
    """
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


@app_views.route("/places_search", methods=['POST'],
                 strict_slashes=False)
def search_places():
    """Search Places
    Keyword arguments:
    states: list of State ids
    cities: list of City ids
    amenities: list of Amenity ids
    Return: valid JSON
    """
    all_places = []
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    if len(json) > 0:
        placeQuery = storage.all(Place)
        if 'states' in json and len(json['states']) > 0:
            stateQuery = storage.all(State)
            cities = []
            for state in stateQuery.values():
                if state.id in json['states']:
                    for state_city in state.cities:
                        cities.append(state_city.id)
            citiesStr = "', '".join(cities)
            placeQuery = storage.queryfilter(Place, "city_id in ('{}')"
                                             .format(citiesStr))

        if 'cities' in json and len(json['cities']) > 0:
            cityQuery = storage.all(City)
            cities = []
            for city in cityQuery.values():
                if city.id in json['cities']:
                    cities.append(city.id)
            citiesStr = "', '".join(cities)
            placeQuery = storage.queryfilter(Place, "city_id in ('{}')"
                                             .format(citiesStr))

        if (('states' in json and len(json['states']) > 0) and
                ('cities' in json and len(json['cities']) > 0)):
            stateQuery = storage.all(State)
            cities = []
            for state in stateQuery.values():
                if state.id in json['states']:
                    for state_city in state.cities:
                        cities.append(state_city.id)
            cityQuery = storage.all(City)
            for city in cityQuery.values():
                if city.id in json['cities']:
                    cities.append(city.id)

            citiesStr = "', '".join(cities)
            placeQuery = storage.queryfilter(Place, "city_id in ('{}')"
                                             .format(citiesStr))

        if 'amenities' in json and len(json['amenities']) > 0:
            places = []
            for place in placeQuery.values():
                for amenity in place.amenities:
                    if (amenity.id in json['amenities'] and
                            amenity.id not in places):
                        if 'amenities' in place.__dict__:
                            del place.__dict__['amenities']
                        places.append(place.to_dict())
            return jsonify(places)
        else:
            places = []
            for place in placeQuery:
                print(place)
                places.append(place.to_dict())
            return jsonify(places)
    else:
        placeQuery = storage.all(Place)
        places = []
        for place in placeQuery.values():
            places.append(place.to_dict())
        return jsonify(places)
