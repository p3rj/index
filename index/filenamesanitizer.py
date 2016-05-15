"""
    filenamesanitizer
    ~~~~~~~~~~~~~~~~~

    This module provides a class to remove illegal characters from filenames.

    :copyright: (c) 2016 by Peter Jahn
    :license:   BSD (see LICENSE for details)
"""


class FilenameSanitizer:

    """Return copy of string with characters illegal in filename removed."""

    SPECIALS = (' ', '-', '_', '.')

    def __init__(self, filename):
        self.sanitized_name = str(filename).translate(self)

    def __getitem__(self, c):
        """Return ch if that seems acceptable in a file name, or None.

        Used by the String.translate call.
        """
        ch = chr(c)
        if ch.isalnum() or ch in FilenameSanitizer.SPECIALS:
            return ch
        return None

    def __call__(self):
        return self.sanitized_name
