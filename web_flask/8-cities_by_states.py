#!/usr/bin/python3
"""Flask web server"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def poped(err):
    """called after each request finshied"""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """server cities_by_states"""
    states = storage.all(State).values()
    state_cities = {}
    for state in states:
        state_cities[state] = state.cities

    return render_template("8-cities_by_states.html", states=state_cities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
