import unittest

import os
import sys
sys.path.insert(0, "..")

from progress.progress import add, load_items, get_info


class TestLoading(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_get_info(self):
        """Test adding one item"""
        add('test')
        items = load_items()
        info = get_info(items)
        print info
        self.assertTrue('info' in info)


if __name__ == '__main__':
    unittest.main()
