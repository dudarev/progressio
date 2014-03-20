from datetime import datetime
import os
import sys
import unittest

sys.path.insert(0, "../..")

from progressio.progressio import (
    _create_dir_if_needed, _parse_file,
    load_items, PROGRESSIO_DIR)


TEST_FILENAME = "20140313125514"
TEST_ITEM_ADDED_AT = datetime(2014, 03, 13, 12, 55, 14)
TEST_TITLE = "Test title"


class TestLoad(unittest.TestCase):
    """
    Tests for loading items.
    """

    def _create_items(self, N):
        """
        Creates N files that represent items.
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
        filename = os.path.join(
            PROGRESSIO_DIR,
            TEST_FILENAME)
        with open(filename, 'w') as f:
            f.write(TEST_TITLE)

    def test_load_count(self):
        """
        Tests that loaded items are counted correctly.
        """

        # create manually the structure of data that corresponds to valid items
        self._create_items(3)

        # load them
        items = load_items()
        self.assertEqual(len(items), 3)

    def test_parse_file(self):
        self._create_file()
        item = _parse_file(TEST_FILENAME)
        self.assertEqual(item.title, TEST_TITLE)
        self.assertEqual(item.added_at, TEST_ITEM_ADDED_AT)
