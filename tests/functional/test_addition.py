import unittest

import sys
import sqlite3
import subprocess

sys.path.insert(0, "../..")

from progressio.progressio import (
    PROGRESS_DB_FILE_NAME, Item)

from .base import BaseCase


class TestAddition(BaseCase):
    def test_message_when_adding(self):
        """
        Test that pk and message are shown when adding new item.
        """
        ITEM_TITLE = 'item that will be added'
        output = subprocess.check_output(
            '../progressio/progressio.py add -t "{0}"'.format(ITEM_TITLE),
            stderr=subprocess.STDOUT,
            shell=True)

        self.assertTrue("1 - {}".format(ITEM_TITLE) in output)

    def test_add_subitem_from_command_line(self):
        """
        Test that one can add subitem from command line.
        """
        ITEM_TITLE = 'first item'
        subprocess.call(
            '../progressio/progressio.py add -t "{0}"'.format(ITEM_TITLE),
            stdout=subprocess.PIPE,
            shell=True)

        SUBITEM_TITLE = 'child of first item'
        subprocess.call(
            '../progressio/progressio.py add -p 1 -t "{0}"'.format(SUBITEM_TITLE),
            stdout=subprocess.PIPE,
            shell=True)

        # in database item with pk=1 has a child, it's the second item added
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        cur.execute("SELECT * FROM item WHERE pk=1")
        items = cur.fetchall()
        item = Item(*items[0])
        con.close()
        self.assertTrue(2 in item.children)

    def test_error_message_if_item_is_not_added(self):
        """
        Test that error message is shown if item is not added.
        """
        ITEM_TITLE = 'item that will not been added'
        # -t flag is missing
        try:
            subprocess.check_output(
                '../progressio/progressio.py add "{0}"'.format(ITEM_TITLE),
                stderr=subprocess.STDOUT,
                shell=True)
            self.fail(msg="This command exit with code 1")
        except subprocess.CalledProcessError, e:
            self.assertTrue('Error: no title is specified' in e.output)


if __name__ == '__main__':
    unittest.main()
