#!/usr/bin/env python3
""" Module foe APIs
"""

from flask import Flask, jsonify, request, abort
from auth import Auth
from sqlalchemy.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """
    GET route return json payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    Registers a new user.

    This function handles the POST request to register a new user.
    It takes the email and password from the request form data,
    attempts to register the user using the Auth object, and returns
    a JSON response with the user's email and a success message
    if the user is successfully registered. If the email is
    already registered, it returns a JSON response with an error message
    and a status code of 400.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        if user is not None:
            return jsonify({
                "email": user.email,
                "message": "user created"
            })
    except ValueError:
        return jsonify({
            "message": "email already registered"
            }), 400
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
