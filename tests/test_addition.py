import unittest

import os
import sys
sys.path.insert(0, "..")

from progress.progress import add, load_items, get_item


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
        parent_pk = items[1].pk
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


if __name__ == '__main__':
    unittest.main()
