#!/usr/bin/env python3
"""
BasicAuth class
"""
import base64
from flask import request
from binascii import Error as BinasciiError
from typing import Tuple
from models.user import User
from typing import Optional
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class
    """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization header, or None if not
                 found or invalid.
        """
        if authorization_header is None or not isinstance(
            authorization_header, str
        ):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes a Base64 string and returns it as a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded UTF-8 string, or None if invalid.
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode("utf-8")
        except(BinasciiError, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """
        Extracts user credentials from a decoded Base64 Authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64
            Authorization header.

        Returns:
            Tuple(str, str): A tuple containing the user email and password.
        """
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str
        ):
            return None, None

        credentials = decoded_base64_authorization_header.split(":", 1)

        if len(credentials) != 2:
            return None, None

        return tuple(credentials)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> Optional[User]:
        """
        Returns the User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            Optional[User]: The User instance if found, otherwise None.
        """
        if not all(isinstance(i, str) for i in (user_email, user_pwd)):
            return None

        users = User.search({"email": user_email})

        if not users or len(users) != 1:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> Optional[User]:
        """
        Retrieves the User instance for a given request.

        Args:
            request (Request): The request object.

        Returns:
            Optional[User]: The User instance if found, otherwise None.
        """
        if request is None:
            request = request

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
                                  auth_header)

        if not base64_auth_header:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)

        if not decoded_auth_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(
                                decoded_auth_header)

        if not (user_email and user_pwd):
            return None

        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
