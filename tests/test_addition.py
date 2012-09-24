import unittest
import yaml

import os
import sys
sys.path.insert(0, "..")

from progress.progress import add, load_items


class TestAddition(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_addition(self):
        """Test adding one item"""
        add('test')
        add('test2')
        items = load_items()
        is_added = False
        for i in items['items']:
            if items['items'][i].get('title', '') == 'test':
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
        TEST_TEXT = 'test'
        add(TEST_TEXT)
        add('test2')
        items = load_items()
        add(TEST_TEXT, items['items']['0']['id'])
        info, items = load_items()
        self.assertEqual(items['items']['0']['items']['0']['title'], TEST_TEXT)

    def test_info(self):
        """Tests that the first item is info"""
        add('testing info')
        items = load_items()
        self.assertTrue('info' in items)


if __name__ == '__main__':
    unittest.main()
