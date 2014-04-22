import os
import sys

sys.path.insert(0, "../..")

from progressio.progressio import (
    _create_dir_if_needed, _parse_file,
    add, get_item, load_items_list, PROGRESSIO_DIR)

from .base import BaseUnitCase


TEST_FILENAME = "1-test-title"
TEST_TITLE = "Test title"
TEST_ITEM_PATH = "1"


class TestLoad(BaseUnitCase):
    """Tests for loading items.
    """

    def _paths_from_create_items(self, N):
        """Creates N datetime instances that correspond to ids created by
        self._create_items"""
        return [str(i) for i in xrange(N)]

    def _create_items(self, N):
        """Creates N files that represent items.
        """

        _create_dir_if_needed()

        # create N files in it
        for i in xrange(1, N):
            filename = os.path.join(
                PROGRESSIO_DIR,
                '{i:d}'.format(i=i))
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
        self.assertEqual(item.path, TEST_ITEM_PATH)

    def test_load_count(self):
        """Tests that loaded items are counted correctly.
        """

        # create manually the structure of data that corresponds to valid items
        self._create_items(3)

        # load them
        items = load_items_list()
        self.assertEqual(len(items), 3)

    def test_load_ids(self):

        # create manually the structure of data that corresponds to valid items
        self._create_items(3)
        
        # get list of items and a list of expected created_at datetimes
        items = load_items_list()
        paths_list = self._paths_from_create_items(3)

        for i in items:
            self.assertIn(i.path, paths_list)

    def test_get_item(self):
        """Tests getting item based on its path.
        """
        item_title = 'test1'
        add(item_title)
        item = get_item('1')
        self.assertEqual(item.title, item_title)
