#!/usr/bin/env python3
""" Module foe APIs
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    """
    GET route return json payload
    """
    return jsonify({"message": "Bienvenue"})


f __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
