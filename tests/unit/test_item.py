# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

from progressio.progressio import Item
from .base import BaseUnitCase


class TestItem(BaseUnitCase):
    def test_adding_child(self):
        item1_title = 'item 1'
        item2_title = 'item 2'
        i1 = Item(title=item1_title)
        i2 = Item(title=item2_title)
        i1.add_child(i2)
        self.assertEqual(i1.children[0].title, item2_title)
        self.assertEqual(i2.parent.title, item1_title)

    def test_removing_from_children(self):
        item1_title = 'item 1'
        item2_title = 'item 2'
        i1 = Item(title=item1_title)
        i2 = Item(title=item2_title, path='1/1')
        i1.add_child(i2)
        i2.remove_from_children()
        self.assertFalse(i2 in i1.children)
        self.assertTrue(i2.parent is None)
        i1.remove_from_children()
        self.assertTrue(i2.parent is None)
