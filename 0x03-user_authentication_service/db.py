#!/usr/bin/env python3
"""
DB Module
"""

from sqlalchemy.orm import sessionmaker
from user import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


class DB:
    """DB class responsible for database operations."""

    def __init__(self):
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.

        Args:
            email (str): Email of the user.
            hashed_password (str): Hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on given criteria.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The found User object.

        Raises:
            ValueError: If no user is found or multiple users are found.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise ValueError("User not found")
        except MultipleResultsFound:
            raise ValueError("Multiple users found")
