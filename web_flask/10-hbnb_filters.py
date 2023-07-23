#!/usr/bin/python3
"""Flask web server"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def poped(err):
    """called after each request finshied"""
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """serve hbnb_filters"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity)
    state_cities = {}
    for state in states:
        state_cities[state] = state.cities
    return render_template("10-hbnb_filters.html", states=state_cities, amenities=amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
