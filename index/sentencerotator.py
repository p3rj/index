"""
    sentencerotator
    ~~~~~~~~~~~~~~~

    This module provides a class to generate rotations of a sentence.

    :copyright: (c) 2016 by Peter Jahn
    :license:   BSD (see LICENSE for details)
"""


import collections
import re


class SentenceRotator(object):
    """Instances implement a mechanism to create rotations of a string.

    This is used to build Key Word in Context indexes (see
    https://en.wikipedia.org/wiki/Key_Word_in_Context).
    """

    def __init__(self, sentence, stopwords=[]):
        super(SentenceRotator, self).__init__()
        self.sentence = sentence
        self.stopwords = stopwords

    def split_sentence(self):
        """Return sentence split into list of words, dropping punctuation.

        Here are some examples.
        >>> SentenceRotator("It's but a dream").split_sentence()
        ["It's", 'but', 'a', 'dream']
        >>> SentenceRotator('Origin: Any & All').split_sentence()
        ['Origin', 'Any', 'All']
        """
        return [re.search(r'\b.*\b', w).group(0)
                for w in self.sentence.split() if re.search(r'\b.*\b', w)]

    def rotations(self):
        l = self.split_sentence()
        d = collections.deque(l)
        for i in range(len(l)):
            if d[0].lower() not in self.stopwords:
                (yield d)
            d.rotate()
