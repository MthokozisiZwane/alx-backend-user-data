#!/usr/bin/env python3

"""
Regex-ing module - Contains function for obfuscating log messages using regex.
"""

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
