# -*- coding: utf-8 -*-

from datetime import datetime
import os
import shutil
import sys

sys.path.insert(0, "../..")

from progressio.progressio import _create_dir_if_needed, PROGRESSIO_DIR
from .base import BaseUnitCase


TEST_DATETIME = datetime(2014, 3, 20, 12, 0, 0)
TEST_TIMESTAMP = '20140320120000'


class MockedDateTime(object):
    "A fake replacement for date that can be mocked for testing."
    def __new__(cls, *args, **kwargs):
        return object.__new__(object, *args, **kwargs)


class TestAddition(BaseUnitCase):
    def test_create_dir_if_needed(self):
        """Tests function _create_dir_if_needed
        """

        # remove PROGRESSIO_DIR check that function creates it
        if os.path.exists(PROGRESSIO_DIR):
            shutil.rmtree(PROGRESSIO_DIR)

        self.assertFalse(os.path.exists(PROGRESSIO_DIR))
        _create_dir_if_needed()
        self.assertTrue(os.path.exists(PROGRESSIO_DIR))

        # check that it runs well when it already exists
        _create_dir_if_needed()
        self.assertTrue(os.path.exists(PROGRESSIO_DIR))

    # def test_count(self):
    #     """Test adding two items"""
    #     add('test1')
    #     add('test2')
    #     items = load_items_list()
    #     self.assertEqual(len(items), 2)

    # def test_path_id(self):
    #     add('test1')
    #     item = load_items_list()[0]
    #     self.assertEqual(item.path, '1')
    #     add('test2')
    #     item = load_items_list()[1]
    #     self.assertEqual(item.path, '2')

    # def test_content(self):
    #     title = 'test title'
    #     add(title)
    #     items = load_items_list()
    #     self.assertEqual(items[0].title, title)
    #     pass

    # def test_add_subitem(self):
    #     """Test that subitem may be added to some item."""
    #     item_title = 'test1'
    #     subitem_title = 'test11'

    #     add(item_title)
    #     items = load_items_list()
    #     add(subitem_title, parent_path=items[0].path)

    #     self.assertEqual(get_item('1/1').title, subitem_title)
