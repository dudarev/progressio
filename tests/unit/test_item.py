# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

from progressio.progressio import (
    FULL_PROGRESS_FILENAME,
    Item, ItemsDict)
from .base import BaseUnitCase


class TestItem(BaseUnitCase):
    def test_local_path(self):
        i1 = Item(path='1/2/3')
        self.assertEqual(i1.path, '1/2/3')
        self.assertEqual(i1.local_path, 3)

    def test_adding_child(self):
        item1_title = 'item 1'
        item2_title = 'item 2'
        i1 = Item(title=item1_title, path=(1, ))
        i2 = Item(title=item2_title)
        i1.add_child(i2)
        self.assertEqual(i1.children[0].title, item2_title)
        self.assertEqual(i2.parent.title, item1_title)

    def test_removing_from_children(self):
        item1_title = 'item 1'
        item2_title = 'item 2'
        i1 = Item(title=item1_title, path=(1, ))
        i2 = Item(title=item2_title)
        i1.add_child(i2)
        i2.remove_from_children()
        self.assertFalse(i2 in i1.children)
        self.assertTrue(i2.parent is None)
        i1.remove_from_children()
        self.assertTrue(i2.parent is None)


class TestItemsDict(BaseUnitCase):
    def test_save(self):
        item1 = Item(title='test 1')
        item2 = Item(title='test 2')
        items = ItemsDict()
        items[()].add_child(item1)
        items[()].add_child(item2)
        items.save()
        with open(FULL_PROGRESS_FILENAME, 'r') as f:
            line1 = f.readline()
            line2 = f.readline()
            self.assertEqual(line1.strip(), '1 - test 1')
            self.assertEqual(line2.strip(), '2 - test 2')
