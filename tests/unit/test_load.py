from unittest import TestCase

import os
import sys

sys.path.insert(0, "../..")

from progressio.progressio import (
    load_items, PROGRESSIO_DIR)


class TestLoad(TestCase):
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
