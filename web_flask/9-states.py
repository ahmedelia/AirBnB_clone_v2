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


@app.route("/states/", defaults={"id": None}, strict_slashes=False)
@app.route("/states/<string:id>", strict_slashes=False)
def states_route(id):
    """serve states_list"""
    states = storage.all(State)
    if id is None:
        return render_template("9-states.html", states=states, state=None)
    state = None
    for st in states.values():
        if st.id == id:
            state = st
            break
    return render_template("9-states.html", state=state, states=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
