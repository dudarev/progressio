from datetime import datetime
import os
import sys
import unittest

sys.path.insert(0, "../..")

from progressio.progressio import (
    load_items, _parse_item, PROGRESSIO_DIR)


TEST_ITEM_TITLE = "Test item"
TEST_ITEM_ADDED_AT = datetime(2014, 03, 13, 12, 55, 14)
TEST_ITEM_FILE_CONTENT = """---
title: {title}
added_at: {added_at_str}
done_at: 2014-03-13T12:55:15
---
Some extra text
""".format(
    title=TEST_ITEM_TITLE,
    added_at_str=TEST_ITEM_ADDED_AT.isoformat())


class TestLoad(unittest.TestCase):
    """
    Tests for loading items.
    """

    def _create_items(self, N):
        """
        Creates N files that represent items.
        """

        # create the directory
        if not os.path.exists(PROGRESSIO_DIR):
            os.makedirs(PROGRESSIO_DIR)

        # create N files in it
        for i in xrange(N):
            filename = os.path.join(
                PROGRESSIO_DIR,
                '2014030912{i:04d}'.format(i=i))
            open(filename, 'a').close()

    def test_load_count(self):
        """
        Tests that loaded items are counted correctly.
        """

        # create manually the structure of data that corresponds to valid items
        self._create_items(3)

        # load them
        items = load_items()
        self.assertEqual(len(items), 3)

    def test_parse_item(self):
        item = _parse_item(TEST_ITEM_FILE_CONTENT)
        self.assertEqual(item.title, TEST_ITEM_TITLE)
        self.assertEqual(item.added_at, TEST_ITEM_ADDED_AT)
