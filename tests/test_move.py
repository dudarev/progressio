import unittest

import os
import sys
import sqlite3
from subprocess import call, Popen, PIPE

sys.path.insert(0, "..")

from progressio.progressio import (
    PROGRESS_DB_FILE_NAME, Item)


class TestMove(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_move_subitem(self):
        """
        Test that subitem can be moved.
        """

        # create progress.yaml
        p = Popen('../progressio/progressio.py', stdin=PIPE)
        p.communicate('y\n')

        call(
            '../progressio/progressio.py add -t "1st item"',
            stdout=PIPE, shell=True)

        call(
            '../progressio/progressio.py add -p 1 -t "subitem"',
            stdout=PIPE, shell=True)

        call(
            '../progressio/progressio.py add -t "2nd item"',
            stdout=PIPE, shell=True)

        call(
            '../progressio/progressio.py move 2 -p 3',
            stdout=PIPE, shell=True)

        # in database item with pk=1 has a child, it's the second item added
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        cur.execute("SELECT * FROM item WHERE pk=1")
        items = cur.fetchall()
        item1 = Item(*items[0])
        cur.execute("SELECT * FROM item WHERE pk=3")
        items = cur.fetchall()
        item2 = Item(*items[0])
        con.close()

        self.assertFalse(2 in item1.children)
        self.assertTrue(2 in item2.children)


if __name__ == '__main__':
    unittest.main()
