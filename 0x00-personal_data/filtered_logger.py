#!/usr/bin/env python3

"""
Regex-ing module - Contains function for obfuscating log messages using regex.
"""

import logging
import re
from typing import List


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
