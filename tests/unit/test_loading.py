# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

from progressio.progressio import (
    ITEM_TAB,
    _find_line_level,
    Item, load_items)
from .base import BaseUnitCase

LOAD_TEST = """1 - item 1
    1 - item 2
    2 - item 3
        1 - item 4
2 - item 5
"""


class TestLoading(BaseUnitCase):
    def test_from_string(self):
        """Tests function for parsing a line
        """
        line = 'title'
        item = Item.from_string(line)
        self.assertEqual(item.title, line)
        line = '        1/2/1 - item 4'
        item = Item.from_string(line)
        self.assertEqual(item.path, '1/2/1')
        self.assertEqual(item.title, 'item 4')

    def test_line_level(self):
        line = 'test line'
        level = _find_line_level(line)
        self.assertEqual(level, 0)
        line = ITEM_TAB + 'test line'
        level = _find_line_level(line)
        self.assertEqual(level, 1)
        line = 2 * ITEM_TAB + 'test line'
        level = _find_line_level(line)
        self.assertEqual(level, 2)

    def test_loading(self):
        items = load_items(LOAD_TEST)
        self.assertEqual(items[()].children[0].title, 'item 1')
        self.assertEqual(items[()].children[0].children[0].title, 'item 2')
        self.assertEqual(items[()].children[0].children[1].title, 'item 3')
        self.assertEqual(
            items[()].children[0].children[1].children[0].title, 'item 4')
        self.assertEqual(items[()].children[1].title, 'item 5')

    def test_next_child_path(self):
        """Test that next_child_path field is added."""
        items = load_items(LOAD_TEST)
        print('items inside test=', items)
        item = items[(1, )]
        print('item =', item)
        print('item.path =', item.path)
        self.assertEqual(item.next_child_path, 3)
        item = items[(2, )]
        self.assertEqual(item.next_child_path, 1)
        item = items[(1, 2)]
        self.assertEqual(item.next_child_path, 2)
