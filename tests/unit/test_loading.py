# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

from progressio.progressio import (
    ITEM_TAB,
    _find_line_level, _parse_line,
    load_items)
from .base import BaseUnitCase

LOAD_TEST = """item 1
    item 2
    item 3
item 4
"""


class TestLoading(BaseUnitCase):
    def test_parse_line(self):
        """Tests function for parsing a line
        """
        line = 'title'
        item = _parse_line(line)
        self.assertEqual(item.title, line)

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
        self.assertEqual(items[None].children[0].title, 'item 1')
        self.assertEqual(items[None].children[1].title, 'item 4')
        self.assertEqual(items[None].children[0].children[0].title, 'item 2')
        self.assertEqual(items[None].children[1].children[0].title, 'item 3')
