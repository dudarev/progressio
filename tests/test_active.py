import unittest

import os
import sys
import subprocess

sys.path.insert(0, "..")

from progressio.progressio import add, active, done, load_items, get_item


class TestActive(unittest.TestCase):
    def setUp(self):
        """
        Clean up old progress files.
        """
        filelist = [f for f in os.listdir(".") if f.startswith("progress.")]
        for f in filelist:
            os.remove(f)

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
        print output
        self.assertTrue("Item {} is marked as active".format(pk) in output)

        i = get_item(pk)
        self.assertEqual(i.is_done, 'FALSE')


if __name__ == '__main__':
    unittest.main()
