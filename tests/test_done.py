import unittest

import os
import sys
sys.path.insert(0, "..")

from progress.progress import add, load_items, done


class TestDone(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_done(self):
        """Test adding one item"""
        add('test that will be done')
        data = load_items()
        print len(data['items'].keys())
        items = data['items']
        done(items.keys()[0])
        data = load_items()
        self.assertTrue(data['items']['0'].get('done', False))


if __name__ == '__main__':
    unittest.main()
