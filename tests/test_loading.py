import unittest
from subprocess import Popen, PIPE

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

    def test_subitem_tabulated(self):
        add('test1')
        add('test2')
        add('subitem of test1', parent_pk=1)
        out, err = Popen(["../progress/progress.py"], stdout=PIPE).communicate()
        print out
        self.assertTrue('1 - test1\n    3 - subitem of test1' in out)


if __name__ == '__main__':
    unittest.main()
