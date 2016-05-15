"""
    stopwords
    ~~~~~~~~~

    This module provides a class to read and manage stopwords.

    :copyright: (c) 2016 by Peter Jahn
    :license:   BSD (see LICENSE for details)
"""


class Stopwords(object):

    """Container for words too common to search for."""

    def __init__(self, fn='stopwords.txt'):
        super(Stopwords, self).__init__()
        self.filename = fn
        self.stopwords = set()
        self._load()

    def _load(self):
        with open(self.filename) as f:
            line = f.readline()
            while line:
                word = line.rstrip()
                if word: self.stopwords.add(word)
                line = f.readline()

    def __contains__(self, word):
        return word in self.stopwords
