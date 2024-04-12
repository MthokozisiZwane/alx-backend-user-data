#!/usr/bin/env python3

"""
Regex-ing module - Contains function for obfuscating log messages using regex.
"""

import logging
import re
from typing import List
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates fields in a log message.

    Args:
        fields: A list of strings representing fields to obfuscate.
        redaction: A string representing the value by which the field
                   will be obfuscated.
        message: A string representing the log line.
        separator: A string representing the character separating all
                    fields in the log line.

    Returns:
        The obfuscated log message.
    """
    pattern = '|'.join(map(re.escape, fields))
    return re.sub(r'({0})=([^{1}]+)'.format(pattern, separator), r'\1={0}'
                  .format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class - Formats log records and redacts
    specified fields.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter with specified fields to redact.

        Args:
            fields: A list of strings representing fields to redact.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record and redact specified fields.

        Args:
            record: The log record to format.

        Returns:
            The formatted log message with specified fields redacted.
        """
        for field in self.fields:
            record.msg = filter_datum([field], self.REDACTION, record.msg,
                                      self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("email", "ssn", "name", "password", "phone")


def get_logger() -> logging.Logger:
    """
    Return a configured logging.Logger object.

    Returns:
        A configured logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database.

    Returns:
        A connector to the MySQL database.
    """
    # Getting database credentials from environment variables
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME", "my_db")

    # Connecting to the database
    try:
        db = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        raise


def main() -> None:
    """
    Retrieve data from the database and log each row with filtering.
    """
    # Gets the logger configured in Task 2
    logger = get_logger()

    try:
        # connection to the database
        db = get_db()
        cursor = db.cursor()

        # Retrieves all rows from the users table
        cursor.execute("SELECT * FROM users")

        # Log each row with information filtered
        for row in cursor.fetchall():
            # Construcst the log message with sensitive information filtered
            filtered_row = '; '.join([
                f"{key}={filter_datum(PII_FIELDS, '***', str(value), ';')}"
                for key, value in zip(cursor.column_names, row)
            ])
            logger.info(filtered_row)

    except Exception as e:
        logger.error(
            f"Error retrieving data from database: {e}"
        )
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
