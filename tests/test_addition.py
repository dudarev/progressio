import unittest

import os
import sys
import sqlite3
from subprocess import call, Popen, PIPE

sys.path.insert(0, "..")

from progress.progress import (
    add, load_items, get_item, PROGRESS_TXT_FILE_NAME,
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

    def test_added_to_txt(self):
        """Test that item is added to progress.txt"""
        TEST_TEXT = 'test'
        add(TEST_TEXT)
        add('test2')
        test_in_txt = False
        for line in open('progress.txt', 'r'):
            if TEST_TEXT in line:
                test_in_txt = True
                break
        self.assertTrue(test_in_txt)

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

        def progress_txt_has_text(text):
            if not os.path.exists(PROGRESS_TXT_FILE_NAME):
                return False
            for line in open(PROGRESS_TXT_FILE_NAME, 'r'):
                if text in line:
                    return True
            return False

        # create progress.yaml
        p = Popen('../progress/progress.py', stdin=PIPE)
        p.communicate('y\n')

        ITEM_TITLE = 'first item'
        call(
            '../progress/progress.py add -t "{0}"'.format(ITEM_TITLE),
            stdout=PIPE,
            shell=True)
        self.assertTrue(progress_txt_has_text(ITEM_TITLE))

        SUBITEM_TITLE = 'child of first item'
        call(
            '../progress/progress.py add -p 1 -t "{0}"'.format(SUBITEM_TITLE),
            stdout=PIPE,
            shell=True)
        self.assertTrue(progress_txt_has_text(SUBITEM_TITLE))

        # in database item with pk=1 has a child, it's the second item added
        con = sqlite3.connect(PROGRESS_DB_FILE_NAME)
        cur = con.cursor()
        cur.execute("SELECT * FROM item WHERE pk=1")
        items = cur.fetchall()
        item = Item(*items[0])
        con.close()
        self.assertTrue(u'2' in item.children)


if __name__ == '__main__':
    unittest.main()
