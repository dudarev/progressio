import unittest
import yaml

import os
import sys
sys.path.insert(0, "..")

from progress.progress import add


def load_items():
    return [i for i in yaml.load_all(open('progress.yaml'))]


class TestAddition(unittest.TestCase):
    def setUp(self):
        """Clean up old progress files."""
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

    def test_addition(self):
        """Test adding one item"""
        add('test')
        items = load_items()
        is_added = False
        for i in items:
            print i
            if i.get('step', {}).get('title', '') == 'test':
                is_added = True
                break
        self.assertTrue(is_added)

    def test_info(self):
        """Tests that the first item is info"""
        add('testing info')
        items = load_items()
        self.assertTrue('info' in items[0])


if __name__ == '__main__':
    unittest.main()
