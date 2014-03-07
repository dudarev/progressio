import unittest

import sys
import subprocess

sys.path.insert(0, "..")

from .base import BaseCase


class TestVersion(BaseCase):
    def test_help(self):
        """
        Test help is shown for `help`, `-h`, `--help` commands.
        """
        option_variations = ['help', '-h', '--help']
        for o in option_variations:
            output = subprocess.check_output(
                "../progressio/progressio.py {}".format(o),
                stderr=subprocess.STDOUT,
                shell=True)
            self.assertTrue('usage:' in output)


if __name__ == '__main__':
    unittest.main()
