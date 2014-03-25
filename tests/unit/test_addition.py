# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps
import os
import mock
import shutil
import sys

from .base import BaseUnitCase

sys.path.insert(0, "../..")

from progressio.progressio import (
    _create_dir_if_needed, _get_filename,
    add, load_items, get_item, PROGRESSIO_DIR)

TEST_DATETIME = datetime(2014, 3, 20, 12, 0, 0)
TEST_TIMESTAMP = '20140320120000'


class MockedDateTime(object):
    "A fake replacement for date that can be mocked for testing."
    def __new__(cls, *args, **kwargs):
        return object.__new__(object, *args, **kwargs)


def fixed_utcnow(func):
    @wraps(func)
    @mock.patch('progressio.progressio.datetime', MockedDateTime)
    def wrapped_function(*args, **kwargs):
        mocked_now = TEST_DATETIME
        MockedDateTime.utcnow = classmethod(lambda cls: mocked_now)
        return func(*args, **kwargs)
    return wrapped_function


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

    @fixed_utcnow
    def test_generate_filename(self):
        filename = _get_filename('Test  title')
        self.assertEqual(filename, '20140320120000-test-title')
        filename = _get_filename(u'Test title 1234 абв')
        self.assertEqual(filename, '20140320120000-test-title-1234')
        filename = _get_filename(u'   ')
        self.assertEqual(filename, '20140320120000-')

    @fixed_utcnow
    def test_generate_filename_if_timestamp_exists(self):
        # create file with name that corresponding to current time (TEST_DATETIME)
        filename = os.path.join(PROGRESSIO_DIR, TEST_TIMESTAMP)
        with open(filename, 'w') as f:
            f.write('Some test title')
        # timestamp is incremented
        filename = _get_filename('Test  title')
        self.assertEqual(filename, '20140320120001-test-title')
        assert False

    # TODO: implement
    def test_count(self):
        """Test adding two items"""
        add('test1')
        add('test2')
        items = load_items()
        self.assertEqual(len(items), 2)

    # TODO: implement
    @fixed_utcnow
    def test_content(self):
        title = 'test title'
        add(title)
        items = load_items()
        self.assertEqual(items[0].title, title)
        self.assertEqual(items[0].added_at, TEST_DATETIME)
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
