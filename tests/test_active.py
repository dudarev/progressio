import unittest

import sys
import subprocess

sys.path.insert(0, "..")

from progressio.progressio import add, active, done, load_items, get_item

from .base import BaseCase


class TestActive(BaseCase):
    def test_active(self):
        """
        Test activating one item.
        """
        add('step that will be done and then activated again')
        items = load_items()
        pk = items[0].pk
        done(pk)
        active(pk)
        i = get_item(pk)
        self.assertEqual(i.is_done, 'FALSE')

    def test_active_cli(self):
        """
        Test command line version of active command.
        """
        add('step that will be done and then activated again')
        items = load_items()
        pk = items[0].pk
        done(pk)
        output = subprocess.check_output(
            "../progressio/progressio.py active {}".format(pk),
            stderr=subprocess.STDOUT,
            shell=True)
        self.assertIn("Item {} is marked as active".format(pk), output)

        i = get_item(pk)
        self.assertEqual(i.is_done, 'FALSE')


if __name__ == '__main__':
    unittest.main()
