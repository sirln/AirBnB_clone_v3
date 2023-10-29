#!/usr/bin/python3
'''
API landing page view module
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def returnstuff():
    '''return stuff'''
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def statistics():
    '''Method that returns the statistics
    about various stuff in JSON format'''
    tables = {'amenities': Amenity, 'cities': City,
              'places': Place, 'reviews': Review,
              'states': State, 'users': User}
    objects = {}
    for key, value in tables.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
