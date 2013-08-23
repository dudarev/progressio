import unittest

import os
import sys
sys.path.insert(0, "..")

from progressio.progressio import add, load_items, done, get_item


class TestDone(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_done(self):
        """Test adding one item"""
        add('step that will be done')
        items = load_items()
        pk = items[0].pk
        done(pk)
        i = get_item(pk)
        self.assertTrue(i.is_done)

if __name__ == '__main__':
    unittest.main()
