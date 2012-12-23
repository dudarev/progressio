import unittest

import os
import sys
sys.path.insert(0, "..")

from progress.progress import add, get_item


class TestLoading(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_get_non_existant_item(self):
        add('test')
        self.assertTrue(get_item(9999999) is None)


if __name__ == '__main__':
    unittest.main()
