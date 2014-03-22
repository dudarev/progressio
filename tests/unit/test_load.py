from datetime import datetime
import os
import sys

sys.path.insert(0, "../..")

from progressio.progressio import (
    _create_dir_if_needed, _parse_file,
    load_items, PROGRESSIO_DIR)

from .base import BaseUnitCase


TEST_FILENAME = "20140313125514"
TEST_ITEM_ADDED_AT = datetime(2014, 03, 13, 12, 55, 14)
TEST_TITLE = "Test title"


class TestLoad(BaseUnitCase):
    """Tests for loading items.
    """

    def _datetimes_from_create_items(self, N):
        """Creates N datetime instances that correspond to ids created by
        self._create_items"""
        return [datetime(2014, 3, 9, 12, 0, i) for i in xrange(N)]

    def _create_items(self, N):
        """Creates N files that represent items.
        """

        _create_dir_if_needed()

        # create N files in it
        for i in xrange(N):
            filename = os.path.join(
                PROGRESSIO_DIR,
                '2014030912{i:04d}'.format(i=i))
            open(filename, 'a').close()

    def _create_file(self):
        _create_dir_if_needed()
        filename = os.path.join(PROGRESSIO_DIR, TEST_FILENAME)
        with open(filename, 'w') as f:
            f.write(TEST_TITLE)

    def test_parse_file(self):
        self._create_file()
        filename = os.path.join(PROGRESSIO_DIR, TEST_FILENAME)
        item = _parse_file(filename)
        self.assertEqual(item.title, TEST_TITLE)
        self.assertEqual(item.added_at, TEST_ITEM_ADDED_AT)

    def test_load_count(self):
        """Tests that loaded items are counted correctly.
        """

        # create manually the structure of data that corresponds to valid items
        self._create_items(3)

        # load them
        items = load_items()
        self.assertEqual(len(items), 3)

    def test_load_ids(self):

        # create manually the structure of data that corresponds to valid items
        self._create_items(3)
        
        # get list of items and a list of expected created_at datetimes
        items = load_items()
        dt_list = self._datetimes_from_create_items(3)

        for i in items:
            self.assertIn(i.added_at, dt_list)
