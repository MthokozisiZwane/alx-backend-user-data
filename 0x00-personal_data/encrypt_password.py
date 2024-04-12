#!/usr/bin/env python3
"""
Encrypting passwords
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the provided password string using bcrypt.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        A salted, hashed password as a byte string.
    """
    # Generates a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates the provided password against the hashed password.

    Args:
        hashed_password: A byte string representing the hashed password.
        password: A string representing the password to be validated.

    Returns:
        True if the provided password matches the hashed password,
        False otherwise.
    """
    # Validates the password against the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
