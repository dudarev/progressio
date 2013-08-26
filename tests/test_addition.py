import unittest

import os
import sys
import sqlite3
# TODO: move all method to subprocess
from subprocess import call, check_output, Popen, PIPE, STDOUT
import subprocess

sys.path.insert(0, "..")

from progressio.progressio import (
    add, load_items, get_item,
    PROGRESS_DB_FILE_NAME, Item)


class TestAddition(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_addition(self):
        """Test adding one item"""
        add('test2')
        add('test')
        items = load_items()
        is_added = False
        for i in items:
            if i.title == 'test2':
                is_added = True
                break
        self.assertTrue(is_added)

    def test_message_when_adding(self):
        """
        Test that pk and message are shown when adding new item.
        """
        # create progress.yaml
        p = Popen('../progressio/progressio.py', stdin=PIPE)
        p.communicate('y\n')

        ITEM_TITLE = 'item that will be added'
        output = check_output(
            '../progressio/progressio.py add -t "{0}"'.format(ITEM_TITLE),
            stderr=STDOUT,
            shell=True)

        self.assertTrue("1 - {}".format(ITEM_TITLE) in output)

    def test_add_subitem(self):
        """Test that subitem may be added to some item."""
        TEST_TEXT = 'test3'
        TEST_TEXT_SUBITEM = 'test33'
        add(TEST_TEXT)
        items = load_items()
        parent_pk = items[0].pk
        add(TEST_TEXT_SUBITEM, parent_pk=parent_pk)
        subitem_pk = get_item(parent_pk).children[0]
        self.assertEqual(get_item(subitem_pk).title, TEST_TEXT_SUBITEM)

    def test_add_subsubitem(self):
        """TODO:"""
        TEST_TEXT_SUBITEM = 'sub test'
        TEST_TEXT_SUBSUBITEM = 'sub sub test'
        add(TEST_TEXT_SUBITEM)
        add('test2')
        items = load_items()
        parent_pk = items[1].pk
        add(TEST_TEXT_SUBITEM, parent_pk=parent_pk)
        parent = get_item(parent_pk)
        subitem = get_item(parent.children[0])
        add(TEST_TEXT_SUBSUBITEM, parent_pk=subitem.pk)
        subitem = get_item(subitem.pk)
        subsubitem_pk = subitem.children[0]
        self.assertEqual(get_item(subsubitem_pk).title, TEST_TEXT_SUBSUBITEM)

    def test_add_subitem_from_command_line(self):
        """
        Test that one can add subitem from command line.
        """

        # create progress.yaml
        p = Popen('../progressio/progressio.py', stdin=PIPE)
        p.communicate('y\n')

        ITEM_TITLE = 'first item'
        call(
            '../progressio/progressio.py add -t "{0}"'.format(ITEM_TITLE),
            stdout=PIPE,
            shell=True)

        SUBITEM_TITLE = 'child of first item'
        call(
            '../progressio/progressio.py add -p 1 -t "{0}"'.format(SUBITEM_TITLE),
            stdout=PIPE,
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
        # create progress.yaml
        p = Popen('../progressio/progressio.py', stdin=PIPE)
        p.communicate('y\n')

        ITEM_TITLE = 'item that will not be added'
        # -t flag is missing
        try:
            check_output(
                '../progressio/progressio.py add "{0}"'.format(ITEM_TITLE),
                stderr=STDOUT,
                shell=True)
            self.fail(msg="This command exit with code 1")
        except subprocess.CalledProcessError, e:
            self.assertTrue('Error: no title is specified' in e.output)


if __name__ == '__main__':
    unittest.main()
