import unittest
from subprocess import Popen, PIPE

import os
import sys
sys.path.insert(0, "..")

from progressio.progressio import (
    add, get_item,
    load_items, done,)


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
        out, err = Popen(["../progressio/progressio.py"], stdout=PIPE).communicate()
        self.assertTrue('1 - test1\n    3 - subitem of test1' in out)

    def test_count(self):
        add('test1')
        add('test2')
        out, err = Popen(["../progressio/progressio.py", "count"], stdout=PIPE).communicate()
        self.assertTrue('done: 0' in out)
        self.assertTrue('total items: 2' in out)
        items = load_items()
        pk = items[0].pk
        done(pk)
        out, err = Popen(["../progressio/progressio.py", "count"], stdout=PIPE).communicate()
        self.assertTrue('done: 1' in out)
        self.assertTrue('total items: 2' in out)

    def test_log(self):
        add('test1')
        add('test2')
        out, err = Popen(["../progressio/progressio.py", "log"], stdout=PIPE).communicate()
        self.assertTrue('test1' in out)
        self.assertTrue('test2' in out)


if __name__ == '__main__':
    unittest.main()
