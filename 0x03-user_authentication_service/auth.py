#!/usr/bin/env python3
"""
Auth Module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """Hashes a password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user. if email not already exist"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return self._db.add_user(email, hashed_password)
            return new_user
        except NoResultFound as e:
            raise e
        except Exception as e:
            raise e
