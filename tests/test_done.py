import unittest

import sys

sys.path.insert(0, "..")

from progressio.progressio import add, load_items, done, get_item

from .base import BaseCase


class TestDone(BaseCase):
    def test_done(self):
        """Test adding one item"""
        add('step that will be done')
        items = load_items()
        pk = items[0].pk
        done(pk)
        i = get_item(pk)
        self.assertEqual(i.is_done, 'TRUE')


if __name__ == '__main__':
    unittest.main()
