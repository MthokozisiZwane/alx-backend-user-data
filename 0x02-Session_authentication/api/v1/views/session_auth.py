#!/usr/bin/env python3
"""
New view for authentication
"""
from api.v1.views import app_views
from os import getenv
from flask import Blueprint, request, abort, jsonify
# from api.v1.app import auth
from models.user import User

session_auth = Blueprint('session_auth', __name__, url_prefix='/auth_session')


@session_auth.route('/login', methods=['POST', 'GET'], strict_slashes=False)
def login():
    """
    Log in route for session authentication.

    Accepts POST requests with email and password parameters.
    Returns a user object and sets a session cookie upon successful login.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400
        if not password:
            return jsonify({"error": "password missing"}), 400

        user = User.search({'email': email})

        if not user:
            return jsonify({"error": "no user found for this email"}), 404
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        session_id = auth.create_session(user.id)
        user_dict = user.to_json()

        response = jsonify(user_dict)
        response.set_cookie(auth.SESSION_NAME, session_id)

        return response, 200

    else:
        abort(405)


from api.v1.app import auth


@app_views.route('/api/v1/auth_session/logout',
           methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logout route.
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
