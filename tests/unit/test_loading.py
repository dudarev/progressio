# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

from progressio.progressio import (
    ITEM_TAB,
    _find_line_level, _parse_line,
    load_items)
from .base import BaseUnitCase

LOAD_TEST = """1 - item 1
    1/1 - item 2
    1/2 - item 3
        1/2/3 - item 4
2 - item 5
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
        self.assertEqual(items['root'].children[0].title, 'item 1')
        self.assertEqual(items['root'].children[0].children[0].title, 'item 2')
        self.assertEqual(items['root'].children[0].children[1].title, 'item 3')
        self.assertEqual(
            items['root'].children[0].children[1].children[0].title, 'item 4')
        self.assertEqual(items['root'].children[1].title, 'item 5')

    def test_next_child_path(self):
        """Test that next_child_path field is added."""
        items = load_items(LOAD_TEST)
        item = items['1']
        self.assertEqual(item.next_child_path, 3)
