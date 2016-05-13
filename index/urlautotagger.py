"""
    urlautotagger
    ~~~~~~~~~~~~~

    This module provides a class to determine tags for urls.

    :copyright: (c) 2016 by Peter Jahn
    :license:   BSD (see LICENSE for details)
"""


import re
import urllib.parse


class UrlAutoTagger(object):

    """
    Automatically derive basic tags from a URL.

    Usage: Instantiate with a URL, call process(),
    then call get_tags().
    """

    TAG_PATTERNS = {
        "(www\.)?google\.[a-z]+": "search",
        "(www\.)?duckduckgo\.com": "search",
        "(www\.)?reddit\.com": "reddit",
        "(www\.)?github\.com": "github",
        "(www\.)?serverfault\.com": "serverfault",
        "(www\.)?stackoverflow\.com": "stackoverflow"
    }

    def __init__(self, url):
        super(UrlAutoTagger, self).__init__()
        self.url = url

    def process(self):
        self.derive_tags()
        return self

    def derive_tags(self):
        self._tag = ''
        url_parts = urllib.parse.urlparse(self.url)
        # currently never creates more than one tag, though it could
        for pattern, tag in UrlAutoTagger.TAG_PATTERNS.items():
            if re.match(pattern, url_parts.netloc):
                self._tag = tag

    def get_tags(self):
        return self._tag
