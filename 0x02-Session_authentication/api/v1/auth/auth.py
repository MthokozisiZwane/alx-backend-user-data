#!/usr/bin/env python3
"""
The class to manage the API authentication
"""

import os
from typing import List, TypeVar
from flask import request

"""
The Auth class

"""


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths where authentication
            is not required.

        Returns:
            bool: True if authenticatiion is required, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Method to retrieve the authorization header from the request.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            str: The authorization header value.
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user based on the request.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            TypeVar('User'): The current user object.
        """
        return None

    def session_cookie(self, request=None):
        """
        Return the value of the session cookie from the request.
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
