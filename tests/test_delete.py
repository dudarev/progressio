import unittest

import os
import sys
import subprocess

sys.path.insert(0, "..")

from progressio.progressio import (
    add, get_item)


class TestDelete(unittest.TestCase):
    def setUp(self):
        """
        Clean up old progress files.
        """
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_item_can_be_deleted(self):
        """
        Item can be deleted and message is shown.
        """
        # create progress.db
        p = subprocess.Popen('../progressio/progressio.py', stdin=subprocess.PIPE)
        p.communicate('y\n')

        # add item, it is added with pk=1
        add('item to be deleted')

        p = subprocess.Popen(
            '../progressio/progressio.py delete 1',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True)
        output = p.communicate('y\n')[0]
        self.assertTrue("Deleted item 1" in output)

        # item is not in database
        self.assertTrue(get_item(1) is None)

    def test_if_not_confirmed_not_deleted(self):
        """
        If delete operation is not confirmed item is not deleted.
        """
        # create progress.db
        p = subprocess.Popen('../progressio/progressio.py', stdin=subprocess.PIPE)
        p.communicate('y\n')

        # add item, it is added with pk=1
        add('item to be deleted')

        p = subprocess.Popen(
            '../progressio/progressio.py delete 1',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True)
        output = p.communicate('n\n')[0]
        self.assertFalse("Deleted item 1" in output)

        # item is in database
        self.assertFalse(get_item(1) is None)


if __name__ == '__main__':
    unittest.main()
