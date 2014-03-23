# -*- coding: utf-8 -*-

import os
import mock
import shutil
import sys
from .base import BaseUnitCase

sys.path.insert(0, "../..")

from progressio.progressio import (
    _create_dir_if_needed, _get_filename,
    add, load_items, get_item, PROGRESSIO_DIR)
    

class MockedDateTime(object):
    "A fake replacement for date that can be mocked for testing."
    def __new__(cls, *args, **kwargs):
        return object.__new__(object, *args, **kwargs)


class TestAddition(BaseUnitCase):
    def test_create_dir_if_needed(self):
        """
        Tests function _create_dir_if_needed
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

    # TODO: implement
    @mock.patch('progressio.progressio.datetime', MockedDateTime)
    def test_generate_filename(self):
        from datetime import datetime
        mocked_now = datetime(2014, 3, 20, 12, 0, 0)
        MockedDateTime.utcnow = classmethod(lambda cls: mocked_now)
        filename = _get_filename('Test  title')
        self.assertEqual(filename, '20140320120000-test-title')
        filename = _get_filename(u'Test title 1234 абв')
        self.assertEqual(filename, '20140320120000-test-title-1234')
        filename = _get_filename(u'   ')
        self.assertEqual(filename, '20140320120000-')

    # TODO: implement
    def test_generate_filename_if_id_exists(self):
        assert False

    # TODO: implement
    def test_count(self):
        """Test adding two items"""
        add('test1')
        add('test2')
        items = load_items()
        self.assertEqual(len(items), 2)

    # TODO: implement
    @mock.patch('progressio.progressio.datetime', MockedDateTime)
    def test_content(self):
        from datetime import datetime
        mocked_now = datetime(2014, 3, 20)
        MockedDateTime.now = classmethod(lambda cls: mocked_now)
        title = 'test title'
        add(title)
        items = load_items()
        self.assertEqual(items[0].title, title)
        self.assertEqual(items[0].added_at, mocked_now)
        pass

    # TODO: rewrite
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

    # TODO: rewrite
    def test_add_subsubitem(self):
        """
        Subitem to subitem can be added.
        """
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
