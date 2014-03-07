import unittest

import sys
import subprocess

sys.path.insert(0, "..")

from progressio.progressio import __version__

from .base import BaseCase


class TestVersion(BaseCase):
    def test_version(self):
        """
        Test version output.
        """
        # check that version is in output
        output = subprocess.check_output(
            "../progressio/progressio.py version",
            stderr=subprocess.STDOUT,
            shell=True)
        self.assertTrue(__version__ in output)


if __name__ == '__main__':
    unittest.main()
