"""
    linkfile
    ~~~~~~~~

    This module provides a class to process link files.

    :copyright: (c) 2016 by Peter Jahn
    :license:   BSD (see LICENSE for details)
"""


import os.path

from . import filenamesanitizer
from . import urlautotagger
from . import urlautotitler


class LinkFile(object):

    """docstring for LinkFile"""

    FIELD_URL = 'url'
    FIELD_TITLE = 'title'
    FIELD_TAGS = 'tags'
    FIELD_COMMENT = 'comment'

    field_names = {FIELD_COMMENT, FIELD_TAGS, FIELD_TITLE, FIELD_URL}

    SEPARATOR = '='

    def __init__(self, filename=None, url=None, title=None):
        """Create an instance (read from file or build per parameters).

        Initialize a new LinkFile object.  Exactly one of filename or
        url is required.  If url is given, title is optional, otherwise
        it cannot be used.  The constructor will raise a RuntimeError if
        any these requirements aren't met.

        If filename is supplied, assume the named file contains a link
        saved previously and try to read it.  Only if this succeeds, set
        is_valid.

        if url is supplied, use this and the then optional title as
        attributes for the new instance, preparing it to be saved later.

        Keyword arguments:
        filename -- if given, name of file assumed to contain a link
            saved previously (default None)
        url      -- if given, the target URL for the link (default None)
        title    -- if given, the title for the link (default None)
        """
        super(LinkFile, self).__init__()
        self._is_valid = False
        self._data = {}
        self._filename = None
        if filename:
            if title or url:
                raise RuntimeError('Cannot specify title or url with filename')
            self._attempt_to_load(filename)
        elif url:
            self._create(url, title)
        else:
            raise RuntimeError('Must specify either url or filename')

    def __getattr__(self, name):
        if name == LinkFile.FIELD_URL:
            return self._data[LinkFile.FIELD_URL]
        if name == LinkFile.FIELD_TITLE:
            return self._data[LinkFile.FIELD_TITLE]
        raise AttributeError(name)

    def __repr__(self):
        if self._filename:
            return "LinkFile(filename='{0}')".format(self._filename)
        if self.url:
            return "LinkFile(url='{0}', title='{1}')".format(
                self.url, self.title)
        return "LinkFile()"

    def __str__(self):
        return "LinkFile: valid {0}, filename {1}, data {2}".format(
            self._is_valid, self._filename, self._data)

    def _add_field(self, line):
        # TODO this strip is probably superfluous
        (field_name, separator, value) = line.strip().partition(LinkFile.SEPARATOR)
        if field_name.strip() in LinkFile.field_names:
            self._data[field_name] = value.strip()

    def _read(self, f):
        # TODO Limit number of lines scanned
        while True:
            l = f.readline()
            if not l: break
            self._add_field(l)

    def _attempt_to_load(self, filename):
        with open(filename) as f:
            self._read(f)
        if self._contains_required_fields():
            self._is_valid = True
            self._filename = filename

    def _create(self, url, title):
        self._data[LinkFile.FIELD_URL] = url
        if not title:
            title = urlautotitler.UrlAutoTitler(url).process().get_title()
        self._data[LinkFile.FIELD_TITLE] = title
        tags = urlautotagger.UrlAutoTagger(url).process().get_tags()
        if tags:
            self._data[LinkFile.FIELD_TAGS] = tags
        self._is_valid = True

    def _save(self, target_folder):
        def write_field(f, field, value):
            f.write('{0}{1}{2}\n'.format(field, LinkFile.SEPARATOR, value))

        basename = filenamesanitizer.FilenameSanitizer(self.title)()
        # if verbose: print("+ {0}".format(basename))
        with open(os.path.join(target_folder, basename), 'w') as f:
            write_field(f, LinkFile.FIELD_URL, self.url)
            write_field(f, LinkFile.FIELD_TITLE, self.title)
            tags = self._data[LinkFile.FIELD_TAGS]
            if tags:
                write_field(f, LinkFile.FIELD_TAGS, tags)

    def _contains_required_fields(self):
        """Return whether all required fields are defined for this link.

        At the bare minimum, a URL must be defined.  Other checks could
        be added in the future.
        """
        return LinkFile.FIELD_URL in self._data
