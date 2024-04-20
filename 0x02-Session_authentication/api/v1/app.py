#!/usr/bin/env python3
"""
Main module for the API.

This module initializes the Flask application and sets up
routes, error handlers,and authentication mechanisms
"""
import os
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
# Enable Cross-Origin Resource Sharing (CORS) for all routes in the API
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth_type = os.getenv("AUTH_TYPE")
if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> None:
    """
    Before request method
    """
    if auth is None:
        return None

    excluded_paths = [
        '/api/v1/status',
        '/api/v1/status/',
        '/api/v1/unauthorized',
        '/api/v1/forbidden'
    ]

    if request.path not in excluded_paths:
        if auth.authorization_header(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)


@app.route('/users/me', methods=['GET'])
def get_current_user():
    """Get the current authenticated user"""
    user = current_user(request)
    if user:
        return jsonify(user.to_json()), 200
    else:
        abort(401)


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
