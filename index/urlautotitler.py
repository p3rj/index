"""
    urlautotitler
    ~~~~~~~~~~~~~

    This module provides a class to determine titles for urls.

    :copyright: (c) 2016 by Peter Jahn
    :license:   BSD (see LICENSE for details)
"""


import urllib.parse


class UrlAutoTitler(object):

    """
    Instances of this class can be used to generate a title for a URL.

    The class follows the stepwise pattern.  So to get a title string
    for a given url:

        uat = UrlAutoTitler(url)
        uat.process()
        title = uat.get_title()

    Currently the title is simply taken from the url's host name
    portion.  The class could be extended to try to fetch the actual
    title from the target address in the future.
    """

    def __init__(self, url):
        """Create an instance referencing the given url."""
        super(UrlAutoTitler, self).__init__()
        self._url = str(url)

    def process(self):
        """Determine the title from the stored url."""
        # TODO We could make an attempt to retrieve the title
        self._derive_title()
        return self

    def get_title(self):
        """Return the determined title."""
        return self._title

    def _derive_title(self):
        """Parse the stored url."""
        url_parts = urllib.parse.urlparse(self._url)
        self._title = url_parts.netloc
        # TODO If that value's empty, generate something (random, UUID, etc)
