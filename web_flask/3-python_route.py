#!/usr/bin/python3
"""Flask web server"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """Entry point of app"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """hbnb page"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    return f"C {escape(text.replace('_', ' '))}"


@app.route("/python/", defaults={"text": "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def py(text):
    return f"Python {escape(text.replace('_', ' '))}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
